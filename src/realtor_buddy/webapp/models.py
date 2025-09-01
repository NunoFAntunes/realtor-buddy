"""
Pydantic models for Croatian Real Estate Web API

Request and response models for the FastAPI web application.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SearchRequest(BaseModel):
    """Request model for property search endpoint."""
    
    query: str = Field(
        ..., 
        description="Natural language property search query",
        example="Find apartments in Zagreb under 200,000 euros"
    )
    limit: Optional[int] = Field(
        20, 
        ge=1, 
        le=100, 
        description="Maximum number of results to return"
    )


class PropertyResult(BaseModel):
    """Individual property result from database."""
    
    id: int = Field(..., description="Unique property ID")
    title: Optional[str] = Field(None, description="Property title/headline")
    price: Optional[float] = Field(None, description="Property price in EUR")
    
    # Location information
    lokacija: Optional[str] = Field(None, description="Location description in Croatian")
    ulica: Optional[str] = Field(None, description="Street address")
    latitude: Optional[float] = Field(None, description="GPS latitude coordinate")
    longitude: Optional[float] = Field(None, description="GPS longitude coordinate")
    
    # Property details
    property_type: Optional[str] = Field(None, description="Property type")
    broj_soba: Optional[str] = Field(None, description="Number of bedrooms/rooms")
    povrsina: Optional[str] = Field(None, description="Surface area in m²")
    kat: Optional[str] = Field(None, description="Floor level")
    
    # Features
    lift: Optional[str] = Field(None, description="Elevator availability (da/ne)")
    pogled_na_more: Optional[str] = Field(None, description="Sea view (da/ne)")
    energetski_razred: Optional[str] = Field(None, description="Energy rating")
    
    # Agency information
    agency_name: Optional[str] = Field(None, description="Real estate agency name")
    agency_type: Optional[str] = Field(None, description="Agency type")
    
    # Images and metadata
    image_urls: Optional[List[str]] = Field(None, description="Property image URLs")
    url: Optional[str] = Field(None, description="Original listing URL")
    view_count: Optional[int] = Field(None, description="Number of views")
    posted_date: Optional[str] = Field(None, description="When listing was posted")


class SearchResponse(BaseModel):
    """Response model for property search endpoint."""
    
    success: bool = Field(..., description="Whether the search was successful")
    query: str = Field(..., description="Original search query")
    
    # Results
    results: List[PropertyResult] = Field(
        default_factory=list, 
        description="List of matching properties"
    )
    total_results: int = Field(0, description="Total number of properties found")
    
    # Query processing info
    sql_query: Optional[str] = Field(None, description="Generated SQL query")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    
    # Error information
    error: Optional[str] = Field(None, description="Error message if search failed")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Overall system status")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Component health
    database: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Database connection status"
    )
    llm_model: Dict[str, Any] = Field(
        default_factory=dict, 
        description="LLM model status"
    )
    
    # System info
    system_info: Optional[Dict[str, Any]] = Field(
        None, 
        description="System information (GPU, memory, etc.)"
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Type of error")
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = Field(None, description="Request identifier for debugging")