"""Database connection manager for MariaDB/MySQL."""

import os
import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages database connections with connection pooling."""
    
    def __init__(self, 
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 database: Optional[str] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None):
        """Initialize database connection manager.
        
        Args:
            host: Database host (defaults to env DB_HOST)
            port: Database port (defaults to env DB_PORT)
            database: Database name (defaults to env DB_NAME)
            user: Database user (defaults to env DB_USER)
            password: Database password (defaults to env DB_PASSWORD)
        """
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or int(os.getenv('DB_PORT', '3306'))
        self.database = database or os.getenv('DB_NAME', 'njuskam_ultimate3')
        self.user = user or os.getenv('DB_USER', 'realtor_user')
        self.password = password or os.getenv('DB_PASSWORD', 'realtor_password')
        
        self._engine: Optional[Engine] = None
        
    @property
    def connection_string(self) -> str:
        """Get database connection string."""
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    @property
    def engine(self) -> Engine:
        """Get or create SQLAlchemy engine with connection pooling."""
        if self._engine is None:
            self._engine = create_engine(
                self.connection_string,
                poolclass=QueuePool,
                pool_size=5,
                pool_recycle=3600,  # Recycle connections after 1 hour
                pool_pre_ping=True,  # Validate connections before use
                echo=False  # Set to True for SQL query logging
            )
            logger.info("Database engine created")
        return self._engine
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager."""
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()
    
    def test_connection(self) -> bool:
        """Test database connectivity.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                result = conn.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def get_table_info(self, table_name: str = "agency_properties") -> Dict[str, Any]:
        """Get detailed table information for LangChain.
        
        Args:
            table_name: Name of the table to analyze
            
        Returns:
            Dictionary with table schema information
        """
        try:
            with self.get_connection() as conn:
                # Get column information
                columns_query = text("""
                    SELECT 
                        COLUMN_NAME,
                        DATA_TYPE,
                        IS_NULLABLE,
                        COLUMN_DEFAULT,
                        COLUMN_COMMENT
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = :database 
                    AND TABLE_NAME = :table_name
                    ORDER BY ORDINAL_POSITION
                """)
                
                columns_result = conn.execute(
                    columns_query, 
                    {"database": self.database, "table_name": table_name}
                )
                
                columns = [dict(row._mapping) for row in columns_result]
                
                # Get sample values for better LangChain understanding
                sample_query = text(f"SELECT * FROM {table_name} LIMIT 3")
                sample_result = conn.execute(sample_query)
                sample_data = [dict(row._mapping) for row in sample_result]
                
                return {
                    "table_name": table_name,
                    "columns": columns,
                    "sample_data": sample_data,
                    "row_count": self._get_row_count(conn, table_name)
                }
                
        except Exception as e:
            logger.error(f"Failed to get table info: {e}")
            return {}
    
    def _get_row_count(self, conn, table_name: str) -> int:
        """Get approximate row count for the table."""
        try:
            count_query = text(f"SELECT COUNT(*) FROM {table_name}")
            result = conn.execute(count_query)
            return result.fetchone()[0]
        except Exception as e:
            logger.warning(f"Could not get row count: {e}")
            return 0
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> list:
        """Execute a SQL query and return results.
        
        Args:
            query: SQL query to execute
            params: Optional query parameters
            
        Returns:
            List of dictionaries representing query results
        """
        try:
            with self.get_connection() as conn:
                result = conn.execute(text(query), params or {})
                return [dict(row._mapping) for row in result]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise


# Global database connection instance
db_connection = DatabaseConnection()