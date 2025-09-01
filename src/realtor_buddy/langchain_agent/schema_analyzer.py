"""
Croatian Real Estate Schema Analyzer

Main module that provides a unified interface to all schema analysis and mapping
functionality for the LangChain SQL agent implementation.
"""

from .schema_mapping import (
    CROATIAN_TO_ENGLISH_MAPPING,
    ENGLISH_TO_CROATIAN_MAPPING, 
    SCHEMA_DOCUMENTATION,
    QUERY_PATTERNS,
    CROATIAN_VALUE_MAPPINGS,
    get_english_field_name,
    get_croatian_field_name,
    get_field_info,
    translate_croatian_value
)

from .schema_docs import (
    LANGCHAIN_TABLE_INFO,
    SAMPLE_QUERIES,
    CROATIAN_REAL_ESTATE_TERMS,
    CROATIAN_REAL_ESTATE_PROMPT_TEMPLATE,
    DATABASE_CONFIG,
    LANGCHAIN_AGENT_CONFIG,
    get_langchain_table_info,
    get_prompt_template,
    format_sample_queries_for_prompt
)

from .query_patterns import (
    COMMON_QUERY_PATTERNS,
    VALUE_FORMATS,
    CROATIAN_LOCATION_TERMS,
    OPTIMIZATION_PATTERNS,
    QUERY_PARSING_REGEXES,
    extract_price_range,
    extract_location_terms,
    extract_room_count,
    identify_property_type,
    extract_features
)

from .training_examples import (
    TRAINING_EXAMPLES,
    EXAMPLE_CATEGORIES,
    NEGATIVE_EXAMPLES,
    FEW_SHOT_PROMPT_TEMPLATE,
    AGENT_TRAINING_CONFIG,
    get_training_examples_by_category,
    format_examples_for_prompt,
    get_examples_with_concept
)

