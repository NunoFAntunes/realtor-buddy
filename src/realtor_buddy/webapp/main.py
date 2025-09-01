"""
Croatian Real Estate FastAPI Web Application

Main FastAPI application for the Croatian real estate search system using local Llama-3.1-8B.
"""

import logging
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any
import time
import traceback
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

from .models import SearchRequest, SearchResponse, HealthResponse, ErrorResponse, PropertyResult
from .api.search import router as search_router
from .api.health import router as health_router
from ..langchain_agent.sql_agent import CroatianRealEstateAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global agent instance
sql_agent: CroatianRealEstateAgent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup/shutdown tasks."""
    logger.info("Starting Croatian Real Estate Web Application...")
    
    # Startup: Initialize SQL agent
    global sql_agent
    try:
        logger.info("Initializing Croatian Real Estate SQL Agent...")
        sql_agent = CroatianRealEstateAgent()
        
        # Initialize in background to avoid blocking startup
        def init_agent():
            try:
                sql_agent.initialize()
                logger.info("SQL Agent initialization completed successfully")
            except Exception as e:
                logger.error(f"SQL Agent initialization failed: {e}")
                
        # Run initialization in background
        asyncio.create_task(asyncio.to_thread(init_agent))
        
    except Exception as e:
        logger.error(f"Failed to create SQL Agent: {e}")
        sql_agent = None
    
    logger.info("Web application startup completed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Croatian Real Estate Web Application...")
    # Cleanup if needed
    logger.info("Shutdown completed")


# Create FastAPI app
app = FastAPI(
    title="Croatian Real Estate Search",
    description="AI-powered Croatian real estate search using local Llama-3.1-8B model",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="src/realtor_buddy/webapp/static"), name="static")
except RuntimeError:
    logger.warning("Static directory not found, skipping static file mounting")

# Setup templates
try:
    templates = Jinja2Templates(directory="src/realtor_buddy/webapp/templates")
except Exception as e:
    logger.warning(f"Templates directory not found: {e}")
    templates = None


# Include API routers
app.include_router(search_router, prefix="/api", tags=["search"])
app.include_router(health_router, prefix="/api", tags=["health"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main search page."""
    if templates is None:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Croatian Real Estate Search</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .search-box { width: 100%; padding: 15px; font-size: 16px; border: 2px solid #ddd; border-radius: 8px; }
                .search-btn { padding: 15px 30px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; }
                .search-btn:hover { background: #0056b3; }
                .property-card { border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 8px; }
                .price { font-size: 20px; font-weight: bold; color: #007bff; }
                .location { color: #666; margin: 5px 0; }
                .features { margin: 10px 0; }
                .loading { text-align: center; margin: 20px 0; }
            </style>
        </head>
        <body>
            <h1>🏠 Croatian Real Estate Search</h1>
            <p>Search for properties using natural language. Try queries like:</p>
            <ul>
                <li>"apartments in Zagreb under 200,000 euros"</li>
                <li>"houses with sea view in Split"</li>
                <li>"3 bedroom properties with elevator"</li>
            </ul>
            
            <div style="margin: 30px 0;">
                <input type="text" id="searchQuery" class="search-box" placeholder="Enter your property search...">
                <br><br>
                <button onclick="searchProperties()" class="search-btn">Search Properties</button>
            </div>
            
            <div id="loading" class="loading" style="display:none;">
                <p>🤖 Processing your query with AI... This may take a few moments.</p>
            </div>
            
            <div id="results"></div>
            
            <script>
                async function searchProperties() {
                    const query = document.getElementById('searchQuery').value;
                    if (!query.trim()) return;
                    
                    const loading = document.getElementById('loading');
                    const results = document.getElementById('results');
                    
                    loading.style.display = 'block';
                    results.innerHTML = '';
                    
                    try {
                        const response = await fetch('/api/search', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ query: query })
                        });
                        
                        const data = await response.json();
                        loading.style.display = 'none';
                        
                        if (data.success && data.results.length > 0) {
                            results.innerHTML = '<h3>Found ' + data.total_results + ' properties:</h3>';
                            data.results.forEach(property => {
                                const card = createPropertyCard(property);
                                results.appendChild(card);
                            });
                        } else if (data.success) {
                            results.innerHTML = '<p>No properties found matching your criteria.</p>';
                        } else {
                            results.innerHTML = '<p style="color: red;">Error: ' + data.error + '</p>';
                        }
                    } catch (error) {
                        loading.style.display = 'none';
                        results.innerHTML = '<p style="color: red;">Failed to search properties: ' + error.message + '</p>';
                    }
                }
                
                function createPropertyCard(property) {
                    const card = document.createElement('div');
                    card.className = 'property-card';
                    
                    const price = property.price ? '€' + property.price.toLocaleString() : 'Price not available';
                    const location = property.lokacija || 'Location not specified';
                    const rooms = property.broj_soba || 'N/A';
                    const area = property.povrsina || 'N/A';
                    const floor = property.kat || 'N/A';
                    
                    card.innerHTML = `
                        <div class="price">${price}</div>
                        <div class="location">📍 ${location}</div>
                        <h4>${property.title || 'Property #' + property.id}</h4>
                        <div class="features">
                            <span>🛏️ ${rooms} rooms</span> | 
                            <span>📐 ${area}m²</span> | 
                            <span>🏢 Floor: ${floor}</span>
                        </div>
                        ${property.agency_name ? '<p><strong>Agency:</strong> ' + property.agency_name + '</p>' : ''}
                    `;
                    
                    return card;
                }
                
                // Allow Enter key to trigger search
                document.getElementById('searchQuery').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        searchProperties();
                    }
                });
            </script>
        </body>
        </html>
        """)
    
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Global HTTP exception handler."""
    return ErrorResponse(
        error=exc.detail,
        error_type="HTTPException",
        request_id=getattr(request.state, 'request_id', None)
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors."""
    logger.error(f"Unexpected error processing request: {exc}")
    logger.error(traceback.format_exc())
    
    return ErrorResponse(
        error="An unexpected error occurred",
        error_type=type(exc).__name__,
        request_id=getattr(request.state, 'request_id', None)
    )


def get_agent() -> CroatianRealEstateAgent:
    """Get the global SQL agent instance."""
    global sql_agent
    if sql_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="SQL Agent not initialized. Please wait and try again."
        )
    return sql_agent


if __name__ == "__main__":
    uvicorn.run(
        "src.realtor_buddy.webapp.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )