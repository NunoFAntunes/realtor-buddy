"""
Health Check API endpoints

FastAPI routes for system health monitoring and status checks.
"""

import logging
import psutil
import torch
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy import text

from ..models import HealthResponse
from ...langchain_agent.sql_agent import CroatianRealEstateAgent
from ...utils.config import get_database_config

logger = logging.getLogger(__name__)

router = APIRouter()


def get_agent() -> CroatianRealEstateAgent:
    """Dependency to get the SQL agent instance."""
    from ..main import get_agent as _get_agent
    return _get_agent()


def check_database_health() -> Dict[str, Any]:
    """Check database connectivity and basic stats."""
    try:
        # Get database config
        db_config = get_database_config()
        
        # Try to get agent and test connection
        from ..main import sql_agent
        if sql_agent and sql_agent.db:
            # Test basic query
            result = sql_agent.db.run("SELECT COUNT(*) as total FROM agency_properties LIMIT 1")
            
            return {
                "status": "healthy",
                "connected": True,
                "database": db_config["database"],
                "host": db_config["host"],
                "test_query_result": result
            }
        else:
            return {
                "status": "unhealthy", 
                "connected": False,
                "error": "Database connection not available"
            }
            
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }


def check_llm_model_health(agent: CroatianRealEstateAgent = None) -> Dict[str, Any]:
    """Check LLM model status and availability."""
    try:
        if agent is None or not hasattr(agent, 'llm') or agent.llm is None:
            return {
                "status": "unhealthy",
                "loaded": False,
                "error": "LLM model not loaded"
            }
        
        # Check if model is loaded
        model_info = {
            "status": "healthy",
            "loaded": True,
            "model_name": agent.model_name,
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        }
        
        # Add GPU info if available
        if torch.cuda.is_available():
            model_info.update({
                "gpu_name": torch.cuda.get_device_name(0),
                "gpu_memory_total": torch.cuda.get_device_properties(0).total_memory,
                "gpu_memory_allocated": torch.cuda.memory_allocated(0),
                "gpu_memory_cached": torch.cuda.memory_reserved(0)
            })
        
        return model_info
        
    except Exception as e:
        logger.error(f"LLM model health check failed: {e}")
        return {
            "status": "unhealthy",
            "loaded": False,
            "error": str(e)
        }


def get_system_info() -> Dict[str, Any]:
    """Get basic system information."""
    try:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "disk_usage_percent": psutil.disk_usage('/').percent if hasattr(psutil.disk_usage('/'), 'percent') else None,
            "python_version": f"{psutil.version_info.major}.{psutil.version_info.minor}",
            "torch_version": torch.__version__ if torch else None,
            "cuda_available": torch.cuda.is_available() if torch else False
        }
    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        return {"error": str(e)}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check for the Croatian Real Estate application.
    
    Checks:
    - Database connectivity and basic stats
    - LLM model status and GPU availability
    - System resources (CPU, memory, disk)
    """
    try:
        # Get agent if available (don't fail if not ready)
        agent = None
        try:
            from ..main import sql_agent
            agent = sql_agent
        except Exception:
            pass
        
        # Check all components
        database_health = check_database_health()
        llm_health = check_llm_model_health(agent)
        system_info = get_system_info()
        
        # Determine overall status
        overall_status = "healthy"
        if (database_health.get("status") != "healthy" or 
            llm_health.get("status") != "healthy"):
            overall_status = "degraded"
            
        return HealthResponse(
            status=overall_status,
            database=database_health,
            llm_model=llm_health,
            system_info=system_info
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            database={"status": "unknown", "error": str(e)},
            llm_model={"status": "unknown", "error": str(e)}
        )


@router.get("/health/database")
async def database_health():
    """Quick database-only health check."""
    return check_database_health()


@router.get("/health/llm")
async def llm_health():
    """Quick LLM model-only health check."""
    try:
        from ..main import sql_agent
        return check_llm_model_health(sql_agent)
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.get("/health/system")
async def system_health():
    """Quick system-only health check."""
    return get_system_info()