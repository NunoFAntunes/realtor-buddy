"""
LangChain SQL Agent Schema Documentation

This module provides structured schema information specifically formatted for LangChain SQL agents,
including table descriptions, sample queries, and prompt templates for Croatian real estate data.
"""

from typing import Dict, List

# Table schema description for LangChain
LANGCHAIN_TABLE_INFO = """
Table: agency_properties
Description: Comprehensive Croatian real estate properties database containing listings from various agencies

Key Columns:
- id (PRIMARY KEY): Unique property identifier
- price (DECIMAL): Property price in EUR (indexed for fast filtering)  
- lokacija (VARCHAR): Location/address in Croatian (indexed, use LIKE for partial matches)
- property_type (VARCHAR): General property type (stan=apartment, kuća=house, etc.)
- agency_name (VARCHAR): Real estate agency name (indexed)

Property Details:
- broj_soba (VARCHAR): Number of bedrooms/rooms ("1", "2", "3", "4", "5+")
- povrsina (VARCHAR): Surface area in m² (numbers as strings, e.g. "85", "120")
- kat (VARCHAR): Floor ("prizemlje"=ground, "1"=1st floor, "potkrovlje"=attic)
- lift (VARCHAR): Elevator ("da"=yes, "ne"=no)
- pogled_na_more (VARCHAR): Sea view ("da"=yes, "ne"=no)
- energetski_razred (VARCHAR): Energy rating ("A+", "A", "B", "C", "D", "E", "F", "G")

Location Data:
- latitude/longitude (DECIMAL): GPS coordinates for location-based searches
- ulica (VARCHAR): Street address

Timestamps:
- created_at (TIMESTAMP): When record was added (indexed)
- time_posted (TIMESTAMP): When listing was posted

JSON Fields (use JSON_EXTRACT for querying):
- parking: Parking options and types
- grijanje: Heating systems  
- komunalije: Utilities information

Important Notes:
- Many fields contain Croatian values - refer to value mappings
- Numeric fields like povrsina are stored as VARCHAR, convert for numeric comparisons
- Use LIKE '%term%' for partial text matches on location fields
- Price filtering should use numeric comparisons on the price DECIMAL field
"""

# Sample queries for LangChain training
SAMPLE_QUERIES = [
    {
        "english_query": "Find apartments in Zagreb under 200,000 euros",
        "sql_query": """
            SELECT id, title, price, lokacija, broj_soba, povrsina 
            FROM agency_properties 
            WHERE property_type LIKE '%stan%' 
            AND lokacija LIKE '%Zagreb%' 
            AND price < 200000 
            AND price IS NOT NULL
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Filters for apartments (stan) in Zagreb under 200k EUR, ordered by price ascending"
    },
    {
        "english_query": "Show me houses with sea view in Split",
        "sql_query": """
            SELECT id, title, price, lokacija, pogled_na_more, povrsina
            FROM agency_properties 
            WHERE property_type LIKE '%kuća%' 
            AND lokacija LIKE '%Split%'
            AND pogled_na_more = 'da'
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Searches for houses (kuća) in Split with sea view (pogled_na_more = 'da')"
    },
    {
        "english_query": "Properties with parking and elevator in city center",
        "sql_query": """
            SELECT id, title, price, lokacija, lift, parking
            FROM agency_properties 
            WHERE lift = 'da'
            AND JSON_LENGTH(parking) > 0
            AND (lokacija LIKE '%centar%' OR lokacija LIKE '%center%')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Finds properties with elevator (lift='da') and parking (JSON field not empty) in city center"
    },
    {
        "english_query": "3 bedroom apartments between 100-150k euros with energy rating A or B",
        "sql_query": """
            SELECT id, title, price, lokacija, broj_soba, energetski_razred, povrsina
            FROM agency_properties 
            WHERE property_type LIKE '%stan%'
            AND broj_soba = '3'
            AND price BETWEEN 100000 AND 150000
            AND energetski_razred IN ('A+', 'A', 'B')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Filters apartments with 3 bedrooms, price range, and high energy efficiency"
    },
    {
        "english_query": "New constructions from 2020 onwards with 100+ sqm",
        "sql_query": """
            SELECT id, title, price, lokacija, godina_izgradnje, povrsina
            FROM agency_properties 
            WHERE CAST(godina_izgradnje AS UNSIGNED) >= 2020
            AND CAST(povrsina AS UNSIGNED) >= 100
            AND godina_izgradnje IS NOT NULL
            AND povrsina IS NOT NULL
            ORDER BY godina_izgradnje DESC, price ASC
            LIMIT 20
        """,
        "explanation": "Finds properties built from 2020+ with 100+ sqm area (casting VARCHAR to numeric)"
    },
    {
        "english_query": "Properties near the sea with prices under 300k",
        "sql_query": """
            SELECT id, title, price, lokacija, pogled_na_more, povrsina
            FROM agency_properties 
            WHERE price < 300000
            AND price IS NOT NULL
            AND (lokacija LIKE '%more%' OR pogled_na_more = 'da' OR lokacija LIKE '%obala%')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Searches for seaside properties using location keywords and sea view indicator"
    },
    {
        "english_query": "Ground floor apartments with parking",
        "sql_query": """
            SELECT id, title, price, lokacija, kat, parking
            FROM agency_properties 
            WHERE property_type LIKE '%stan%'
            AND kat = 'prizemlje'
            AND JSON_LENGTH(parking) > 0
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Finds ground floor (prizemlje) apartments with parking facilities"
    },
    {
        "english_query": "Show expensive properties over 500k euros",
        "sql_query": """
            SELECT id, title, price, lokacija, povrsina, property_type
            FROM agency_properties 
            WHERE price > 500000
            ORDER BY price DESC
            LIMIT 20
        """,
        "explanation": "Lists high-end properties above 500k EUR ordered by price descending"
    }
]

