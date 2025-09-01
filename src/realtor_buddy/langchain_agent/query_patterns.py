"""
Croatian Real Estate Query Patterns and Value Formats

This module documents common query patterns, expected value formats, and search strategies
for Croatian real estate data to help LangChain agents generate effective SQL queries.
"""

from typing import Dict, List, Tuple, Pattern
import re

# Common search patterns users might employ
COMMON_QUERY_PATTERNS = {
    "location_based": {
        "description": "Search by city, neighborhood, or general area",
        "user_examples": [
            "apartments in Zagreb",
            "houses near Split", 
            "properties in city center",
            "seaside properties",
            "downtown area"
        ],
        "sql_pattern": "lokacija LIKE '%{location}%'",
        "fields_used": ["lokacija", "ulica"],
        "notes": "Use LIKE with wildcards for flexible location matching"
    },
    
    "price_filtering": {
        "description": "Filter properties by price or price range",
        "user_examples": [
            "under 200000 euros",
            "between 100k and 300k",
            "budget under 150000",
            "expensive properties over 500k",
            "properties from 50000 to 200000"
        ],
        "sql_pattern": "price BETWEEN {min_price} AND {max_price}",
        "fields_used": ["price"],
        "value_format": "Decimal numbers (EUR)",
        "notes": "Always include 'price IS NOT NULL' to filter out listings without price"
    },
    
    "property_size": {
        "description": "Search by property area/size",
        "user_examples": [
            "apartments over 80 square meters",
            "houses with 100+ sqm",
            "small apartments under 60m²",
            "large properties 200+ square meters"
        ],
        "sql_pattern": "CAST(povrsina AS UNSIGNED) >= {min_area}",
        "fields_used": ["povrsina", "stambena_povrsina", "netto_povrsina"],
        "value_format": "Numbers as strings (need to cast for numeric comparison)",
        "notes": "Area stored as VARCHAR, cast to UNSIGNED for numeric comparisons"
    },
    
    "room_count": {
        "description": "Filter by number of bedrooms/rooms",
        "user_examples": [
            "3 bedroom apartments",
            "2 room properties",
            "studio apartments",
            "4+ bedrooms"
        ],
        "sql_pattern": "broj_soba = '{room_count}'",
        "fields_used": ["broj_soba", "broj_prostorija"],
        "value_format": "String numbers ('1', '2', '3', '4', '5+') ",
        "common_values": ["1", "2", "3", "4", "5+"]
    },
    
    "property_type": {
        "description": "Filter by specific property types",
        "user_examples": [
            "apartments only",
            "houses for sale",
            "commercial properties",
            "land/plots",
            "luxury properties"
        ],
        "sql_pattern": "property_type IN ('{types}')",
        "fields_used": ["property_type", "tip_nekretnine"],
        "english_values": [
            "apartments",
            "houses", 
            "commercial_land",
            "commercial_real_estate",
            "luxury_properties"
        ],
        "value_mappings": {
            "apartment": ["apartments", "stan"],
            "house": ["houses", "kuća"], 
            "commercial": ["commercial_real_estate", "commercial_land", "poslovni prostor"],
            "land": ["commercial_land", "zemljište"],
            "luxury": ["luxury_properties", "luksuzne nekretnine"]
        }
    },
    
    "floor_level": {
        "description": "Search by floor number or level",
        "user_examples": [
            "ground floor apartments",
            "upper floors only",
            "penthouse/attic",
            "first floor"
        ],
        "sql_pattern": "kat = '{floor_value}'",
        "fields_used": ["kat"],
        "value_mappings": {
            "ground floor": "prizemlje",
            "attic": "potkrovlje", 
            "basement": "podrum",
            "first floor": "1",
            "second floor": "2"
        }
    },
    
    "agency_type": {
        "description": "Filter by agency type",
        "user_examples": [
            "properties from agencies",
            "direct from owner",
            "investor properties"
        ],
        "sql_pattern": "agency_type = '{type}'",
        "fields_used": ["agency_type"],
        "valid_values": ["agencija", "investitor", "trgovina"],
        "value_mappings": {
            "agency": "agencija",
            "investor": "investitor", 
            "shop": "trgovina",
            "direct": "investitor"
        }
    },
    
    "amenities_features": {
        "description": "Search by property features and amenities",
        "user_examples": [
            "properties with elevator",
            "sea view apartments", 
            "parking included",
            "with balcony",
            "with terrace",
            "with loggia"
        ],
        "sql_patterns": {
            "elevator": "lift = 'da'",
            "sea_view": "pogled_na_more = 'da'",
            "parking": "JSON_LENGTH(parking) > 0",
            "balcony": "balkon_lodza_terasa LIKE '%Balkon%'",
            "terrace": "balkon_lodza_terasa LIKE '%Terasa%'",
            "loggia": "balkon_lodza_terasa LIKE '%Lođa%'"
        },
        "boolean_fields": ["lift", "pogled_na_more"],
        "json_fields": ["parking", "grijanje"]
    },
    
    "construction_year": {
        "description": "Filter by construction or renovation year",
        "user_examples": [
            "new construction from 2020",
            "recently built properties",
            "older buildings before 2000",
            "renovated after 2015"
        ],
        "sql_pattern": "CAST(godina_izgradnje AS UNSIGNED) >= {year}",
        "fields_used": ["godina_izgradnje", "godina_zadnje_renovacije"],
        "value_format": "Year as string, cast to number for comparisons"
    },
    
    "energy_efficiency": {
        "description": "Search by energy rating",
        "user_examples": [
            "high energy efficiency",
            "A or B rated properties",
            "green buildings"
        ],
        "sql_pattern": "energetski_razred IN ('A+', 'A', 'B')",
        "fields_used": ["energetski_razred"],
        "value_range": ["A+", "A", "B", "C", "D", "E", "F", "G"]
    }
}

