# Realtor Buddy 🏠

A sophisticated real estate search application that leverages AI to make Croatian property data searchable through natural language queries. Built with LangChain and Python, Realtor Buddy transforms user questions like "Find apartments in Zagreb under 200,000 euros" into precise SQL queries against a comprehensive property database.

## 🎯 Project Overview

Realtor Buddy addresses the challenge of searching through complex real estate data by providing an intelligent interface that understands both Croatian and English property-related queries. The system connects to a MariaDB database containing detailed information about Croatian properties from various real estate agencies.

### ✨ Key Features
- **Natural Language Search**: Query properties using conversational language in a web interface
- **Multilingual Support**: Works with both Croatian and English property search queries
- **Visual Property Display**: Interactive property cards with images, maps, and detailed information
- **Smart Query Generation**: AI-powered SQL generation using local Llama-3.1-8B model
- **Croatian Real Estate Expert**: Understands Croatian property terminology and location names
- **Fast & Local**: No API costs - runs entirely on your hardware with GPU acceleration

## 🏗️ Project Structure

```
realtor-buddy/
├── src/realtor_buddy/          # Main application package
│   ├── database/               # Database connection and health checks
│   │   ├── connection.py       # SQLAlchemy-based connection manager
│   │   └── health_check.py     # Comprehensive database monitoring
│   ├── langchain_agent/        # LangChain SQL agent implementation
│   │   ├── schema_mapping.py   # Croatian ↔ English field mappings
│   │   ├── schema_docs.py      # LangChain-formatted documentation
│   │   ├── query_patterns.py   # Common search patterns & value formats
│   │   ├── training_examples.py # Real-world query examples for training
│   │   ├── schema_analyzer.py  # Unified interface for schema analysis
│   │   └── sql_agent.py        # Main LangChain SQL agent with Llama-3.1-8B
│   ├── webapp/                 # Web application (Phase 3+)
│   │   ├── api/               # FastAPI backend routes
│   │   ├── static/            # CSS, JavaScript, images  
│   │   ├── templates/         # HTML templates
│   │   └── main.py           # FastAPI application entry point
│   └── utils/                  # Configuration and utilities
│       └── config.py          # Environment-based configuration
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── docs/                       # Documentation
├── database/
│   └── agency_properties.sql       # Database schema and sample data (19MB)
├── docker compose.yml          # Full stack deployment (database + webapp)
├── docker compose.override.yml # Development configuration
├── Dockerfile                  # Web application container with GPU support
├── .dockerignore              # Docker build optimization
├── requirements.txt            # Complete Python dependencies
└── .env                       # Configuration file
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone and navigate to project
cd realtor-buddy

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac

# Install dependencies (includes PyTorch, Transformers, LangChain, FastAPI)
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Start MariaDB with Docker
docker compose up -d
```

### 3. Configuration
```bash
# Copy environment template
cp .env.example .env

### 4. Launch Web Application

#### Option A: Docker (Recommended)
```bash
# Start full stack (database + web app) with GPU support
docker compose up

# For development with hot reload
docker compose up

# Open browser to: http://localhost:8000
```

#### Option B: Local Development
```bash
# Start database only
docker compose up database

# Install dependencies locally
pip install -r requirements.txt

# Start web application
python -m src.realtor_buddy.webapp.main

