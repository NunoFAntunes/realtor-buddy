"""
Croatian Real Estate LangChain SQL Agent

Main implementation of the LangChain SQL agent for querying Croatian real estate data
using local Llama-3.1-8B model via HuggingFace Transformers.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser

from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline
)
import torch

from ..utils.config import get_database_config
from .schema_analyzer import get_langchain_config
from .training_examples import format_examples_for_prompt

logger = logging.getLogger(__name__)

class SQLQueryParser(BaseOutputParser):
    """Custom parser to extract SQL queries from Llama model output."""
    
    def parse(self, text: str) -> str:
        """Extract SQL query from model response."""
        # Remove any markdown code blocks
        if "```sql" in text:
            start = text.find("```sql") + 6
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        
        if "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        
        # Look for SELECT statements
        text_upper = text.upper()
        if "SELECT" in text_upper:
            select_start = text_upper.find("SELECT")
            # Find the end of the query (semicolon or end of text)
            remaining = text[select_start:]
            semicolon = remaining.find(";")
            if semicolon != -1:
                return remaining[:semicolon + 1].strip()
            else:
                return remaining.strip()
        
        return text.strip()

class CroatianRealEstateAgent:
    """
    LangChain SQL Agent for Croatian real estate queries using local Llama-3.1-8B.
    """
    
    def __init__(self, model_name: str = "meta-llama/Llama-3.1-8B-Instruct"):
        """
        Initialize the Croatian Real Estate SQL Agent.
        
        Args:
            model_name: HuggingFace model identifier for local Llama model
        """
        self.model_name = model_name
        self.llm = None
        self.sql_chain = None
        self.db = None
        self.schema_config = get_langchain_config()
        
        logger.info(f"Initializing Croatian Real Estate Agent with model: {model_name}")
    
    def _setup_local_llm(self) -> HuggingFacePipeline:
        """Set up local Llama-3.1-8B model optimized for RTX 2070 + 32GB RAM."""
        logger.info("Setting up local Llama-3.1-8B model for RTX 2070...")
        
        try:
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                padding_side="left"
            )
            
            # Add pad token if it doesn't exist
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # Load model in FP16 without quantization (better quality + your hardware can handle it)
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",  # Automatically use GPU + CPU if needed
                trust_remote_code=True,
                torch_dtype=torch.float16,  # FP16 for GPU efficiency
                low_cpu_mem_usage=True,     # Optimize CPU memory usage
            )
            
            # Create text generation pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=512,
                temperature=0.1,  # Low temperature for consistent SQL generation
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.1,
            )
            
            # Wrap in LangChain HuggingFacePipeline
            llm = HuggingFacePipeline(pipeline=pipe)
            
            logger.info("Successfully loaded local Llama-3.1-8B model")
            return llm
            
        except Exception as e:
            logger.error(f"Failed to load local model: {e}")
            raise RuntimeError(f"Could not initialize local Llama model: {e}")
    
    def _setup_database_connection(self) -> SQLDatabase:
        """Set up database connection for LangChain SQL operations."""
        logger.info("Setting up database connection...")
        
        try:
            # Get database configuration
            db_config = get_database_config()
            
            # Create SQLAlchemy engine with read-only settings
            connection_string = (
                f"mysql+pymysql://{db_config['user']}:{db_config['password']}"
                f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            )
            
            engine = create_engine(
                connection_string,
                poolclass=StaticPool,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False  # Set to True for SQL debugging
            )
            
            # Create LangChain SQLDatabase with our table
            sql_database = SQLDatabase(
                engine=engine,
                include_tables=["agency_properties"],
                sample_rows_in_table_info=3,
                custom_table_info=self.schema_config["table_info"]
            )
            
            logger.info("Successfully connected to MariaDB database")
            return sql_database
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise RuntimeError(f"Database connection failed: {e}")
    
    def _create_sql_prompt_template(self) -> PromptTemplate:
        """Create optimized prompt template for Croatian real estate queries."""
        
        # Get few-shot examples from our training data
        examples = format_examples_for_prompt(num_examples=5)
        
        prompt_template = """You are an expert SQL query generator for Croatian real estate data.

Database Information:
{table_info}

