import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Destination, Package, Hotel, TransportOption, Inquiry, Newsletter, Testimonial

app = FastAPI(title="Travel Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Travel Platform API is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# ---------- Public Content Endpoints ----------
@app.get("/api/destinations", response_model=List[Destination])
def list_destinations(limit: Optional[int] = 50):
    try:
        docs = get_documents("destination", {}, limit)
        return [Destination(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception:
        # return sample static fallback if DB not configured
        sample = [
            Destination(name="Kedarnath", state="Uttarakhand", description="One of the holiest Char Dham shrines.", image_url="https://images.unsplash.com/photo-1583413230541-9b5f2a5c6cfb", tags=["yatra", "temple", "himalayas"]),
            Destination(name="Badrinath", state="Uttarakhand", description="Sacred town in Chamoli district.", image_url="https://images.unsplash.com/photo-1603262110263-fb0112e7cc33", tags=["char dham", "alakananda"]) ,
        ]
        return sample[: limit or 2]


@app.get("/api/packages", response_model=List[Package])
def list_packages(limit: Optional[int] = 50):
    try:
        docs = get_documents("package", {}, limit)
        return [Package(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception:
        sample = [
            Package(title="Kedarnath Yatra 3N/4D", destination="Kedarnath", duration_days=4, price=12999, highlights=["Helicopter assist", "VIP darshan"], inclusions=["Hotel", "Transport", "Meals"], image_url="https://images.unsplash.com/photo-1512453979798-5ea266f8880c", is_featured=True),
            Package(title="Char Dham Express 9N/10D", destination="Uttarakhand", duration_days=10, price=45999, highlights=["All 4 shrines", "Experienced guide"], inclusions=["Hotels", "Transport", "Breakfast"], image_url="https://images.unsplash.com/photo-1544735716-392fe2489ffa", is_featured=True),
        ]
        return sample[: limit or 2]


@app.get("/api/hotels", response_model=List[Hotel])
def list_hotels(limit: Optional[int] = 50):
    try:
        docs = get_documents("hotel", {}, limit)
        return [Hotel(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception:
        sample = [
            Hotel(name="Himalayan View Inn", destination="Guptkashi", stars=3, price_per_night=2200, amenities=["WiFi", "Hot Water"], image_url="https://images.unsplash.com/photo-1551776235-dde6d4829808"),
            Hotel(name="Char Dham Residency", destination="Joshimath", stars=4, price_per_night=3800, amenities=["Breakfast", "Parking"], image_url="https://images.unsplash.com/photo-1566073771259-6a8506099945"),
        ]
        return sample[: limit or 2]


@app.get("/api/transport", response_model=List[TransportOption])
def list_transport(limit: Optional[int] = 50):
    try:
        docs = get_documents("transportoption", {}, limit)
        return [TransportOption(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception:
        sample = [
            TransportOption(type="car", origin="Dehradun", destination="Kedarnath", seats=4, price=5999, operator="InstantRides"),
            TransportOption(type="bus", origin="Haridwar", destination="Badrinath", seats=45, price=899, operator="YatraBus"),
        ]
        return sample[: limit or 2]


# ---------- Lead capture endpoints ----------
@app.post("/api/inquiry")
def create_inquiry(payload: Inquiry):
    try:
        doc_id = create_document("inquiry", payload)
        return {"status": "ok", "id": doc_id}
    except Exception:
        # fallback without DB: succeed but no persistence
        return {"status": "ok", "id": None}


@app.post("/api/newsletter")
def subscribe_newsletter(payload: Newsletter):
    try:
        doc_id = create_document("newsletter", payload)
        return {"status": "ok", "id": doc_id}
    except Exception:
        return {"status": "ok", "id": None}


@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials(limit: Optional[int] = 10):
    try:
        docs = get_documents("testimonial", {}, limit)
        return [Testimonial(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]
    except Exception:
        sample = [
            Testimonial(name="Rahul", text="Seamless Kedarnath yatra, great arrangements!", rating=5, location="Delhi"),
            Testimonial(name="Sneha", text="Quick hotel booking and polite support.", rating=4, location="Mumbai"),
        ]
        return sample[: limit or 2]


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