# Expected value formats for different field types
VALUE_FORMATS = {
    "balkon_lodza_terasa": {
        "data_type": "VARCHAR(200)",
        "format": "Comma-separated Croatian outdoor space types",
        "valid_values": [
            "Balkon",
            "Lođa (Loggia)", 
            "Terasa",
            "Terasa, Balkon",
            "Terasa, Lođa (Loggia), Balkon",
            "Lođa (Loggia), Balkon",
            "Terasa, Lođa (Loggia)",
            "Balkon, Terasa",
            "Lođa (Loggia), Terasa",
            "Balkon, Lođa (Loggia)",
            "Balkon, Lođa (Loggia), Terasa",
            "Nema ništa navedeno",
            None
        ],
        "search_patterns": {
            "balcony": "LIKE '%Balkon%'",
            "terrace": "LIKE '%Terasa%'",
            "loggia": "LIKE '%Lođa%'",
            "any_outdoor": "IS NOT NULL AND != 'Nema ništa navedeno'"
        }
    },
    
    "broj_etaza": {
        "data_type": "VARCHAR(100)",
        "format": "Croatian building floor descriptions",
        "valid_values": [
            "Jednoetažni",    # Single-story
            "Dvoetažni",      # Two-story  
            "Višeetažni",     # Multi-story
            "Prizemnica",     # Ground level house
            "Visoka prizemnica", # High ground level
            "Katnica",        # House with floors
            "Višekatnica",    # Multi-floor house
            "Dvokatnica",     # Two-floor house
            None
        ],
        "search_patterns": {
            "single_story": "= 'Jednoetažni' OR = 'Prizemnica'",
            "multi_story": "LIKE '%višeet%' OR LIKE '%višekat%'",
            "two_story": "= 'Dvoetažni' OR = 'Dvokatnica'"
        }
    },
    
    "broj_parkirnih_mjesta": {
        "data_type": "VARCHAR(100)",
        "format": "Parking space count or description",
        "valid_values": [
            "1", "2", "3", "4", "5", "6", "7", "7+",
            "nema vlastito parkirno mjesto",
            None
        ],
        "search_patterns": {
            "has_parking": "IS NOT NULL AND != 'nema vlastito parkirno mjesto'",
            "no_parking": "= 'nema vlastito parkirno mjesto' OR IS NULL",
            "multiple_spaces": "IN ('2', '3', '4', '5', '6', '7', '7+')"
        }
    },
    "price": {
        "data_type": "DECIMAL(12,2)",
        "format": "Numeric (EUR currency)",
        "range": "Typically 20,000 - 2,000,000",
        "null_handling": "Always check 'IS NOT NULL'",
        "examples": [50000, 150000.50, 750000]
    },
    
    "povrsina": {
        "data_type": "VARCHAR(100)", 
        "format": "Area in square meters as string",
        "casting": "CAST(povrsina AS UNSIGNED) for numeric operations",
        "range": "Typically 20-500 for residential",
        "examples": ["45", "85.5", "120", "200"]
    },
    
    "broj_soba": {
        "data_type": "VARCHAR(100)",
        "format": "Room count as string",
        "common_values": ["1", "2", "3", "4", "5+"],
        "special_cases": ["5+", "više od 5"],
        "examples": ["1", "2", "3", "4", "5+"]
    },
    
    "lokacija": {
        "data_type": "VARCHAR(500)",
        "format": "Free text location description in Croatian",
        "search_strategy": "Use LIKE '%term%' for partial matching",
        "common_cities": ["Zagreb", "Split", "Rijeka", "Osijek", "Zadar"],
        "examples": [
            "Zagreb, Gornji Grad",
            "Split, Marjan", 
            "Rijeka, Centar",
            "Dubrovnik, Stari Grad"
        ]
    },
    
    "kat": {
        "data_type": "VARCHAR(100)",
        "format": "Floor level in Croatian",
        "special_values": {
            "prizemlje": "Ground floor",
            "potkrovlje": "Attic/penthouse",
            "podrum": "Basement"
        },
        "numeric_floors": ["1", "2", "3", "4", "5+"],
        "examples": ["prizemlje", "1", "2", "potkrovlje"]
    },
    
    "boolean_croatian": {
        "data_type": "VARCHAR(50)",
        "format": "Croatian yes/no values",
        "values": {"da": "yes", "ne": "no"},
        "applicable_fields": ["lift", "pogled_na_more"],
        "examples": ["da", "ne"]
    },
    
    "json_fields": {
        "data_type": "LONGTEXT (JSON)",
        "format": "JSON arrays or objects",
        "query_method": "Use JSON functions like JSON_LENGTH(), JSON_EXTRACT()",
        "applicable_fields": ["parking", "grijanje", "komunalije"],
        "examples": [
            '["garažno mjesto", "vanjsko"]',
            '["centralno grijanje"]'
        ]
    }
}

