"""
Croatian Real Estate Database Schema Mapping and Documentation

This module provides comprehensive mapping between Croatian database field names
and their English equivalents, along with schema documentation for LangChain SQL agents.
"""

from typing import Dict, List, Any

# Croatian to English field mapping
CROATIAN_TO_ENGLISH_MAPPING: Dict[str, str] = {
    # Basic property information
    "agencijska_provizija": "agency_commission",
    "agencijsku_proviziju_placa": "commission_paid_by",
    "balkon_lodza_terasa": "balcony_loggia_terrace",
    "blizina_tramvaja": "tram_proximity",
    "broj_etaza": "number_of_floors",
    "broj_parkirnih_mjesta": "number_of_parking_spaces",
    "broj_prostorija": "number_of_rooms",
    "broj_sanitarnih_cvorova": "number_of_bathrooms",
    "broj_soba": "number_of_bedrooms",
    
    # Availability and accessibility
    "dostupno_od": "available_from",
    "dostupnost_kroz_godinu": "yearly_availability",
    "energetski_razred": "energy_rating",
    "godina_izgradnje": "construction_year",
    "godina_zadnje_adaptacije": "last_adaptation_year",
    "godina_zadnje_renovacije": "last_renovation_year",
    
    # Location and floor information
    "kat": "floor",
    "lift": "elevator",
    "lokacija": "location",
    "mogucnost_zamjene": "exchange_possibility",
    "namjena": "purpose_use",
    "namjena_poslovnog_prostora": "commercial_space_purpose",
    "namjestenost_i_stanje": "furnished_condition",
    
    # Area measurements
    "netto_povrsina": "net_area",
    "pogled_na_more": "sea_view",
    "povrsina": "surface_area",
    "povrsina_objekta": "building_area",
    "povrsina_okucnice": "yard_area",
    "stambena_povrsina": "living_area",
    
    # Commercial and business properties
    "pozicija_poslovnog_prostora": "commercial_space_position",
    "razgledavanje_putem_video_poziva": "video_call_viewing",
    "rezije": "utilities_costs",
    
    # Property types and characteristics
    "tip_kuce": "house_type",
    "tip_nekretnine": "property_type",
    "tip_stana": "apartment_type",
    "tip_zemljista": "land_type",
    "ukupni_broj_katova": "total_floors",
    "ulica": "street",
    "vrsta_kuce_gradnje": "house_construction_type",
    "sifra_objekta": "property_code",
    
    # JSON fields with complex data
    "dozvole": "permits",
    "dozvole_i_potvrde": "permits_and_certificates",
    "funkcionalnosti_i_ostale_karakteristike": "functionality_other_features",
    "grijanje": "heating",
    "komunalije": "utilities",
    "kupaonica_i_wc": "bathroom_toilet",
    "orijentacija_stana": "apartment_orientation",
    "ostali_objekti_i_povrsine": "other_objects_surfaces",
    "parking": "parking",
    "podaci_o_objektu": "building_data",
    "tehnika": "technical_equipment",
    "troskovi": "costs",
    "vrsta_parkinga": "parking_type",
}

# Reverse mapping for English to Croatian
ENGLISH_TO_CROATIAN_MAPPING: Dict[str, str] = {
    v: k for k, v in CROATIAN_TO_ENGLISH_MAPPING.items()
}

