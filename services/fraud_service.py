# services/fraud_service.py
import json

def calculate_fraud_score(listing, owner) -> tuple[int, dict]:
    """
    Calculates fraud risk score for a listing.
    
    Lower score = MORE trustworthy (counter-intuitive naming in SRS — we keep it).
    Score starts at 0. Higher = more suspicious.
    Max possible: 65. We cap at 100.
    
    Factors (add points = more suspicious):
    - Short description (< 100 chars): +15
    - No photos: +20
    - No location (lat/lon): +10
    - Suspicious price (< 1000 TL or > 50000 TL): +5
    - Contains "acil" (urgent) in title/description: +5
    
    Factors (subtract points = more trustworthy):
    - Owner has other active listings: -10
    """
    score = 0
    factors = {}

    # Short description
    if len(listing.description or "") < 100:
        score += 15
        factors["short_description"] = "+15 (açıklama çok kısa)"

    # No photos (checked via relationship)
    if not listing.photos:
        score += 20
        factors["no_photos"] = "+20 (fotoğraf yok)"

    # No location
    if not listing.latitude or not listing.longitude:
        score += 10
        factors["no_location"] = "+10 (konum bilgisi eksik)"

    # Suspicious price
    if listing.price < 1000 or listing.price > 50000:
        score += 5
        factors["suspicious_price"] = "+5 (şüpheli fiyat aralığı)"

    # "Acil" (urgent) keyword
    text = f"{listing.title} {listing.description}".lower()
    if "acil" in text:
        score += 5
        factors["urgent_keyword"] = '+5 ("acil" ifadesi kullanılmış)'

    # Trust bonus: owner has other listings
    if owner and hasattr(owner, "listings") and len(owner.listings) > 1:
        score -= 10
        factors["experienced_owner"] = "-10 (ev sahibinin başka ilanı var)"

    # Clamp between 0 and 100
    score = max(0, min(100, score))

    return score, factors
