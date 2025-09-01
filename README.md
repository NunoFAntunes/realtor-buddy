# Realtor Buddy 🏠

A sophisticated real estate search application that leverages AI to make Croatian property data searchable through natural language queries. Built with LangChain and Python, Realtor Buddy transforms user questions like "Find apartments in Zagreb under 200,000 euros" into precise SQL queries against a comprehensive property database.

## 🎯 Project Overview

Realtor Buddy addresses the challenge of searching through complex real estate data by providing an intelligent interface that understands both Croatian and English property-related queries. The system connects to a MariaDB database containing detailed information about Croatian properties from various real estate agencies.

### ✨ Key Features (Planned)
- **Natural Language Search**: Query properties using conversational language
- **Multilingual Support**: Works with both Croatian and English inputs
- **Comprehensive Database**: Access to extensive property data including location, price, features, and agency information
- **Smart Query Generation**: AI-powered SQL generation with safety validation
- **Rich CLI Interface**: Interactive command-line tool with health monitoring and configuration management
- **Flexible AI Backend**: Support for OpenAI, Anthropic, and Hugging Face models

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
│   ├── cli/                    # Command-line interface
│   │   └── main.py            # Interactive CLI with Rich formatting
│   └── utils/                  # Configuration and utilities
│       └── config.py          # Environment-based configuration
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── docs/                       # Documentation
├── database/
│   └── agency_properties.sql       # Database schema and sample data (19MB)
├── docker-compose.yml          # MariaDB setup
├── requirements.txt            # Python dependencies
└── .env                       # Configuration file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- AI API Key (OpenAI, Anthropic, or Hugging Face)

### 1. Environment Setup
```bash
# Clone and navigate to project
cd realtor-buddy

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac

# Install dependencies
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

# Edit .env and add your API keys:
# HUGGINGFACE_TOKEN=your_token_here
# or OPENAI_API_KEY=your_key_here
# or ANTHROPIC_API_KEY=your_key_here
```

### 4. Test Installation
```bash
# Check database connectivity
python -m src.realtor_buddy.cli.main health

# Verify configuration
python -m src.realtor_buddy.cli.main config
```

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

## 🔧 Available Commands

```bash
# Health monitoring
python -m src.realtor_buddy.cli.main health

# Configuration status
python -m src.realtor_buddy.cli.main config

# Property search (Phase 2C - CLI integration coming soon)
python -m src.realtor_buddy.cli.main search "apartments in Zagreb"
```

## 📋 Development Status

### ✅ Phase 1: Foundation (Complete)
- [x] Python project structure with proper packaging
- [x] Database connection layer with SQLAlchemy
- [x] Comprehensive health monitoring system
- [x] Rich CLI interface with status indicators
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

### 🚧 Phase 2C: CLI Integration & Testing (Next)
- [ ] Add search command to existing CLI interface
- [ ] Query result formatting and display
- [ ] Interactive query refinement and suggestions
- [ ] Comprehensive testing with real estate queries

### 📅 Future Phases
- **Phase 3**: Query generation and execution
- **Phase 4**: Enhanced UI and safety features
- **Phase 5**: Advanced search capabilities
- **Phase 6**: Testing and documentation

## Implementation Plan

### Phase 1: Project Foundation
1. **Environment Setup**
   - Create Python virtual environment
   - Install core dependencies: `langchain`, `langchain-community`, `pymysql`, `python-dotenv`
   - Install AI provider SDK (OpenAI, Anthropic, or local LLM)
   - Set up project structure with proper modules

2. **Database Connection Layer**
   - Create database connection manager using environment variables
   - Implement connection pooling for performance
   - Add database health check functionality
   - Create utility functions for query execution and result formatting

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

### Phase 3: Query Generation & Execution
6. **SQL Query Generation**
   - Implement safe SQL generation with query validation
   - Add query optimization hints for large dataset performance
   - Build complex query support (multiple filters, ranges, location-based)
   - Implement query result limiting and pagination

7. **Result Processing**
   - Create structured result formatting (JSON, table format)
   - Add result ranking and relevance scoring
   - Implement image URL processing and display
   - Build location-based result mapping integration

### Phase 4: User Interface & Experience
8. **Command Line Interface**
   - Build interactive CLI with query history
   - Add autocomplete for common property terms
   - Implement result export functionality (CSV, JSON)
   - Create verbose/debug mode for query inspection

9. **Query Validation & Safety**
   - Implement SQL injection prevention
   - Add query complexity limits and timeouts
   - Build error handling with user-friendly messages
   - Create fallback mechanisms for failed queries

### Phase 5: Advanced Features
10. **Enhanced Query Capabilities**
    - Location-based search using latitude/longitude
    - Price trend analysis and comparative queries
    - Agency performance and listing statistics
    - Advanced filtering (sea view, elevator, parking, etc.)

11. **Performance Optimization**
    - Implement query caching for common searches
    - Add database indexing recommendations
    - Build query performance monitoring
    - Optimize LLM token usage and response times

### Phase 6: Testing & Documentation
12. **Testing Framework**
    - Unit tests for database operations
    - Integration tests for LangChain SQL generation
    - End-to-end tests with sample queries
    - Performance benchmarking suite

13. **Documentation & Examples**
    - User guide with Croatian and English query examples
    - API documentation for programmatic usage
    - Deployment guide with Docker setup
    - Troubleshooting guide for common issues

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

### **Current Implementation (Phase 2B Complete)**
- **Database**: MariaDB with comprehensive Croatian property data (19MB dataset)
- **AI/LLM**: Local Llama-3.1-8B via HuggingFace Transformers (optimized for RTX 2070)
- **LangChain**: SQLDatabaseChain with custom Croatian real estate prompts
- **Language**: Python 3.8+ with SQLAlchemy, Transformers, PyTorch
- **Interface**: CLI foundation ready, SQL agent API complete
- **Hardware Requirements**: NVIDIA GPU (RTX 2070+), 16GB+ RAM

### **Key Components**
1. **Schema Analysis Layer** (Phase 2A)
   - Croatian ↔ English field mappings (40+ fields)
   - Query pattern recognition and value translation
   - Training examples and few-shot prompting templates

2. **LangChain SQL Agent** (Phase 2B)  
   - Local Llama-3.1-8B integration with custom SQL parser
   - Croatian real estate domain-optimized prompts
   - Database safety with read-only operations and query validation

3. **Database Infrastructure** (Phase 1)
   - MariaDB with Docker setup and health monitoring
   - SQLAlchemy connection management with pooling
   - Rich CLI interface with configuration management

### **Deployment Strategy**
- **Local Development**: Direct Python execution with local Llama model
- **Production**: Docker containers with GPU support for Llama inference
- **Future**: Web interface, API endpoints, cloud deployment options