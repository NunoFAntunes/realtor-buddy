"""Database health check utilities."""

import logging
import time
from typing import Dict, Any, List
from datetime import datetime

from .connection import db_connection

logger = logging.getLogger(__name__)


class DatabaseHealthChecker:
    """Comprehensive database health checking."""
    
    def __init__(self):
        self.db = db_connection
    
    def check_connectivity(self) -> Dict[str, Any]:
        """Check basic database connectivity.
        
        Returns:
            Dictionary with connectivity status and metrics
        """
        start_time = time.time()
        
        try:
            is_connected = self.db.test_connection()
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return {
                "status": "healthy" if is_connected else "unhealthy",
                "connected": is_connected,
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "connected": False,
                "error": str(e),
                "response_time_ms": (time.time() - start_time) * 1000,
                "timestamp": datetime.now().isoformat()
            }
    
    def check_table_existence(self, table_name: str = "agency_properties") -> Dict[str, Any]:
        """Check if the main table exists and is accessible.
        
        Args:
            table_name: Name of table to check
            
        Returns:
            Dictionary with table status information
        """
        try:
            table_info = self.db.get_table_info(table_name)
            
            if not table_info:
                return {
                    "status": "error",
                    "table_exists": False,
                    "error": f"Table {table_name} not found or inaccessible"
                }
            
            return {
                "status": "healthy",
                "table_exists": True,
                "table_name": table_name,
                "column_count": len(table_info.get("columns", [])),
                "row_count": table_info.get("row_count", 0),
                "has_sample_data": len(table_info.get("sample_data", [])) > 0
            }
            
        except Exception as e:
            return {
                "status": "error",
                "table_exists": False,
                "error": str(e)
            }
    
    def check_data_quality(self, table_name: str = "agency_properties") -> Dict[str, Any]:
        """Perform basic data quality checks.
        
        Args:
            table_name: Name of table to check
            
        Returns:
            Dictionary with data quality metrics
        """
        try:
            # Check for basic data completeness
            quality_checks = []
            
            # Check if we have recent data
            recent_data_query = f"""
                SELECT COUNT(*) as count 
                FROM {table_name} 
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                OR last_updated >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            """
            
            recent_count = self.db.execute_query(recent_data_query)[0]["count"]
            quality_checks.append({
                "check": "recent_data",
                "status": "pass" if recent_count > 0 else "warning",
                "value": recent_count,
                "description": "Properties updated in last 30 days"
            })
            
            # Check for properties with prices
            price_query = f"SELECT COUNT(*) as count FROM {table_name} WHERE price IS NOT NULL AND price > 0"
            price_count = self.db.execute_query(price_query)[0]["count"]
            
            total_count = self.db.execute_query(f"SELECT COUNT(*) as count FROM {table_name}")[0]["count"]
            price_percentage = (price_count / total_count * 100) if total_count > 0 else 0
            
            quality_checks.append({
                "check": "price_completeness",
                "status": "pass" if price_percentage >= 80 else "warning",
                "value": round(price_percentage, 1),
                "description": "Percentage of properties with valid prices"
            })
            
            # Check for location data
            location_query = f"""
                SELECT COUNT(*) as count 
                FROM {table_name} 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """
            location_count = self.db.execute_query(location_query)[0]["count"]
            location_percentage = (location_count / total_count * 100) if total_count > 0 else 0
            
            quality_checks.append({
                "check": "location_completeness",
                "status": "pass" if location_percentage >= 70 else "warning",
                "value": round(location_percentage, 1),
                "description": "Percentage of properties with GPS coordinates"
            })
            
            overall_status = "healthy" if all(check["status"] == "pass" for check in quality_checks) else "warning"
            
            return {
                "status": overall_status,
                "total_properties": total_count,
                "quality_checks": quality_checks,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def comprehensive_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of the database.
        
        Returns:
            Dictionary with complete health status
        """
        logger.info("Starting comprehensive database health check")
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy"
        }
        
        # Connectivity check
        connectivity = self.check_connectivity()
        health_status["connectivity"] = connectivity
        
        if connectivity["status"] != "healthy":
            health_status["overall_status"] = "unhealthy"
            return health_status
        
        # Table existence check
        table_check = self.check_table_existence()
        health_status["table_status"] = table_check
        
        if table_check["status"] != "healthy":
            health_status["overall_status"] = "unhealthy"
            return health_status
        
        # Data quality check
        data_quality = self.check_data_quality()
        health_status["data_quality"] = data_quality
        
        if data_quality["status"] == "error":
            health_status["overall_status"] = "unhealthy"
        elif data_quality["status"] == "warning":
            health_status["overall_status"] = "warning"
        
        logger.info(f"Health check completed with status: {health_status['overall_status']}")
        return health_status


# Global health checker instance
health_checker = DatabaseHealthChecker()