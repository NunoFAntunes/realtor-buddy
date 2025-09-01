"""
Property Search API endpoints

FastAPI routes for natural language property search using the Croatian Real Estate SQL agent.
"""

import logging
import time
import json
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text

from ..models import SearchRequest, SearchResponse, PropertyResult
from ...langchain_agent.sql_agent import CroatianRealEstateAgent

logger = logging.getLogger(__name__)

router = APIRouter()


def get_agent() -> CroatianRealEstateAgent:
    """Dependency to get the SQL agent instance."""
    # Import here to avoid circular imports
    from ..main import get_agent as _get_agent
    return _get_agent()


def parse_image_urls(image_urls_json: str) -> List[str]:
    """Parse image URLs from JSON string in database."""
    if not image_urls_json:
        return []
    
    try:
        urls = json.loads(image_urls_json)
        if isinstance(urls, list):
            return [url for url in urls if isinstance(url, str)]
        return []
    except (json.JSONDecodeError, TypeError):
        return []


def format_property_result(row: Dict[str, Any]) -> PropertyResult:
    """Convert database row to PropertyResult model."""
    return PropertyResult(
        id=row.get('id'),
        title=row.get('title'),
        price=float(row.get('price')) if row.get('price') is not None else None,
        
        # Location
        lokacija=row.get('lokacija'),
        ulica=row.get('ulica'), 
        latitude=float(row.get('latitude')) if row.get('latitude') is not None else None,
        longitude=float(row.get('longitude')) if row.get('longitude') is not None else None,
        
        # Property details
        property_type=row.get('property_type'),
        broj_soba=row.get('broj_soba'),
        povrsina=row.get('povrsina'),
        kat=row.get('kat'),
        
        # Features
        lift=row.get('lift'),
        pogled_na_more=row.get('pogled_na_more'),
        energetski_razred=row.get('energetski_razred'),
        
        # Agency
        agency_name=row.get('agency_name'),
        agency_type=row.get('agency_type'),
        
        # Images and metadata
        image_urls=parse_image_urls(row.get('image_urls')),
        url=row.get('url'),
        view_count=row.get('view_count'),
        posted_date=row.get('posted_date')
    )


@router.post("/search", response_model=SearchResponse)
async def search_properties(
    request: SearchRequest,
    agent: CroatianRealEstateAgent = Depends(get_agent)
) -> SearchResponse:
    """
    Search for Croatian real estate properties using natural language.
    
    This endpoint accepts natural language queries like:
    - "apartments in Zagreb under 200,000 euros"  
    - "houses with sea view in Split"
    - "3 bedroom properties with elevator"
    
    The query is processed by a local Llama-3.1-8B model to generate SQL,
    which is then executed against the Croatian property database.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing search request: '{request.query}'")
        
        # Execute the natural language query using the SQL agent
        agent_result = agent.query(request.query)
        
        if not agent_result["success"]:
            logger.error(f"Agent query failed: {agent_result['error']}")
            return SearchResponse(
                success=False,
                query=request.query,
                error=agent_result["error"]
            )
        
        # Parse the raw database results  
        raw_result = agent_result["result"]
        sql_query = agent_result["sql_query"]
        
        logger.info(f"Generated SQL: {sql_query}")
        
        # If we have string results, we need to parse them into structured data
        properties = []
        
        if raw_result and isinstance(raw_result, str):
            # The agent returns text results, we need to re-execute to get structured data
            try:
                # Get database connection from agent
                db_connection = agent.db
                
                # Execute the SQL query directly to get structured results
                if sql_query:
                    # Ensure we have all the fields we need in the SELECT
                    if "SELECT *" in sql_query:
                        # Replace SELECT * with specific fields for better control
                        enhanced_sql = sql_query.replace(
                            "SELECT *", 
                            """SELECT id, title, price, lokacija, ulica, latitude, longitude,
                                      property_type, broj_soba, povrsina, kat, lift, pogled_na_more,
                                      energetski_razred, agency_name, agency_type, image_urls, 
                                      url, view_count, posted_date"""
                        )
                    else:
                        enhanced_sql = sql_query
                    
                    # Apply limit if not already present
                    if "LIMIT" not in enhanced_sql.upper():
                        enhanced_sql += f" LIMIT {request.limit}"
                    
                    # Execute query
                    result = db_connection.run(enhanced_sql)
                    
                    # Parse results - the LangChain SQLDatabase returns string results
                    # We need to manually execute to get structured data
                    with db_connection._engine.connect() as connection:
                        db_result = connection.execute(text(enhanced_sql))
                        rows = db_result.fetchall()
                        
                        # Convert to dictionaries
                        columns = db_result.keys()
                        for row in rows:
                            row_dict = dict(zip(columns, row))
                            property_result = format_property_result(row_dict)
                            properties.append(property_result)
                            
            except Exception as e:
                logger.error(f"Failed to parse database results: {e}")
                # Return the raw result as an error for debugging
                return SearchResponse(
                    success=False,
                    query=request.query,
                    sql_query=sql_query,
                    error=f"Failed to parse database results: {str(e)}"
                )
        
        processing_time = time.time() - start_time
        
        logger.info(f"Search completed: {len(properties)} properties found in {processing_time:.2f}s")
        
        return SearchResponse(
            success=True,
            query=request.query,
            results=properties,
            total_results=len(properties),
            sql_query=sql_query,
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        error_msg = f"Search failed: {str(e)}"
        logger.error(error_msg)
        
        return SearchResponse(
            success=False,
            query=request.query,
            error=error_msg,
            processing_time=processing_time
        )


@router.get("/search/examples")
async def get_search_examples():
    """Get example search queries for user guidance."""
    return {
        "examples": [
            {
                "query": "apartments in Zagreb under 200,000 euros",
                "description": "Find affordable apartments in Croatia's capital city"
            },
            {
                "query": "houses with sea view in Split",
                "description": "Find houses with beautiful sea views in Split"
            },
            {
                "query": "3 bedroom properties with elevator",
                "description": "Find family-sized properties with elevator access"
            },
            {
                "query": "new construction from 2020 onwards",
                "description": "Find recently built properties"
            },
            {
                "query": "properties with parking in city center",
                "description": "Find properties with parking in downtown areas"
            },
            {
                "query": "ground floor apartments with balcony",
                "description": "Find accessible apartments with outdoor space"
            }
        ]
    }