# services/safety_service.py
import math
from database import SafetyMapPoint
from sqlalchemy.orm import Session


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates in kilometers.
    Uses the Haversine formula.
    """
    R = 6371  # Earth's radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def query_safety_map(lat: float, lon: float, radius_km: float, db: Session) -> dict:
    """
    Query safety points within radius_km of the given coordinate.
    Returns the average safety index and list of points.
    """
    if radius_km <= 0:
        raise ValueError("Yarıçap sıfırdan büyük olmalıdır")

    all_points = db.query(SafetyMapPoint).all()
    nearby = []

    for point in all_points:
        dist = haversine_distance(lat, lon, point.latitude, point.longitude)
        if dist <= radius_km:
            nearby.append({
                "latitude": point.latitude,
                "longitude": point.longitude,
                "district": point.district,
                "city": point.city,
                "safety_index": point.safety_index,
                "distance_km": round(dist, 2)
            })

    if not nearby:
        return {"average_index": None, "points": [], "message": "Bu bölgede güvenlik verisi bulunamadı"}

    avg_index = round(sum(p["safety_index"] for p in nearby) / len(nearby))
    return {"average_index": avg_index, "points": nearby}
