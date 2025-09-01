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
│   ├── langchain_agent/        # LangChain SQL agent (Phase 2)
│   ├── cli/                    # Command-line interface
│   │   └── main.py            # Interactive CLI with Rich formatting
│   └── utils/                  # Configuration and utilities
│       └── config.py          # Environment-based configuration
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── docs/                       # Documentation
├── agency_properties.sql       # Database schema and sample data (19MB)
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

## 📊 Database Schema

The core `agency_properties` table contains comprehensive property information:

- **Basic Info**: Price, location, property type, title, description
- **Property Details**: Rooms, bathrooms, surface area, floor, elevator
- **Location Data**: GPS coordinates, address, proximity to transport
- **Features**: Sea view, parking, balcony, energy rating
- **Agency Data**: Agency name, type, commission details
- **Metadata**: Posted date, view count, images

**Croatian Field Names**: The database uses Croatian terminology (`broj_soba`, `povrsina`, `lokacija`, etc.) which the AI agent will intelligently map from English queries.

## 🔧 Available Commands

```bash
# Health monitoring
python -m src.realtor_buddy.cli.main health

# Configuration status
python -m src.realtor_buddy.cli.main config

# Property search (coming in Phase 2)
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

### 🚧 Phase 2: LangChain Implementation (Next)
- [ ] Schema analysis and Croatian field mapping
- [ ] LangChain SQL agent configuration
- [ ] Few-shot prompting with real estate examples
- [ ] Natural language query processing

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

### Phase 2: LangChain SQL Agent Implementation
3. **Schema Analysis & Documentation**
   - Generate comprehensive schema documentation for LangChain
   - Create field mapping between Croatian terms and English equivalents
   - Document common query patterns and expected value formats
   - Build sample query examples for training the agent

4. **LangChain SQL Chain Setup**
   - Initialize SQL database chain with MariaDB connection
   - Configure SQL agent with schema information and Croatian field mappings
   - Implement few-shot prompting with real estate domain examples
   - Add custom prompt templates for Croatian property terminology

5. **Natural Language Processing**
   - Build query intent classification (search, filter, aggregate)
   - Implement Croatian/English query support
   - Add location normalization (Croatian city/neighborhood names)
   - Create price range and property type standardization

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

## Example Queries to Support

- "Find apartments in Zagreb under 200,000 euros"
- "Show me houses with sea view in Split"
- "Properties with parking and elevator in city center"
- "New constructions from 2020 onwards with 3+ rooms"
- "Commercial properties for rent near tram lines"

## Technical Architecture

- **Database**: MariaDB with comprehensive Croatian property data
- **AI/LLM**: LangChain with SQL agent for query generation  
- **Language**: Python with async support for performance
- **Interface**: CLI initially, with potential web interface later
- **Deployment**: Docker containers for easy setup and deployment