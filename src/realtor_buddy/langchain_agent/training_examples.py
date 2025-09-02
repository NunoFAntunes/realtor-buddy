"""
LangChain Agent Training Examples

Comprehensive collection of real-world query examples for training the Croatian real estate
LangChain SQL agent. Includes natural language queries, corresponding SQL, and explanations.
"""

from typing import Dict, List

# Comprehensive training examples for few-shot prompting
TRAINING_EXAMPLES = [
    # Basic location and price searches
    {
        "user_query": "Find apartments in Zagreb under 200,000 euros",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'apartments' 
            AND lokacija LIKE '%Zagreb%' 
            AND price < 200000 
            AND price IS NOT NULL
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Searches for apartments (stan) in Zagreb with price under 200k EUR",
        "key_concepts": ["property_type filtering", "location search", "price range", "NULL handling"]
    },
    
    {
        "user_query": "Show me houses with sea view in Split",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'houses' 
            AND lokacija LIKE '%Split%'
            AND pogled_na_more = 'da'
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Finds houses (kuća) in Split with sea view (pogled_na_more = 'da')",
        "key_concepts": ["property_type", "location", "boolean Croatian values"]
    },
    
    {
        "user_query": "3 bedroom apartments between 100,000 and 300,000 euros",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'apartments'
            AND broj_soba = '3'
            AND price BETWEEN 100000 AND 300000
            AND price IS NOT NULL
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Filters for 3-bedroom apartments in specific price range",
        "key_concepts": ["room count as string", "price range", "BETWEEN operator"]
    },
    
    # Area and size-based searches
    {
        "user_query": "Large apartments over 100 square meters in Zagreb",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'apartments'
            AND lokacija LIKE '%Zagreb%'
            AND CAST(povrsina AS UNSIGNED) > 100
            AND povrsina IS NOT NULL
            ORDER BY CAST(povrsina AS UNSIGNED) DESC
            LIMIT 20
        """,
        "explanation": "Finds large apartments by casting area string to number for comparison",
        "key_concepts": ["area casting", "VARCHAR to numeric conversion", "size filtering"]
    },
    
    {
        "user_query": "Small properties under 60 sqm with parking",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE CAST(povrsina AS UNSIGNED) < 60
            AND povrsina IS NOT NULL
            AND JSON_LENGTH(parking) > 0
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Searches for small properties with parking using JSON field check",
        "key_concepts": ["area comparison", "JSON field querying", "parking availability"]
    },
    
    # Feature-based searches
    {
        "user_query": "Properties with elevator and parking in city center",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE lift = 'da'
            AND JSON_LENGTH(parking) > 0
            AND (lokacija LIKE '%centar%' OR lokacija LIKE '%center%')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Combines elevator, parking, and city center location filters",
        "key_concepts": ["multiple feature filtering", "JSON parking check", "location variants"]
    },
    
    {
        "user_query": "Ground floor apartments with balcony",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'apartments'
            AND kat = 'prizemlje'
            AND balkon_lodza_terasa IS NOT NULL
            AND balkon_lodza_terasa != 'Nema ništa navedeno'
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Finds ground floor apartments with balcony/terrace features",
        "key_concepts": ["floor level Croatian terms", "feature availability", "empty string handling"]
    },
    
    # New construction and modern properties
    {
        "user_query": "New construction from 2020 onwards with high energy rating",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE CAST(godina_izgradnje AS UNSIGNED) >= 2020
            AND energetski_razred IN ('A+', 'A', 'B')
            AND godina_izgradnje IS NOT NULL
            ORDER BY godina_izgradnje DESC, price ASC
            LIMIT 20
        """,
        "explanation": "Filters for recent construction with excellent energy efficiency",
        "key_concepts": ["year filtering with casting", "energy rating values", "multiple sorting"]
    },
    
    {
        "user_query": "Recently renovated properties after 2015",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE CAST(godina_zadnje_renovacije AS UNSIGNED) > 2015
            AND godina_zadnje_renovacije IS NOT NULL
            ORDER BY godina_zadnje_renovacije DESC
            LIMIT 20
        """,
        "explanation": "Searches for properties renovated after 2015",
        "key_concepts": ["renovation year filtering", "date casting", "recent updates"]
    },
    
    # Luxury and high-end searches
    {
        "user_query": "Expensive properties over 500k euros",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE price > 500000
            ORDER BY price DESC
            LIMIT 20
        """,
        "explanation": "Lists luxury properties ordered by price descending",
        "key_concepts": ["high-end filtering", "descending sort", "luxury market"]
    },
    
    {
        "user_query": "Penthouses and attic apartments with sea view",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'apartments'
            AND kat = 'potkrovlje'
            AND pogled_na_more = 'da'
            ORDER BY price DESC
            LIMIT 20
        """,
        "explanation": "Finds penthouse/attic apartments with sea view",
        "key_concepts": ["floor level terminology", "premium locations", "luxury features"]
    },
    
    # Location-specific and regional searches
    {
        "user_query": "Seaside properties near the beach under 400k",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE price < 400000
            AND price IS NOT NULL
            AND (lokacija LIKE '%more%' OR lokacija LIKE '%plaža%' OR 
                 lokacija LIKE '%obala%' OR pogled_na_more = 'da')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Searches for coastal properties using multiple location indicators",
        "key_concepts": ["multiple location terms", "coastal indicators", "OR conditions"]
    },
    
    {
        "user_query": "Properties in Dubrovnik old town area",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE lokacija LIKE '%Dubrovnik%'
            AND (lokacija LIKE '%stari grad%' OR lokacija LIKE '%old town%')
            ORDER BY price DESC
            LIMIT 20
        """,
        "explanation": "Finds properties in historic Dubrovnik old town",
        "key_concepts": ["specific city", "historic areas", "multilingual terms"]
    },
    
    # Commercial and investment properties
    {
        "user_query": "Commercial spaces for rent in Zagreb center",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'commercial_real_estate'
            AND lokacija LIKE '%Zagreb%'
            AND (lokacija LIKE '%centar%' OR lokacija LIKE '%center%')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Searches for commercial properties in Zagreb city center",
        "key_concepts": ["commercial property types", "business locations", "rental market"]
    },
    
    {
        "user_query": "Investment properties with good rental potential",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE agency_type = 'investitor'
            AND price IS NOT NULL
            AND (lokacija LIKE '%centar%' OR lokacija LIKE '%more%')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Finds investment properties from investors in prime locations (using Croatian agency_type)",
        "key_concepts": ["agency type filtering", "investment focus", "prime locations"]
    },
    
    # Specific amenity searches
    {
        "user_query": "Properties with central heating and AC",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE JSON_CONTAINS(grijanje, '"centralno grijanje"')
            OR grijanje LIKE '%centralno%'
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Searches for properties with central heating using JSON field",
        "key_concepts": ["JSON field searching", "heating systems", "comfort features"]
    },
    
    {
        "user_query": "Pet-friendly apartments with yard space",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'apartments'
            AND (povrsina_okucnice IS NOT NULL OR 
                 JSON_LENGTH(ostali_objekti_i_povrsine) > 0)
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Finds apartments with outdoor space for pets",
        "key_concepts": ["yard area", "pet-friendly features", "outdoor space"]
    },
    
    # Budget-conscious searches
    {
        "user_query": "Affordable starter homes under 80k euros",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE price < 80000
            AND price IS NOT NULL
            AND (property_type = 'apartments' OR property_type = 'houses')
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Budget search for affordable residential properties",
        "key_concepts": ["budget filtering", "starter properties", "multiple property types"]
    },
    
    {
        "user_query": "Properties requiring renovation under 100k",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE price < 100000
            AND price IS NOT NULL
            AND (namjestenost_i_stanje LIKE '%renovacija%' OR 
                 namjestenost_i_stanje LIKE '%adaptacija%' OR
                 godina_zadnje_renovacije IS NULL)
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Finds fixer-upper properties needing renovation work",
        "key_concepts": ["renovation needed", "property condition", "investment opportunities"]
    },
    
    # Luxury and commercial property examples
    {
        "user_query": "Luxury properties with premium features over 300k",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'luxury_properties'
            AND price > 300000
            AND price IS NOT NULL
            ORDER BY price DESC
            LIMIT 20
        """,
        "explanation": "Searches for luxury properties using English property_type value",
        "key_concepts": ["luxury property type", "premium filtering", "high-end market"]
    },
    
    {
        "user_query": "Commercial land for development projects",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'commercial_land'
            AND price IS NOT NULL
            ORDER BY CAST(povrsina AS UNSIGNED) DESC
            LIMIT 20
        """,
        "explanation": "Finds commercial land using specific English property_type",
        "key_concepts": ["commercial land type", "development potential", "area sorting"]
    },
    
    # Complex multi-criteria searches
    {
        "user_query": "4+ bedroom houses in Split with garden and parking under 600k",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'houses'
            AND lokacija LIKE '%Split%'
            AND (broj_soba IN ('4', '5+') OR CAST(broj_soba AS UNSIGNED) >= 4)
            AND povrsina_okucnice IS NOT NULL
            AND JSON_LENGTH(parking) > 0
            AND price < 600000
            AND price IS NOT NULL
            ORDER BY price ASC
            LIMIT 20
        """,
        "explanation": "Complex search combining multiple criteria for family homes",
        "key_concepts": ["multiple room criteria", "garden space", "family requirements", "complex filtering"]
    },
    
    {
        "user_query": "Modern apartments from 2018+ with elevator, A/B energy rating, and balcony in Zagreb",
        "sql_query": """
            SELECT *
            FROM agency_properties 
            WHERE property_type = 'apartments'
            AND lokacija LIKE '%Zagreb%'
            AND CAST(godina_izgradnje AS UNSIGNED) >= 2018
            AND lift = 'da'
            AND energetski_razred IN ('A+', 'A', 'B')
            AND (balkon_lodza_terasa LIKE '%Balkon%' OR balkon_lodza_terasa LIKE '%Terasa%' OR balkon_lodza_terasa LIKE '%Lođa%')
            ORDER BY godina_izgradnje DESC, price ASC
            LIMIT 20
        """,
        "explanation": "Premium modern apartments with multiple high-end features",
        "key_concepts": ["modern construction", "multiple premium features", "energy efficiency", "comprehensive filtering"]
    }
]

# Categorized examples for different use cases
EXAMPLE_CATEGORIES = {
    "basic_searches": [
        "Find apartments in Zagreb under 200,000 euros",
        "Show me houses with sea view in Split", 
        "3 bedroom apartments between 100,000 and 300,000 euros"
    ],
    
    "feature_based": [
        "Properties with elevator and parking in city center",
        "Ground floor apartments with balcony",
        "Properties with central heating and AC"
    ],
    
    "location_specific": [
        "Seaside properties near the beach under 400k",
        "Properties in Dubrovnik old town area",
        "Commercial spaces for rent in Zagreb center"
    ],
    
    "luxury_high_end": [
        "Expensive properties over 500k euros",
        "Penthouses and attic apartments with sea view",
        "Luxury properties with premium features over 300k"
    ],
    
    "commercial_properties": [
        "Commercial spaces for rent in Zagreb center",
        "Investment properties with good rental potential",
        "Commercial land for development projects"
    ],
    
    "budget_conscious": [
        "Affordable starter homes under 80k euros",
        "Properties requiring renovation under 100k"
    ],
    
    "complex_criteria": [
        "4+ bedroom houses in Split with garden and parking under 600k",
        "Modern apartments from 2018+ with elevator, A/B energy rating, and balcony in Zagreb"
    ]
}

# Negative examples (what NOT to do)
NEGATIVE_EXAMPLES = [
    {
        "bad_query": "SELECT * FROM agency_properties WHERE lokacija = 'Zagreb'",
        "problem": "Exact match on location field - should use LIKE '%Zagreb%'",
        "better_query": "SELECT * FROM agency_properties WHERE lokacija LIKE '%Zagreb%'"
    },
    
    {
        "bad_query": "SELECT * FROM agency_properties WHERE povrsina > 100",
        "problem": "Comparing VARCHAR field as number without casting",
        "better_query": "SELECT * FROM agency_properties WHERE CAST(povrsina AS UNSIGNED) > 100"
    },
    
    {
        "bad_query": "SELECT * FROM agency_properties WHERE lift = 'yes'",
        "problem": "Using English value instead of Croatian 'da'",
        "better_query": "SELECT * FROM agency_properties WHERE lift = 'da'"
    },
    
    {
        "bad_query": "SELECT * FROM agency_properties WHERE price > 100000",
        "problem": "Not handling NULL prices",
        "better_query": "SELECT * FROM agency_properties WHERE price > 100000 AND price IS NOT NULL"
    }
]

# Few-shot prompting template
FEW_SHOT_PROMPT_TEMPLATE = """
You are an expert SQL agent for Croatian real estate data. Here are examples of how to convert natural language queries to SQL:

{examples}

Now generate a SQL query for this request: {user_question}
"""

def get_training_examples_by_category(category: str) -> List[Dict]:
    """Get training examples filtered by category."""
    if category not in EXAMPLE_CATEGORIES:
        return TRAINING_EXAMPLES
    
    category_queries = EXAMPLE_CATEGORIES[category]
    return [ex for ex in TRAINING_EXAMPLES if ex["user_query"] in category_queries]

def format_examples_for_prompt(num_examples: int = 5) -> str:
    """Format training examples for few-shot prompting."""
    examples = TRAINING_EXAMPLES[:num_examples]
    formatted = []
    
    for i, example in enumerate(examples, 1):
        formatted.append(f"Example {i}:")
        formatted.append(f"Question: {example['user_query']}")
        formatted.append(f"SQL: {example['sql_query'].strip()}")
        formatted.append("")
    
    return "\n".join(formatted)

def get_examples_with_concept(concept: str) -> List[Dict]:
    """Get examples that demonstrate a specific concept."""
    return [ex for ex in TRAINING_EXAMPLES if concept in ex.get("key_concepts", [])]

# Template for agent configuration with examples
AGENT_TRAINING_CONFIG = {
    "few_shot_examples": TRAINING_EXAMPLES[:10],  # Top 10 examples
    "negative_examples": NEGATIVE_EXAMPLES,
    "prompt_template": FEW_SHOT_PROMPT_TEMPLATE,
    "validation_queries": EXAMPLE_CATEGORIES["basic_searches"]
}