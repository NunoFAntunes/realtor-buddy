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

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import openai

from ..utils.config import Config
from .schema_analyzer import get_langchain_config
from .training_examples import format_examples_for_prompt

logger = logging.getLogger(__name__)

def get_database_config() -> Dict[str, Any]:
    """Get database configuration dictionary."""
    return Config.get_db_config()

class SQLQueryParser(BaseOutputParser):
    """Custom parser to extract SQL queries from Llama model output."""
    
    def parse(self, text: str) -> str:
        """Extract SQL query from model response and replace SELECT clause with SELECT *."""
        # Remove any markdown code blocks
        if "```sql" in text:
            start = text.find("```sql") + 6
            end = text.find("```", start)
            if end != -1:
                text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end != -1:
                text = text[start:end].strip()
        
        # Look for SELECT statements
        text_upper = text.upper()
        if "SELECT" in text_upper:
            select_start = text_upper.find("SELECT")
            remaining = text[select_start:]
            
            # Find potential end markers for the SQL query
            end_markers = [
                "\nSQLResult:",
                "\n\nSQLResult:",
                "SQLResult:",
                "\n| ",
                "\n---",
                "There are no more rows",
                "\nNote:",
                "\nExplanation:"
            ]
            
            end_pos = len(remaining)
            for marker in end_markers:
                marker_pos = remaining.find(marker)
                if marker_pos != -1 and marker_pos < end_pos:
                    end_pos = marker_pos
            
            # Also check for semicolon (but not if it's followed by result formatting)
            semicolon_pos = remaining.find(";")
            if semicolon_pos != -1:
                # Check if there's result formatting after the semicolon
                after_semicolon = remaining[semicolon_pos + 1:].strip()
                if not after_semicolon or not any(marker.strip() in after_semicolon for marker in end_markers):
                    end_pos = min(end_pos, semicolon_pos + 1)
                else:
                    end_pos = min(end_pos, semicolon_pos)
            
            sql_query = remaining[:end_pos].strip()
            
            # Replace SELECT clause with SELECT *
            sql_query = self._replace_select_with_asterisk(sql_query)
            
            return sql_query
        
        return text.strip()
    
    def _replace_select_with_asterisk(self, sql_query: str) -> str:
        """Replace the SELECT clause with SELECT * to return all columns."""
        import re
        
        # Match SELECT ... FROM pattern with case insensitive regex
        # This handles multi-line selections and complex field lists
        pattern = r'(SELECT\s+)(?:(?:DISTINCT\s+)?(?:[^,\s]+(?:\s*,\s*[^,\s]+)*)?(?:\s*,\s*[^,\s]+)*\s*)(FROM\s+)'
        
        # Use a more robust approach with word boundaries and handle complex cases
        sql_upper = sql_query.upper()
        select_pos = sql_upper.find('SELECT')
        from_pos = sql_upper.find('FROM', select_pos)
        
        if select_pos != -1 and from_pos != -1:
            # Extract parts: before SELECT, SELECT keyword, between SELECT and FROM, FROM and after
            before_select = sql_query[:select_pos]
            select_keyword = sql_query[select_pos:select_pos + 6]  # "SELECT"
            from_and_after = sql_query[from_pos:]
            
            # Reconstruct with SELECT *
            return f"{before_select}{select_keyword} * {from_and_after}"
        
        return sql_query

class CroatianRealEstateAgent:
    """
    LangChain SQL Agent for Croatian real estate queries using OpenAI models.
    """
    
    def __init__(self, model_name: str = "gpt-4.1"):
        """
        Initialize the Croatian Real Estate SQL Agent.
        
        Args:
            model_name: OpenAI model identifier (e.g., "gpt-4.1", "gpt-4")
        """
        self.model_name = model_name
        self.llm = None
        self.sql_chain = None
        self.db = None
        self.schema_config = get_langchain_config()
        
        logger.info(f"Initializing Croatian Real Estate Agent with OpenAI model: {model_name}")
    
    def _setup_openai_llm(self) -> ChatOpenAI:
        """Set up OpenAI model using API key."""
        logger.info(f"Setting up OpenAI model: {self.model_name}")
        
        try:
            # Get OpenAI API key from environment
            api_key = (
                os.getenv("OPENAI_API_KEY")
                or os.getenv("OPENAI_KEY")
            )
            
            if not api_key:
                raise ValueError("OpenAI API key not found in environment variables. "
                               "Please set OPENAI_API_KEY or OPENAI_KEY.")
            
            # Initialize OpenAI chat model
            llm = ChatOpenAI(
                model=self.model_name,
                temperature=0.1,  # Low temperature for consistent SQL generation
                max_tokens=512,
                openai_api_key=api_key,
                model_kwargs={
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0,
                }
            )
            
            logger.info(f"Successfully initialized OpenAI model: {self.model_name}")
            return llm
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI model: {e}")
            raise RuntimeError(f"Could not initialize OpenAI model: {e}")
    
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

User Question: {question}

The examples shown in the example file can also be written in Croatian, so you must account for both languages.
Generate ONLY the SQL query. Do not include any explanation or markdown formatting.

SQL Query:"""
        
        return PromptTemplate(
            input_variables=["table_info", "examples", "question"],
            template=prompt_template
        )
    
    def initialize(self) -> None:
        """Initialize the SQL agent with OpenAI LLM and database connection."""
        logger.info("Initializing Croatian Real Estate SQL Agent...")
        
        try:
            # Setup OpenAI model
            self.llm = self._setup_openai_llm()
            
            # Setup database connection
            self.db = self._setup_database_connection()
            
            # Create SQL query generation chain (Runnable-based API)
            self.sql_chain = create_sql_query_chain(self.llm, self.db)
            
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
            # Generate SQL from the natural language question
            generated_sql = self.sql_chain.invoke({"question": natural_language_query})

            # Sanitize potential markdown/code fences from model output
            parsed_sql = SQLQueryParser().parse(generated_sql)

            # Ensure a reasonable LIMIT if not present
            sql_lower = parsed_sql.lower()
            if sql_lower.strip().startswith("select") and "limit" not in sql_lower:
                if parsed_sql.strip().endswith(";"):
                    parsed_sql = parsed_sql.rstrip(";") + " LIMIT 50;"
                else:
                    parsed_sql = parsed_sql + " LIMIT 50"

            # Execute SQL against the database
            execution_result = self.db.run(parsed_sql)

            # Format response
            response = {
                "success": True,
                "query": natural_language_query,
                "sql_query": parsed_sql,
                "result": execution_result,
                "intermediate_steps": [{"generated_sql": generated_sql}],
                "error": None
            }

            logger.info("Query executed successfully")
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
def create_agent(model_name: str = "gpt-4.1") -> CroatianRealEstateAgent:
    """Create and initialize a Croatian Real Estate SQL Agent with OpenAI."""
    agent = CroatianRealEstateAgent(model_name=model_name)
    agent.initialize()
    return agent

def quick_query(query: str, model_name: str = "gpt-4.1") -> Dict[str, Any]:
    """Execute a quick query without maintaining agent state."""
    agent = create_agent(model_name)
    return agent.query(query)