# Open browser to: http://localhost:8000
```

#### Try These Searches:
- "apartments in Zagreb under 200k euros"
- "houses with sea view in Split"  
- "3 bedroom properties with elevator"
- "ground floor apartments with parking"

## 📊 Database Schema & Field Mapping

The core `agency_properties` table contains comprehensive property information with **Croatian field names** that are intelligently mapped to English equivalents:

### 🏠 Property Information
- **Basic Info**: Price, location (`lokacija`), property type (`tip_nekretnine`), title, description
- **Property Details**: Rooms (`broj_soba`), bathrooms (`broj_sanitarnih_cvorova`), surface area (`povrsina`), floor (`kat`), elevator (`lift`)
- **Location Data**: GPS coordinates, address (`ulica`), proximity to transport (`blizina_tramvaja`)
- **Features**: Sea view (`pogled_na_more`), parking, balcony (`balkon_lodza_terasa`), energy rating (`energetski_razred`)
- **Agency Data**: Agency name, type (`agencija`/`investitor`/`trgovina`), commission details
- **Metadata**: Posted date, view count, images (JSON), timestamps

### 🗺️ Croatian ↔ English Field Mapping
The system includes comprehensive field mappings for natural language queries:

| Croatian Field | English Equivalent | Example Values |
|---|---|---|
| `broj_soba` | number_of_bedrooms | "1", "2", "3", "4", "5+" |
| `povrsina` | surface_area | "45", "85.5", "120" (m²) |
| `lokacija` | location | "Zagreb, Gornji Grad" |
| `kat` | floor | "prizemlje", "1", "potkrovlje" |
| `lift` | elevator | "da", "ne" (yes/no) |
| `pogled_na_more` | sea_view | "da", "ne" (yes/no) |
| `energetski_razred` | energy_rating | "A+", "A", "B", "C", "D" |

### 🔍 Smart Query Understanding
The AI agent understands natural language patterns and translates them to proper SQL:
- **"apartments in Zagreb"** → `property_type LIKE '%stan%' AND lokacija LIKE '%Zagreb%'`
- **"3 bedrooms under 200k"** → `broj_soba = '3' AND price < 200000`  
- **"sea view properties"** → `pogled_na_more = 'da'`
- **"ground floor with elevator"** → `kat = 'prizemlje' AND lift = 'da'`

## 🌟 Web Application Features

The Croatian Real Estate Search app provides:

- **🔍 Natural Language Search**: Type queries like "apartments in Zagreb under 200k euros"
- **🏠 Visual Property Cards**: See photos, prices, locations, and key features at a glance  
- **🗺️ Interactive Maps**: View property locations on integrated maps using GPS coordinates
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices
- **⚡ Fast Local AI**: No API costs - Llama-3.1-8B runs on your GPU for instant results
- **🇭🇷 Croatian Expert**: Understands Croatian property terms, cities, and neighborhoods

## Example Queries Supported

The schema analysis system now supports comprehensive query understanding and translation:

### 🔍 Basic Searches
- **"Find apartments in Zagreb under 200,000 euros"**
  ```sql
  SELECT * FROM agency_properties 
  WHERE property_type LIKE '%stan%' 
  AND lokacija LIKE '%Zagreb%' 
  AND price < 200000
  ```

- **"Show me houses with sea view in Split"**
  ```sql
  SELECT * FROM agency_properties 
  WHERE property_type LIKE '%kuća%' 
  AND lokacija LIKE '%Split%' 
  AND pogled_na_more = 'da'
  ```

### 🏡 Feature-Based Searches
- **"Properties with parking and elevator in city center"**
  ```sql
  SELECT * FROM agency_properties 
  WHERE lift = 'da' 
  AND JSON_LENGTH(parking) > 0 
  AND lokacija LIKE '%centar%'
  ```

- **"Ground floor apartments with balcony"**
  ```sql
  SELECT * FROM agency_properties 
  WHERE property_type LIKE '%stan%' 
  AND kat = 'prizemlje' 
  AND balkon_lodza_terasa IS NOT NULL
  ```

### 🏢 Advanced Searches  
- **"New constructions from 2020 onwards with 3+ rooms"**
  ```sql
  SELECT * FROM agency_properties 
  WHERE CAST(godina_izgradnje AS UNSIGNED) >= 2020 
  AND broj_soba IN ('3', '4', '5+')
  ```

- **"4+ bedroom houses in Split with garden and parking under 600k"**
  ```sql
  SELECT * FROM agency_properties 
  WHERE property_type LIKE '%kuća%' 
  AND lokacija LIKE '%Split%'
  AND broj_soba IN ('4', '5+')
  AND povrsina_okucnice IS NOT NULL 
  AND price < 600000
  ```

## 🔧 Technical Architecture

### **Current Implementation (Phase 3 Complete)**
- **Database**: MariaDB with comprehensive Croatian property data (19MB dataset)
- **AI/LLM**: Local Llama-3.1-8B via HuggingFace Transformers (optimized for RTX 2070)
- **LangChain**: SQLDatabaseChain with custom Croatian real estate prompts
- **Backend**: FastAPI with async support, comprehensive API endpoints
- **Frontend**: Complete responsive web interface with embedded HTML
- **Language**: Python 3.8+ with FastAPI, SQLAlchemy, Transformers, PyTorch
- **Deployment**: Docker containers with GPU support and health monitoring
- **Hardware Requirements**: NVIDIA GPU (RTX 2070+), 16GB+ RAM

### **Production-Ready Web Architecture**
- **Backend**: FastAPI with async Llama inference and background initialization
- **API Design**: RESTful endpoints with comprehensive Pydantic validation
- **Frontend**: Responsive web interface with real-time search and property cards
- **Database**: MariaDB with health monitoring and connection pooling
- **Deployment**: Docker Compose with GPU support, hot reload, service dependencies
- **Monitoring**: System health endpoints (GPU, database, LLM status)


### **Deployment Strategy**
- **Docker Deployment**: `docker compose up` for complete full-stack deployment
- **Local Development**: Hot reload with `docker compose.override.yml` configuration
- **GPU Support**: NVIDIA runtime with automatic device mapping and model caching
- **Health Monitoring**: Comprehensive service health checks and automatic restarts
- **Production Ready**: nginx reverse proxy, service dependencies, and error recovery