# Schema documentation for LangChain
SCHEMA_DOCUMENTATION = {
    "table_name": "agency_properties",
    "description": "Croatian real estate properties from various agencies with comprehensive property details",
    "primary_key": "id",
    "indexes": [
        "ad_id (unique)",
        "agency_name",
        "property_type", 
        "lokacija",
        "price",
        "created_at"
    ],
    "fields": {
        # Core identifiers and metadata
        "id": {
            "type": "int(11)",
            "description": "Primary key, unique property identifier",
            "nullable": False
        },
        "ad_id": {
            "type": "varchar(255)",
            "description": "Unique advertisement ID from the source website",
            "nullable": True,
            "unique": True
        },
        "url": {
            "type": "varchar(510)",
            "description": "URL to the original property listing",
            "nullable": True
        },
        "website": {
            "type": "varchar(50)",
            "description": "Source website (default: 'njuskalo')",
            "nullable": True,
            "default": "njuskalo"
        },
        
        # Agency information
        "agency_name": {
            "type": "varchar(255)",
            "description": "Name of the real estate agency",
            "nullable": True,
            "indexed": True
        },
        "agency_type": {
            "type": "enum('agencija','investitor','trgovina')",
            "description": "Type of agency: agencija (agency), investitor (investor), trgovina (trade)",
            "nullable": True,
            "values": ["agencija", "investitor", "trgovina"]
        },
        
        # Basic property information
        "property_type": {
            "type": "varchar(100)",
            "description": "General property type (stan/apartment, kuća/house, etc.)",
            "nullable": True,
            "indexed": True
        },
        "title": {
            "type": "varchar(500)",
            "description": "Property listing title/headline",
            "nullable": True
        },
        "description": {
            "type": "text",
            "description": "Detailed property description",
            "nullable": True
        },
        "price": {
            "type": "decimal(12,2)",
            "description": "Property price in EUR",
            "nullable": True,
            "indexed": True
        },
        "view_count": {
            "type": "int(11)",
            "description": "Number of times the listing was viewed",
            "nullable": True
        },
        "posted_date": {
            "type": "varchar(100)",
            "description": "When the listing was originally posted",
            "nullable": True
        },
        
        # Location data
        "latitude": {
            "type": "decimal(10,8)",
            "description": "GPS latitude coordinate",
            "nullable": True
        },
        "longitude": {
            "type": "decimal(11,8)",
            "description": "GPS longitude coordinate", 
            "nullable": True
        },
        "lokacija": {
            "type": "varchar(500)",
            "description": "Location/address description in Croatian",
            "nullable": True,
            "indexed": True,
            "english_equivalent": "location"
        },
        "ulica": {
            "type": "varchar(200)",
            "description": "Street address",
            "nullable": True,
            "english_equivalent": "street"
        },
        
        # Property characteristics (Croatian fields)
        "broj_soba": {
            "type": "varchar(100)",
            "description": "Number of bedrooms/rooms",
            "nullable": True,
            "english_equivalent": "number_of_bedrooms",
            "common_values": ["1", "2", "3", "4", "5+"]
        },
        "broj_sanitarnih_cvorova": {
            "type": "varchar(100)",
            "description": "Number of bathrooms/toilets",
            "nullable": True,
            "english_equivalent": "number_of_bathrooms"
        },
        "povrsina": {
            "type": "varchar(100)",
            "description": "Total surface area in m²",
            "nullable": True,
            "english_equivalent": "surface_area",
            "unit": "m²"
        },
        "kat": {
            "type": "varchar(100)",
            "description": "Floor number (prizemlje=ground floor, numbers for upper floors)",
            "nullable": True,
            "english_equivalent": "floor",
            "common_values": ["prizemlje", "1", "2", "3", "potkrovlje"]
        },
        "lift": {
            "type": "varchar(50)",
            "description": "Elevator availability (da/ne = yes/no)",
            "nullable": True,
            "english_equivalent": "elevator",
            "common_values": ["da", "ne"]
        },
        "pogled_na_more": {
            "type": "varchar(50)",
            "description": "Sea view (da/ne = yes/no)",
            "nullable": True,
            "english_equivalent": "sea_view",
            "common_values": ["da", "ne"]
        },
        "energetski_razred": {
            "type": "varchar(50)",
            "description": "Energy efficiency rating (A+ to G)",
            "nullable": True,
            "english_equivalent": "energy_rating",
            "common_values": ["A+", "A", "B", "C", "D", "E", "F", "G"]
        },
        "godina_izgradnje": {
            "type": "varchar(50)",
            "description": "Construction/build year",
            "nullable": True,
            "english_equivalent": "construction_year"
        },
        "namjena": {
            "type": "varchar(100)",
            "description": "Property purpose/use (stambena=residential, poslovna=commercial)",
            "nullable": True,
            "english_equivalent": "purpose_use",
            "common_values": ["stambena", "poslovna", "mješovita"]
        },
        
        # JSON fields with complex structured data
        "parking": {
            "type": "longtext (JSON)",
            "description": "JSON array of parking options and details",
            "nullable": True,
            "english_equivalent": "parking",
            "json_structure": "Array of parking types and availability"
        },
        "grijanje": {
            "type": "longtext (JSON)", 
            "description": "JSON array of heating systems and types",
            "nullable": True,
            "english_equivalent": "heating",
            "json_structure": "Array of heating types (centralno, etažno, etc.)"
        },
        "komunalije": {
            "type": "longtext (JSON)",
            "description": "JSON array of utilities (water, electricity, gas, etc.)",
            "nullable": True,
            "english_equivalent": "utilities",
            "json_structure": "Array of utility types and availability"
        },
        
        # Timestamps
        "created_at": {
            "type": "timestamp",
            "description": "When the record was created in the database",
            "nullable": False,
            "indexed": True,
            "default": "current_timestamp()"
        },
        "time_posted": {
            "type": "timestamp", 
            "description": "Timestamp of when posted (auto-updated)",
            "nullable": False,
            "default": "current_timestamp() ON UPDATE current_timestamp()"
        },
        "last_updated": {
            "type": "timestamp",
            "description": "When the record was last modified",
            "nullable": False,
            "default": "current_timestamp() ON UPDATE current_timestamp()"
        }
    }
}