class SchemaAnalyzer:
    """
    Unified interface for Croatian real estate schema analysis and query generation.
    
    This class provides methods to analyze user queries, map Croatian/English terms,
    and generate appropriate SQL for the LangChain agent.
    """
    
    def __init__(self):
        self.field_mappings = CROATIAN_TO_ENGLISH_MAPPING
        self.value_mappings = CROATIAN_VALUE_MAPPINGS
        self.schema_info = SCHEMA_DOCUMENTATION
        self.query_patterns = COMMON_QUERY_PATTERNS
        
    def analyze_user_query(self, query: str) -> dict:
        """
        Analyze a user's natural language query and extract key components.
        
        Args:
            query: User's search query in English or Croatian
            
        Returns:
            Dictionary containing extracted query components
        """
        analysis = {
            "original_query": query,
            "price_range": extract_price_range(query),
            "locations": extract_location_terms(query),
            "room_count": extract_room_count(query),
            "property_type": identify_property_type(query),
            "features": extract_features(query),
            "suggested_fields": self._suggest_relevant_fields(query)
        }
        
        return analysis
    
    def _suggest_relevant_fields(self, query: str) -> list:
        """Suggest relevant database fields based on query content."""
        query_lower = query.lower()
        relevant_fields = []
        
        # Always include basic fields
        relevant_fields.extend(["id", "title", "price", "lokacija"])
        
        # Add fields based on query content
        if any(term in query_lower for term in ["room", "bedroom", "soba"]):
            relevant_fields.append("broj_soba")
            
        if any(term in query_lower for term in ["area", "size", "sqm", "m²", "square"]):
            relevant_fields.append("povrsina")
            
        if any(term in query_lower for term in ["floor", "ground", "attic", "kat"]):
            relevant_fields.append("kat")
            
        if any(term in query_lower for term in ["sea", "view", "more"]):
            relevant_fields.append("pogled_na_more")
            
        if any(term in query_lower for term in ["elevator", "lift"]):
            relevant_fields.append("lift")
            
        if any(term in query_lower for term in ["parking", "garage"]):
            relevant_fields.append("parking")
            
        if any(term in query_lower for term in ["energy", "rating", "efficiency"]):
            relevant_fields.append("energetski_razred")
            
        return list(set(relevant_fields))  # Remove duplicates
    
    def get_field_mapping(self, field_name: str, direction: str = "croatian_to_english") -> str:
        """
        Get field name mapping between Croatian and English.
        
        Args:
            field_name: Field name to translate
            direction: "croatian_to_english" or "english_to_croatian"
            
        Returns:
            Translated field name or original if no mapping exists
        """
        if direction == "croatian_to_english":
            return get_english_field_name(field_name)
        else:
            return get_croatian_field_name(field_name)
    
    def get_training_examples(self, category: str = None, limit: int = 10) -> list:
        """
        Get training examples for the LangChain agent.
        
        Args:
            category: Optional category filter
            limit: Maximum number of examples to return
            
        Returns:
            List of training examples
        """
        if category:
            examples = get_training_examples_by_category(category)
        else:
            examples = TRAINING_EXAMPLES
            
        return examples[:limit]
    
    def format_for_langchain(self) -> dict:
        """
        Format all schema information for LangChain agent initialization.
        
        Returns:
            Dictionary with all necessary LangChain configuration
        """
        return {
            "table_info": get_langchain_table_info(),
            "prompt_template": get_prompt_template(),
            "sample_queries": format_sample_queries_for_prompt(),
            "database_config": DATABASE_CONFIG,
            "agent_config": LANGCHAIN_AGENT_CONFIG,
            "field_mappings": self.field_mappings,
            "value_mappings": self.value_mappings,
            "training_examples": AGENT_TRAINING_CONFIG["few_shot_examples"]
        }
    
    def validate_query_components(self, analysis: dict) -> dict:
        """
        Validate extracted query components and suggest corrections.
        
        Args:
            analysis: Query analysis from analyze_user_query()
            
        Returns:
            Dictionary with validation results and suggestions
        """
        validation = {
            "valid": True,
            "warnings": [],
            "suggestions": []
        }
        
        # Validate price range
        min_price, max_price = analysis["price_range"]
        if min_price > 0 or max_price < float('inf'):
            if min_price >= max_price and max_price != float('inf'):
                validation["valid"] = False
                validation["warnings"].append("Invalid price range: minimum >= maximum")
            elif max_price > 5000000:  # Very high price
                validation["suggestions"].append("Price seems very high - consider if this is correct")
        
        # Validate locations
        locations = analysis["locations"]
        known_cities = CROATIAN_LOCATION_TERMS["major_cities"]
        for location in locations:
            if location not in known_cities:
                validation["suggestions"].append(f"'{location}' may not be a recognized Croatian city")
        
        # Validate room count
        room_count = analysis["room_count"]
        if room_count and room_count not in ["1", "2", "3", "4", "5+"]:
            validation["warnings"].append(f"Unusual room count: {room_count}")
        
        return validation

# Convenience functions for quick access
def get_schema_analyzer() -> SchemaAnalyzer:
    """Get a configured SchemaAnalyzer instance."""
    return SchemaAnalyzer()

def analyze_query(query: str) -> dict:
    """Quick query analysis using default analyzer."""
    analyzer = SchemaAnalyzer()
    return analyzer.analyze_user_query(query)

def get_langchain_config() -> dict:
    """Get complete LangChain configuration for the Croatian real estate agent."""
    analyzer = SchemaAnalyzer()
    return analyzer.format_for_langchain()

# Export all important components
__all__ = [
    'SchemaAnalyzer',
    'get_schema_analyzer', 
    'analyze_query',
    'get_langchain_config',
    'CROATIAN_TO_ENGLISH_MAPPING',
    'SCHEMA_DOCUMENTATION',
    'TRAINING_EXAMPLES',
    'LANGCHAIN_TABLE_INFO',
    'CROATIAN_REAL_ESTATE_PROMPT_TEMPLATE'
]