Important Croatian Real Estate Terms:
- stan = apartment, kuća = house
- lokacija = location (use LIKE '%term%' for searches)
- broj_soba = number of bedrooms 
- povrsina = surface area in m² (stored as VARCHAR, cast if needed)
- kat = floor (prizemlje=ground, 1=first floor, potkrovlje=attic)
- lift = elevator (da=yes, ne=no)
- pogled_na_more = sea view (da=yes, ne=no)
- price = price in EUR (use numeric comparisons)

SQL Rules:
1. ALWAYS use LIKE '%term%' for location searches
2. For property types: LIKE '%stan%' for apartments, LIKE '%kuća%' for houses
3. Cast VARCHAR fields to numbers: CAST(povrsina AS UNSIGNED) > 100
4. Croatian boolean values: "da" = yes, "ne" = no
5. ALWAYS add LIMIT clause (max 50 results)
6. Handle NULL values: price IS NOT NULL
7. For JSON fields use JSON_LENGTH() > 0 to check existence

Example Queries:
{examples}

User Question: {input}

Generate ONLY the SQL query. Do not include any explanation or markdown formatting.

SQL Query:"""
        
        return PromptTemplate(
            input_variables=["table_info", "examples", "input"],
            template=prompt_template
        )
    
    def initialize(self) -> None:
        """Initialize the SQL agent with local LLM and database connection."""
        logger.info("Initializing Croatian Real Estate SQL Agent...")
        
        try:
            # Setup local Llama model
            self.llm = self._setup_local_llm()
            
            # Setup database connection
            self.db = self._setup_database_connection()
            
            # Create SQL prompt template
            prompt = self._create_sql_prompt_template()
            
            # Create SQL database chain
            self.sql_chain = SQLDatabaseChain.from_llm(
                llm=self.llm,
                db=self.db,
                prompt=prompt,
                verbose=True,  # Set to False to reduce logging
                use_query_checker=True,  # Enable SQL query validation
                query_checker_prompt=None,  # Use default query checker
                return_intermediate_steps=True,
                output_parser=SQLQueryParser(),
                top_k=20  # Limit results
            )
            
            logger.info("Croatian Real Estate SQL Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize SQL agent: {e}")
            raise
    
    def query(self, natural_language_query: str) -> Dict[str, Any]:
        """
        Execute a natural language query against the Croatian real estate database.
        
        Args:
            natural_language_query: User's question in natural language
            
        Returns:
            Dictionary containing query results, SQL, and metadata
        """
        if not self.sql_chain:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        
        logger.info(f"Processing query: {natural_language_query}")
        
        try:
            # Prepare prompt inputs
            examples = format_examples_for_prompt(num_examples=5)
            
            # Execute the chain
            result = self.sql_chain.invoke({
                "query": natural_language_query,
                "table_info": self.schema_config["table_info"],
                "examples": examples
            })
            
            # Format response
            response = {
                "success": True,
                "query": natural_language_query,
                "sql_query": result.get("intermediate_steps", [{}])[0].get("sql_cmd", ""),
                "result": result.get("result", ""),
                "intermediate_steps": result.get("intermediate_steps", []),
                "error": None
            }
            
            logger.info(f"Query executed successfully: {len(str(result.get('result', '')))} chars returned")
            return response
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return {
                "success": False,
                "query": natural_language_query,
                "sql_query": "",
                "result": "",
                "intermediate_steps": [],
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """Test database connection and model availability."""
        try:
            if not self.db:
                return False
                
            # Test database connection
            test_query = "SELECT COUNT(*) as total FROM agency_properties LIMIT 1"
            result = self.db.run(test_query)
            
            logger.info(f"Database test query result: {result}")
            return True
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_schema_info(self) -> str:
        """Get database schema information for debugging."""
        if not self.db:
            return "Database not initialized"
        
        try:
            return self.db.get_table_info()
        except Exception as e:
            return f"Error getting schema info: {e}"

# Convenience functions
def create_agent(model_name: str = "meta-llama/Llama-3.1-8B-Instruct") -> CroatianRealEstateAgent:
    """Create and initialize a Croatian Real Estate SQL Agent."""
    agent = CroatianRealEstateAgent(model_name=model_name)
    agent.initialize()
    return agent

def quick_query(query: str, model_name: str = "meta-llama/Llama-3.1-8B-Instruct") -> Dict[str, Any]:
    """Execute a quick query without maintaining agent state."""
    agent = create_agent(model_name)
    return agent.query(query)