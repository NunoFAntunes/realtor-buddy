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
├── docker-compose.yml          # Full stack deployment (database + webapp)
├── docker-compose.override.yml # Development configuration
├── Dockerfile                  # Web application container with GPU support
├── .dockerignore              # Docker build optimization
├── requirements.txt            # Complete Python dependencies
└── .env                       # Configuration file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Docker and Docker Compose** 
- **NVIDIA GPU** (RTX 2070+ recommended) with CUDA support
- **16GB+ RAM** (32GB recommended for optimal performance)

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
docker-compose up -d

# The database will automatically initialize with property data
# Default connection: localhost:3306/njuskam_ultimate3
```

### 3. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with database settings (no AI API keys needed - runs locally!)
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=njuskam_ultimate3
# DB_USER=realtor_user
# DB_PASSWORD=realtor_password
```

### 4. Launch Web Application

#### Option A: Docker (Recommended)
```bash
# Start full stack (database + web app) with GPU support
docker-compose up

# For development with hot reload
docker-compose up

# Open browser to: http://localhost:8000
```

#### Option B: Local Development
```bash
# Start database only
docker-compose up database

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

## 📋 Development Status

### ✅ Phase 1: Foundation (Complete)
- [x] Python project structure with proper packaging
- [x] Database connection layer with SQLAlchemy
- [x] Comprehensive health monitoring system
- [x] Configuration management with validation
- [x] Docker-based database setup

### ✅ Phase 2A: Schema Analysis & Mapping (Complete)
- [x] **Schema analysis and Croatian field mapping**
  - [x] Complete Croatian ↔ English field mapping dictionary (40+ fields)
  - [x] Database schema documentation for LangChain agents
  - [x] Croatian value translation system (`da/ne` → `yes/no`, floor levels, etc.)
  - [x] Field type validation and casting guidance
- [x] **Query pattern documentation** 
  - [x] Common search patterns (location, price, size, features)
  - [x] Value format specifications and examples
  - [x] Croatian location terms and property types
  - [x] Query optimization recommendations
- [x] **Training examples for LangChain**
  - [x] 20+ real-world query examples with SQL translations
  - [x] Categorized examples (basic, luxury, budget, complex)
  - [x] Few-shot prompting templates
  - [x] Negative examples showing common mistakes
- [x] **Unified schema analyzer interface**
  - [x] Query analysis and component extraction
  - [x] Field relevance suggestion system
  - [x] LangChain configuration formatting
  - [x] Query validation and error detection

### ✅ Phase 2B: LangChain SQL Agent (Complete)
- [x] **LangChain SQL agent configuration**
  - [x] Local Llama-3.1-8B integration with HuggingFace Transformers
  - [x] Optimized for RTX 2070 + 32GB RAM (FP16, no quantization)
  - [x] SQLDatabaseChain with custom Croatian real estate prompt templates
  - [x] Custom SQL query parser for clean Llama output extraction
- [x] **Database integration and safety**
  - [x] Extended Phase 1 database connection with LangChain SQLDatabase
  - [x] Read-only operations with connection pooling
  - [x] Built-in SQL query validation and result limiting
  - [x] Comprehensive error handling and logging
- [x] **Croatian real estate domain optimization**
  - [x] Few-shot prompting with 5 best training examples
  - [x] Croatian terminology guidance in system prompts
  - [x] Integrated schema documentation and field mappings
  - [x] Natural language to SQL translation pipeline

### ✅ Phase 3: FastAPI Web Backend (Complete)
- [x] **FastAPI application setup**
  - [x] Created FastAPI app with async support for Llama inference
  - [x] Integrated existing SQL agent with web API endpoints
  - [x] Added CORS support and error handling middleware
  - [x] Implemented comprehensive Pydantic request/response models
- [x] **API endpoints for property search**
  - [x] `/api/search` endpoint for natural language property queries
  - [x] `/api/health` comprehensive system status monitoring
  - [x] `/api/search/examples` for query suggestions and guidance
  - [x] Robust error handling and query validation
  - [x] Structured property data response formatting
- [x] **Complete web interface**
  - [x] Embedded HTML frontend with modern, responsive design
  - [x] Real-time property search with loading indicators
  - [x] Property cards displaying price, location, features
  - [x] Mobile-friendly interface with error handling
- [x] **Docker deployment**
  - [x] Complete Dockerfile with NVIDIA GPU support
  - [x] docker-compose.yml for full stack deployment
  - [x] Development configuration with hot reload
  - [x] Health monitoring and automatic service dependencies

### 🚧 Phase 4: Enhanced Frontend Features (Future)
- [ ] **Advanced property display**
  - [ ] Image galleries from database JSON URLs
  - [ ] Interactive maps using latitude/longitude coordinates
  - [ ] Property detail modal/page with full information
  - [ ] Advanced filtering and sorting options
- [ ] **User experience enhancements**
  - [ ] Pagination for large result sets
  - [ ] Infinite scroll loading
  - [ ] Croatian/English language toggle
  - [ ] Save favorite properties and searches
- [ ] **Advanced search features**
  - [ ] Comparison tools for multiple properties
  - [ ] Price alerts and notifications
  - [ ] Search history and saved queries
  - [ ] Advanced filters (price range sliders, map boundaries)

### 📅 Future Phases
- **Phase 5**: Advanced Features (favorites, comparisons, alerts)
- **Phase 6**: Performance & Scaling (caching, optimization)
- **Phase 7**: Testing & Documentation (comprehensive test suite)
- **Phase 8**: Deployment (Docker, production deployment)

## 🛠️ Web Application Implementation Plan

### Phase 1: Project Foundation ✅
1. **Environment Setup (COMPLETE)**
   - ✅ Python virtual environment with all dependencies
   - ✅ Installed: `langchain`, `transformers`, `torch`, `pymysql`, `sqlalchemy`
   - ✅ Local Llama-3.1-8B integration via HuggingFace
   - ✅ Project structure with proper modules

2. **Database Connection Layer (COMPLETE)**
   - ✅ SQLAlchemy database connection manager
   - ✅ Connection pooling and health monitoring
   - ✅ MariaDB Docker setup with Croatian property data
   - ✅ Utility functions for database operations

### Phase 2A: Schema Analysis & Croatian Field Mapping ✅
3. **Schema Analysis & Documentation (COMPLETE)**
   - ✅ Generated comprehensive schema documentation for LangChain agents
   - ✅ Created complete Croatian ↔ English field mapping dictionary (40+ fields)
   - ✅ Documented all query patterns and expected value formats
   - ✅ Built 20+ real-world sample queries for agent training
   - ✅ Added field type validation and casting guidance for VARCHAR numeric fields

**Key Implementation Files:**
- `schema_mapping.py`: Complete field mappings and value translations
- `schema_docs.py`: LangChain-formatted table documentation and prompt templates  
- `query_patterns.py`: Common search patterns, value formats, and Croatian location terms
- `training_examples.py`: Comprehensive real-world query examples for few-shot learning
- `schema_analyzer.py`: Unified interface combining all schema analysis functionality

**Features Delivered:**
- **Croatian Value Translation**: `da/ne` → `yes/no`, `prizemlje` → `ground_floor`, property types
- **Smart Query Analysis**: Extracts price ranges, locations, room counts from natural language
- **Field Relevance Engine**: Suggests relevant database fields based on query content
- **Query Validation**: Detects invalid price ranges, unrecognized locations, unusual values
- **Training Examples**: Categories include basic searches, luxury properties, budget finds, complex multi-criteria

### Phase 2B: LangChain SQL Agent Implementation ✅
4. **LangChain SQL Chain Setup (COMPLETE)**
   - ✅ Initialized SQLDatabaseChain with MariaDB connection using existing Phase 1 infrastructure
   - ✅ Configured SQL agent with comprehensive Croatian schema information and field mappings
   - ✅ Implemented few-shot prompting with 5 best real estate domain examples
   - ✅ Added custom prompt templates optimized for Croatian property terminology
   - ✅ Integrated local Llama-3.1-8B model with HuggingFace Transformers (RTX 2070 optimized)

**Key Implementation File:**
- `sql_agent.py`: Complete LangChain SQL agent with local Llama-3.1-8B integration

**Features Delivered:**
- **Local Llama-3.1-8B Integration**: FP16 optimization, no quantization, auto device mapping
- **Croatian Real Estate Prompts**: System prompts with terminology guidance and few-shot examples
- **Database Safety**: Read-only operations, connection pooling, query validation, result limiting
- **Error Handling**: Comprehensive error recovery, structured responses, detailed logging
- **Custom SQL Parser**: Extracts clean SQL queries from Llama model outputs
- **Production Ready**: Connection testing, schema inspection, convenient wrapper functions

**Usage Examples:**
```python
# Initialize and use the agent
from src.realtor_buddy.langchain_agent.sql_agent import create_agent
agent = create_agent()
result = agent.query("Find apartments in Zagreb under 200000 euros")

