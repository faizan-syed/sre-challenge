import logging
import os
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SRE Challenge FastAPI Application",
    description="A simple FastAPI application for the SRE Challenge",
    version="1.0.0",
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # In production, specify actual hosts
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str


@app.get("/", response_model=dict)
def read_root():
    """Root endpoint returning a simple greeting"""
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        environment=os.getenv("ENVIRONMENT", "unknown"),
        version="1.0.0",
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """Get item by ID with optional query parameter"""
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")

    logger.info(f"Item endpoint accessed: item_id={item_id}, q={q}")
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update item by ID"""
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")

    logger.info(f"Item update endpoint accessed: item_id={item_id}")
    return {"item_name": item.name, "item_id": item_id}


@app.get("/data")
def data():
    """Get environment configuration data"""
    logger.info("Data endpoint accessed")

    # In production, sensitive data should not be exposed like this
    # This is for demo purposes only
    return {
        "DB_PASSWORD": (
            "***" if os.getenv("DB_PASSWORD") else None
        ),  # Masked for security
        "API_BASE_URL": os.getenv("API_BASE_URL"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "MAX_CONNECTIONS": os.getenv("MAX_CONNECTIONS"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT"),
    }