# Croatian real estate terminology for LangChain prompts
CROATIAN_REAL_ESTATE_TERMS = {
    "property_types": {
        "apartment": ["stan", "apartman"],
        "house": ["kuća", "vila"],
        "commercial": ["poslovni prostor", "lokal", "ured"],
        "land": ["zemljište", "parcela"],
        "garage": ["garaža", "parking"]
    },
    "locations": {
        "city_center": ["centar", "center", "središte"],
        "seaside": ["more", "obala", "plaža", "primorje"],
        "near_transport": ["tramvaj", "autobusna stanica", "željeznička"]
    },
    "features": {
        "sea_view": ["pogled na more", "sea view"],
        "elevator": ["lift", "dizalo"],
        "parking": ["parking", "garaža", "parkirno mjesto"],
        "balcony": ["balkon", "terasa", "lodža"],
        "heating": ["grijanje", "centralno grijanje"],
        "furnished": ["namješten", "opremljen"]
    },
    "floor_terms": {
        "ground_floor": ["prizemlje", "ground floor"],
        "first_floor": ["prvi kat", "1. kat"],
        "attic": ["potkrovlje", "tavanski"],
        "basement": ["podrum", "suteren"]
    }
}

# Prompt template for Croatian real estate queries
CROATIAN_REAL_ESTATE_PROMPT_TEMPLATE = """
You are a SQL expert helping users search Croatian real estate data. The database contains property listings with both Croatian and English field names.

Database Schema:
{table_info}

Important Croatian Terms:
- stan = apartment, kuća = house
- lokacija = location (use LIKE '%term%' for city searches)
- broj_soba = number of bedrooms 
- povrsina = surface area (in m²)
- kat = floor (prizemlje=ground, numbers=upper floors)
- lift = elevator (da=yes, ne=no)
- pogled_na_more = sea view (da=yes, ne=no)
- price = price in EUR (use numeric comparisons)

Query Guidelines:
1. Always use LIKE '%term%' for location searches
2. Property types: use LIKE '%stan%' for apartments, LIKE '%kuća%' for houses
3. Numeric fields like povrsina are stored as VARCHAR - cast if needed
4. Boolean Croatian values: "da" = yes, "ne" = no
5. Always add reasonable LIMIT (max 50 results)
6. Handle NULL values appropriately
7. For JSON fields like parking, use JSON_LENGTH() > 0 to check existence

Sample Queries:
{sample_queries}

User Question: {question}

Generate a SQL query to answer this question. Only return the SQL query, no explanation.
"""

# Field validation patterns
FIELD_VALIDATION_PATTERNS = {
    "price_range": r"(\d+)[-–to](\d+)",
    "area_range": r"(\d+)[-–to](\d+)\s*(?:m²|sqm|square|meters)",
    "room_count": r"(\d+)\s*(?:bedroom|room|soba)",
    "year_range": r"(?:from\s+|after\s+|since\s+)?(\d{4})",
    "location_terms": r"(?:in\s+|near\s+)?([A-Za-z\s]+?)(?:\s+(?:city|area|region))?",
    "property_type": r"(?:apartment|house|commercial|land|kuća|stan)",
    "features": r"(?:sea view|elevator|parking|balcony|lift|more|garaža)"
}

def format_sample_queries_for_prompt() -> str:
    """Format sample queries for inclusion in prompts."""
    formatted = []
    for i, query in enumerate(SAMPLE_QUERIES[:5], 1):  # Use first 5 samples
        formatted.append(f"{i}. Question: {query['english_query']}")
        formatted.append(f"   SQL: {query['sql_query'].strip()}")
        formatted.append("")
    return "\n".join(formatted)

def get_langchain_table_info() -> dict:
    """Get formatted table information for LangChain SQL agents."""
    return {"agency_properties": LANGCHAIN_TABLE_INFO}

def get_prompt_template() -> str:
    """Get the complete prompt template for Croatian real estate queries."""
    return CROATIAN_REAL_ESTATE_PROMPT_TEMPLATE

# Database connection info for LangChain
DATABASE_CONFIG = {
    "dialect": "mysql",
    "driver": "pymysql",
    "database": "njuskam_ultimate3",
    "table": "agency_properties",
    "connection_template": "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
}

# LangChain agent configuration
LANGCHAIN_AGENT_CONFIG = {
    "verbose": True,
    "return_intermediate_steps": True,
    "max_iterations": 5,
    "early_stopping_method": "generate",
    "handle_parsing_errors": True,
    "top_k": 20,  # Default result limit
    "sample_rows_in_table_info": 3
}