# Quick one-off queries
from src.realtor_buddy.langchain_agent.sql_agent import quick_query
result = quick_query("3 bedroom houses with sea view")
```

5. **Natural Language Processing (INTEGRATED)**
   - ✅ Query intent classification integrated into prompt templates
   - ✅ Croatian/English query support through schema mappings and value translations
   - ✅ Location normalization using Croatian location terms dictionary
   - ✅ Price range and property type standardization in training examples

### Phase 3: FastAPI Web Backend ✅
6. **FastAPI Application Development (COMPLETE)**
   - ✅ Created async FastAPI app optimized for Llama-3.1-8B inference with background initialization
   - ✅ Integrated existing SQL agent with comprehensive web API endpoints
   - ✅ Implemented complete Pydantic models for request/response validation
   - ✅ Added CORS support, global exception handling, and error recovery middleware

**Key Implementation Files:**
- `webapp/main.py`: Complete FastAPI application with embedded frontend
- `webapp/models.py`: Comprehensive Pydantic request/response models  
- `webapp/api/search.py`: Property search endpoints with structured result parsing
- `webapp/api/health.py`: System health monitoring with GPU and database status

7. **Property Search API (COMPLETE)**
   - ✅ `/api/search` endpoint for natural language property queries with full Croatian field support
   - ✅ `/api/health` comprehensive system status (database, LLM, GPU, system resources)
   - ✅ `/api/search/examples` query suggestions and guidance for users
   - ✅ Robust error handling and SQL query validation with user-friendly messages
   - ✅ Structured property data formatting with all Croatian real estate fields

**Features Delivered:**
- **Complete Web Interface**: Embedded responsive HTML with real-time search
- **Property Cards**: Display price, location, rooms, features with Croatian field mapping
- **System Monitoring**: GPU utilization, database connectivity, model status
- **Error Recovery**: Graceful handling of AI/database failures with detailed logging
- **Docker Deployment**: Full-stack containerization with GPU support and health checks

### Phase 4: Frontend Web Interface
8. **Search Interface Design**
   - Modern, responsive search page with intuitive input field
   - Loading states and progress indicators during AI processing
   - Error handling with user-friendly messages
   - Query suggestions and example searches

9. **Property Results Display**
   - Visual property cards with images from database JSON URLs
   - Display key information: price, location, rooms, features
   - Pagination and infinite scroll for large result sets
   - Sort and filter options (price, location, date, etc.)

### Phase 5: Enhanced User Experience  
10. **Interactive Features**
    - Interactive maps showing property locations using GPS coordinates
    - Property detail pages with full information and image galleries
    - Responsive design optimized for mobile and desktop
    - Croatian/English language toggle for international users

11. **Advanced Search Capabilities**
    - Save favorite properties and search criteria
    - Property comparison tools (side-by-side comparison)
    - Price alerts and new listing notifications
    - Advanced filters (sea view, elevator, parking, energy rating)

### Phase 6: Performance & Production
12. **Optimization & Scaling**
    - Query result caching and database query optimization
    - Image lazy loading and CDN integration for property photos
    - Performance monitoring and analytics
    - GPU memory optimization for Llama model inference

13. **Testing & Deployment**
    - Comprehensive test suite (unit, integration, end-to-end)
    - Docker containerization with GPU support
    - Production deployment guide and monitoring setup
    - User documentation and Croatian real estate search examples

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

### **Key Components**
1. **Schema Analysis Layer** (Phase 2A)
   - Croatian ↔ English field mappings (40+ fields)
   - Query pattern recognition and value translation
   - Training examples and few-shot prompting templates

2. **LangChain SQL Agent** (Phase 2B)  
   - Local Llama-3.1-8B integration with custom SQL parser
   - Croatian real estate domain-optimized prompts
   - Database safety with read-only operations and query validation

3. **FastAPI Web Application** (Phase 3)
   - Async web server with comprehensive API endpoints
   - Embedded responsive frontend with real-time search
   - System health monitoring and error recovery
   - Docker containerization with GPU support

4. **Database Infrastructure** (Phase 1)
   - MariaDB with Docker setup and health monitoring
   - SQLAlchemy connection management with pooling
   - Configuration management and health monitoring system

### **Deployment Strategy**
- **Docker Deployment**: `docker-compose up` for complete full-stack deployment
- **Local Development**: Hot reload with `docker-compose.override.yml` configuration
- **GPU Support**: NVIDIA runtime with automatic device mapping and model caching
- **Health Monitoring**: Comprehensive service health checks and automatic restarts
- **Production Ready**: nginx reverse proxy, service dependencies, and error recovery