# Common query patterns and field relationships
QUERY_PATTERNS = {
    "location_search": {
        "description": "Search by location/area",
        "fields": ["lokacija", "ulica", "latitude", "longitude"],
        "english_equivalents": ["location", "street", "latitude", "longitude"],
        "example_values": ["Zagreb", "Split", "Rijeka", "Osijek", "Zadar"]
    },
    "price_range": {
        "description": "Filter by price range",
        "fields": ["price"],
        "operators": ["<", ">", "BETWEEN", "<=", ">="],
        "example_ranges": ["50000-100000", "100000-200000", "200000-500000"]
    },
    "property_size": {
        "description": "Filter by property size/area",
        "fields": ["povrsina", "stambena_povrsina", "netto_povrsina"],
        "english_equivalents": ["surface_area", "living_area", "net_area"],
        "unit": "m²",
        "example_ranges": ["50-80", "80-120", "120-200"]
    },
    "room_count": {
        "description": "Filter by number of rooms/bedrooms",
        "fields": ["broj_soba", "broj_prostorija"],
        "english_equivalents": ["number_of_bedrooms", "number_of_rooms"],
        "common_values": ["1", "2", "3", "4", "5+"]
    },
    "property_features": {
        "description": "Search by specific features",
        "fields": ["pogled_na_more", "lift", "parking", "balkon_lodza_terasa"],
        "english_equivalents": ["sea_view", "elevator", "parking", "balcony_loggia_terrace"],
        "boolean_fields": ["pogled_na_more", "lift"],
        "json_fields": ["parking"]
    },
    "property_type": {
        "description": "Filter by property type",
        "fields": ["property_type", "tip_nekretnine", "tip_stana", "tip_kuce"],
        "english_equivalents": ["property_type", "property_type", "apartment_type", "house_type"],
        "common_values": ["stan", "kuća", "poslovni prostor", "zemljište"]
    }
}

# Value mappings for common Croatian terms
CROATIAN_VALUE_MAPPINGS = {
    "boolean_yes_no": {
        "da": "yes",
        "ne": "no"
    },
    "floor_levels": {
        "prizemlje": "ground_floor",
        "potkrovlje": "attic",
        "podrum": "basement"
    },
    "property_types": {
        "stan": "apartment",
        "kuća": "house", 
        "poslovni prostor": "commercial_space",
        "zemljište": "land",
        "garaža": "garage"
    },
    "agency_types": {
        "agencija": "agency",
        "investitor": "investor", 
        "trgovina": "trade"
    },
    "purpose_use": {
        "stambena": "residential",
        "poslovna": "commercial",
        "mješovita": "mixed_use"
    }
}

def get_english_field_name(croatian_field: str) -> str:
    """
    Convert Croatian field name to English equivalent.
    
    Args:
        croatian_field: Croatian database field name
        
    Returns:
        English equivalent field name, or original if no mapping exists
    """
    return CROATIAN_TO_ENGLISH_MAPPING.get(croatian_field, croatian_field)

def get_croatian_field_name(english_field: str) -> str:
    """
    Convert English field name to Croatian database field name.
    
    Args:
        english_field: English field name
        
    Returns:
        Croatian database field name, or original if no mapping exists
    """
    return ENGLISH_TO_CROATIAN_MAPPING.get(english_field, english_field)

def get_field_info(field_name: str) -> Dict[str, Any]:
    """
    Get comprehensive information about a database field.
    
    Args:
        field_name: Database field name (Croatian or English)
        
    Returns:
        Dictionary containing field type, description, constraints, etc.
    """
    # Try Croatian field name first
    if field_name in SCHEMA_DOCUMENTATION["fields"]:
        return SCHEMA_DOCUMENTATION["fields"][field_name]
    
    # Try English equivalent
    croatian_name = get_croatian_field_name(field_name)
    if croatian_name in SCHEMA_DOCUMENTATION["fields"]:
        return SCHEMA_DOCUMENTATION["fields"][croatian_name]
    
    return {}

def translate_croatian_value(field_name: str, croatian_value: str) -> str:
    """
    Translate Croatian field values to English equivalents.
    
    Args:
        field_name: Database field name
        croatian_value: Croatian value to translate
        
    Returns:
        English equivalent value, or original if no mapping exists
    """
    # Check field-specific mappings based on field characteristics
    field_info = get_field_info(field_name)
    
    # Boolean fields (da/ne)
    if field_name in ["pogled_na_more", "lift"] or "yes/no" in str(field_info.get("description", "")):
        return CROATIAN_VALUE_MAPPINGS["boolean_yes_no"].get(croatian_value.lower(), croatian_value)
    
    # Floor levels
    if field_name == "kat":
        return CROATIAN_VALUE_MAPPINGS["floor_levels"].get(croatian_value.lower(), croatian_value)
    
    # Property types
    if "property" in field_name.lower() or "tip" in field_name:
        return CROATIAN_VALUE_MAPPINGS["property_types"].get(croatian_value.lower(), croatian_value)
    
    # Agency types
    if field_name == "agency_type":
        return CROATIAN_VALUE_MAPPINGS["agency_types"].get(croatian_value.lower(), croatian_value)
    
    # Purpose/use
    if field_name == "namjena":
        return CROATIAN_VALUE_MAPPINGS["purpose_use"].get(croatian_value.lower(), croatian_value)
    
    return croatian_value