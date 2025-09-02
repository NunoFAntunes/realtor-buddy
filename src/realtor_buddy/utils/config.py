"""Configuration management utilities."""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration management."""
    
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_NAME = os.getenv('DB_NAME', 'njuskam_ultimate3')
    DB_USER = os.getenv('DB_USER', 'realtor_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'realtor_password')
    
    # LangChain / LLM configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')  # openai, anthropic
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4.1')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.1'))
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    MAX_QUERY_RESULTS = int(os.getenv('MAX_QUERY_RESULTS', '50'))
    QUERY_TIMEOUT = int(os.getenv('QUERY_TIMEOUT', '30'))
    
    # CLI settings
    CLI_HISTORY_SIZE = int(os.getenv('CLI_HISTORY_SIZE', '100'))
    CLI_PAGER = os.getenv('CLI_PAGER', 'auto')
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status.
        
        Returns:
            Dictionary with validation results
        """
        issues = []
        warnings = []
        
        # Check required LLM API keys
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            issues.append("No LLM API key provided. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
        
        # Validate LLM provider
        if cls.LLM_PROVIDER not in ['openai', 'anthropic']:
            warnings.append(f"Unknown LLM provider: {cls.LLM_PROVIDER}. Using 'openai'")
            cls.LLM_PROVIDER = 'openai'
        
        # Check if selected provider has API key
        if cls.LLM_PROVIDER == 'openai' and not cls.OPENAI_API_KEY:
            if cls.ANTHROPIC_API_KEY:
                warnings.append("OpenAI key not found, switching to Anthropic")
                cls.LLM_PROVIDER = 'anthropic'
            else:
                issues.append("OpenAI provider selected but OPENAI_API_KEY not set")
        
        if cls.LLM_PROVIDER == 'anthropic' and not cls.ANTHROPIC_API_KEY:
            if cls.OPENAI_API_KEY:
                warnings.append("Anthropic key not found, switching to OpenAI")
                cls.LLM_PROVIDER = 'openai'
            else:
                issues.append("Anthropic provider selected but ANTHROPIC_API_KEY not set")
        
        # Validate numeric settings
        if cls.LLM_TEMPERATURE < 0 or cls.LLM_TEMPERATURE > 1:
            warnings.append(f"Invalid temperature {cls.LLM_TEMPERATURE}, using 0.1")
            cls.LLM_TEMPERATURE = 0.1
        
        if cls.MAX_QUERY_RESULTS <= 0:
            warnings.append(f"Invalid MAX_QUERY_RESULTS {cls.MAX_QUERY_RESULTS}, using 50")
            cls.MAX_QUERY_RESULTS = 50
        
        if cls.QUERY_TIMEOUT <= 0:
            warnings.append(f"Invalid QUERY_TIMEOUT {cls.QUERY_TIMEOUT}, using 30")
            cls.QUERY_TIMEOUT = 30
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    @classmethod
    def get_db_config(cls) -> Dict[str, Any]:
        """Get database configuration dictionary."""
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "database": cls.DB_NAME,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD
        }
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration dictionary."""
        return {
            "provider": cls.LLM_PROVIDER,
            "model": cls.LLM_MODEL,
            "temperature": cls.LLM_TEMPERATURE,
            "api_key": cls.OPENAI_API_KEY if cls.LLM_PROVIDER == 'openai' else cls.ANTHROPIC_API_KEY
        }
    
    @classmethod
    def setup_logging(cls):
        """Configure application logging."""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL, logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Reduce noise from some third-party libraries
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)


# Initialize logging
Config.setup_logging()