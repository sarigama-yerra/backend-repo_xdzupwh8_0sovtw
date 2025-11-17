"""
Database Schemas for Travel Platform

Each Pydantic model represents a MongoDB collection. The collection name is the lowercase
of the class name, e.g. Package -> "package".
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal


class Destination(BaseModel):
    name: str = Field(..., description="Destination name e.g., Kedarnath")
    state: str = Field(..., description="Indian state")
    description: Optional[str] = Field(None, description="Short description")
    image_url: Optional[str] = Field(None, description="Hero image URL")
    tags: List[str] = Field(default_factory=list, description="Tags/keywords")


class Package(BaseModel):
    title: str = Field(..., description="Package title")
    destination: str = Field(..., description="Destination name")
    duration_days: int = Field(..., ge=1, description="Number of days")
    price: float = Field(..., ge=0, description="Base price per person")
    highlights: List[str] = Field(default_factory=list)
    inclusions: List[str] = Field(default_factory=list)
    exclusions: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    is_featured: bool = Field(default=False)


class Hotel(BaseModel):
    name: str
    destination: str
    stars: int = Field(ge=1, le=5)
    price_per_night: float = Field(ge=0)
    amenities: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    contact_phone: Optional[str] = None


class TransportOption(BaseModel):
    type: Literal["car", "bus", "tempo", "helicopter", "train"]
    origin: str
    destination: str
    seats: int = Field(ge=1)
    price: float = Field(ge=0)
    operator: Optional[str] = None


class Inquiry(BaseModel):
    name: str
    email: EmailStr
    phone: str
    service_type: Literal["package", "hotel", "transport", "custom"]
    message: Optional[str] = None
    package_id: Optional[str] = None
    travel_dates: Optional[str] = None
    travelers: Optional[int] = Field(default=1, ge=1)


class Newsletter(BaseModel):
    email: EmailStr


class Testimonial(BaseModel):
    name: str
    text: str
    rating: int = Field(ge=1, le=5)
    location: Optional[str] = None