# Location-specific search terms
CROATIAN_LOCATION_TERMS = {
    "major_cities": [
        "Zagreb", "Split", "Rijeka", "Osijek", "Zadar", "Slavonski Brod",
        "Pula", "Karlovac", "Sisak", "Šibenik", "Dubrovnik", "Bjelovar"
    ],
    
    "neighborhood_indicators": [
        "centar", "center", "središte",  # city center
        "stari grad",  # old town
        "novi grad",   # new town  
        "gornji grad", "donji grad",  # upper/lower town
        "trešnjevka", "maksimir",  # Zagreb neighborhoods
        "marjan", "meje",  # Split neighborhoods
        "trsat", "pecine"  # Rijeka neighborhoods
    ],
    
    "proximity_terms": [
        "blizu", "near", "kod", "pokraj",  # near/close to
        "centar", "more", "plaža",  # center, sea, beach
        "tramvaj", "autobusna stanica",  # transport
        "škola", "bolnica", "trgovina"  # amenities
    ]
}

# Query optimization patterns
OPTIMIZATION_PATTERNS = {
    "indexed_fields": {
        "description": "Fields with database indexes for faster queries",
        "fields": ["price", "lokacija", "agency_name", "property_type", "created_at"],
        "usage": "Prefer these fields in WHERE clauses for better performance"
    },
    
    "limit_results": {
        "description": "Always limit query results",
        "recommended_limits": {
            "default": 20,
            "list_view": 50,
            "export": 1000,
            "maximum": 5000
        },
        "sql_pattern": "LIMIT {limit}"
    },
    
    "null_handling": {
        "description": "Handle NULL values appropriately",
        "critical_fields": ["price", "lokacija", "povrsina"],
        "sql_patterns": [
            "price IS NOT NULL",
            "lokacija IS NOT NULL AND lokacija != ''",
            "povrsina IS NOT NULL AND povrsina != ''"
        ]
    },
    
    "text_search": {
        "description": "Efficient text search patterns",
        "patterns": [
            "lokacija LIKE '%{term}%'",  # partial match
            "title LIKE '%{term}%'",     # title search
            "MATCH(description) AGAINST('{term}')"  # full-text if available
        ]
    }
}

# Regular expressions for parsing user queries
QUERY_PARSING_REGEXES = {
    "price_range": [
        r"(?:under|below|less than)\s+(\d+(?:,\d{3})*(?:\.\d{2})?)",
        r"(?:over|above|more than)\s+(\d+(?:,\d{3})*(?:\.\d{2})?)",
        r"between\s+(\d+(?:,\d{3})*)\s+and\s+(\d+(?:,\d{3})*)",
        r"(\d+(?:,\d{3})*)\s*[-–to]\s*(\d+(?:,\d{3})*)",
        r"budget\s+(\d+(?:,\d{3})*)"
    ],
    
    "area_size": [
        r"(\d+)\+?\s*(?:m²|sqm|square meters?)",
        r"(?:over|above)\s+(\d+)\s*(?:m²|sqm)",
        r"(\d+)\s*[-–to]\s*(\d+)\s*(?:m²|sqm)"
    ],
    
    "room_count": [
        r"(\d+)\s*(?:bedroom|bed|room|soba)",
        r"(\d+)\+?\s*rooms?",
        r"studio|garsonijera"  # 1 room
    ],
    
    "location": [
        r"(?:in|at|near)\s+([A-Za-zšđčćžŠĐČĆŽ\s]+?)(?:\s|,|$)",
        r"([A-Za-zšđčćžŠĐČĆŽ\s]+?)\s+(?:area|region|city)",
        r"city\s+center|centar|centre"
    ],
    
    "property_type": [
        r"apartment|stan|apartman",
        r"house|kuća|vila", 
        r"commercial|poslovni prostor",
        r"land|zemljište|parcela",
        r"luxury|luksuz"
    ],
    
    "features": [
        r"sea view|pogled na more|more",
        r"elevator|lift|dizalo",
        r"parking|garaža",
        r"balcony|balkon|terasa"
    ]
}

def extract_price_range(query: str) -> Tuple[float, float]:
    """
    Extract price range from user query.
    
    Args:
        query: User's search query
        
    Returns:
        Tuple of (min_price, max_price) or (0, float('inf')) if not found
    """
    query_lower = query.lower()
    
    # Check for "under/below" patterns
    under_patterns = [r"(?:under|below|less than)\s+(\d+(?:,\d{3})*(?:k|000)?)"]
    for pattern in under_patterns:
        match = re.search(pattern, query_lower)
        if match:
            price = parse_price_value(match.group(1))
            return (0, price)
    
    # Check for "over/above" patterns  
    over_patterns = [r"(?:over|above|more than)\s+(\d+(?:,\d{3})*(?:k|000)?)"]
    for pattern in over_patterns:
        match = re.search(pattern, query_lower)
        if match:
            price = parse_price_value(match.group(1))
            return (price, float('inf'))
    
    # Check for range patterns
    range_patterns = [
        r"between\s+(\d+(?:,\d{3})*(?:k|000)?)\s+and\s+(\d+(?:,\d{3})*(?:k|000)?)",
        r"(\d+(?:,\d{3})*(?:k|000)?)\s*[-–to]\s*(\d+(?:,\d{3})*(?:k|000)?)"
    ]
    for pattern in range_patterns:
        match = re.search(pattern, query_lower)
        if match:
            min_price = parse_price_value(match.group(1))
            max_price = parse_price_value(match.group(2))
            return (min_price, max_price)
    
    return (0, float('inf'))

def parse_price_value(price_str: str) -> float:
    """Convert price string to numeric value."""
    price_str = price_str.lower().replace(',', '')
    if 'k' in price_str:
        return float(price_str.replace('k', '')) * 1000
    elif price_str.endswith('000'):
        return float(price_str.replace('000', '')) * 1000
    return float(price_str)

def extract_location_terms(query: str) -> List[str]:
    """Extract location terms from user query."""
    locations = []
    for pattern in QUERY_PARSING_REGEXES["location"]:
        matches = re.findall(pattern, query, re.IGNORECASE)
        locations.extend(matches)
    return [loc.strip() for loc in locations if loc.strip()]

def extract_room_count(query: str) -> str:
    """Extract room count from user query."""
    for pattern in QUERY_PARSING_REGEXES["room_count"]:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            if "studio" in match.group(0).lower():
                return "1"
            return match.group(1)
    return ""

def identify_property_type(query: str) -> str:
    """Identify property type from user query, handling both English and Croatian values."""
    query_lower = query.lower()
    if re.search(r"apartment|stan", query_lower):
        return "apartments"  # Return English database value
    elif re.search(r"house|kuća", query_lower):
        return "houses"  # Return English database value
    elif re.search(r"commercial|poslovni", query_lower):
        if re.search(r"land|zemljište", query_lower):
            return "commercial_land"
        return "commercial_real_estate"  
    elif re.search(r"luxury|luksuz", query_lower):
        return "luxury_properties"
    elif re.search(r"land|zemljište", query_lower):
        return "commercial_land"
    return ""

def extract_features(query: str) -> List[str]:
    """Extract desired features from user query."""
    features = []
    feature_mappings = {
        r"sea view|more": "pogled_na_more = 'da'",
        r"elevator|lift": "lift = 'da'", 
        r"parking": "JSON_LENGTH(parking) > 0",
        r"balcony|balkon": "balkon_lodza_terasa IS NOT NULL"
    }
    
    for pattern, sql_condition in feature_mappings.items():
        if re.search(pattern, query, re.IGNORECASE):
            features.append(sql_condition)
    
    return features