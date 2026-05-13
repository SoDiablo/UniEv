# services/match_service.py
from database import User, Profile
from sqlalchemy.orm import Session


def calculate_match_score(user_profile: Profile, candidate_profile: Profile) -> int:
    """
    Calculates roommate compatibility score.
    
    Range is 50-100 (not 0-100 as misleadingly stated in SRS Section 2).
    Base score: 50
    Each matching criterion adds 10 points.
    
    Criteria:
    1. Budget overlap: user1's range overlaps with user2's range
    2. Smoking preference matches
    3. Pet preference matches
    4. Sleep schedule matches
    5. Cleanliness level matches
    """
    score = 50  # Base score

    # 1. Budget overlap
    if (user_profile.budget_min is not None and user_profile.budget_max is not None and
        candidate_profile.budget_min is not None and candidate_profile.budget_max is not None):
        if (user_profile.budget_min <= candidate_profile.budget_max and
                candidate_profile.budget_min <= user_profile.budget_max):
            score += 10

    # 2. Smoking
    if (user_profile.smoking_ok is not None and candidate_profile.smoking_ok is not None and
            user_profile.smoking_ok == candidate_profile.smoking_ok):
        score += 10

    # 3. Pets
    if (user_profile.pet_ok is not None and candidate_profile.pet_ok is not None and
            user_profile.pet_ok == candidate_profile.pet_ok):
        score += 10

    # 4. Sleep schedule
    if (user_profile.sleep_schedule and candidate_profile.sleep_schedule and
            user_profile.sleep_schedule == candidate_profile.sleep_schedule):
        score += 10

    # 5. Cleanliness
    if (user_profile.cleanliness and candidate_profile.cleanliness and
            user_profile.cleanliness == candidate_profile.cleanliness):
        score += 10

    return min(100, score)  # Safety cap at 100


def get_matches(current_user: User, db: Session) -> list:
    """
    Returns top 20 users sorted by compatibility score.
    
    Filters:
    - Exclude current user
    - Exclude suspended users
    - Require profile to exist
    - Require verified users only (as per specification)
    """
    # Require current user to have a profile
    if not current_user.profile:
        return []

    # Get all eligible candidates
    candidates = (
        db.query(User)
        .join(Profile, User.id == Profile.user_id)
        .filter(
            User.id != current_user.id,
            User.is_suspended == False,
            User.is_verified == True,  # Only verified users as per specification
            User.role == "STUDENT",  # Only show students in match results
        )
        .all()
    )

    results = []
    for candidate in candidates:
        if not candidate.profile:
            continue
        score = calculate_match_score(current_user.profile, candidate.profile)
        results.append({
            "user_id": candidate.id,
            "first_name": candidate.first_name,
            "last_name": candidate.last_name[0] + "." if candidate.last_name else "",
            "score": score,
            "bio": candidate.profile.bio,
            "budget_min": candidate.profile.budget_min,
            "budget_max": candidate.profile.budget_max,
            "smoking_ok": candidate.profile.smoking_ok,
            "pet_ok": candidate.profile.pet_ok,
            "sleep_schedule": candidate.profile.sleep_schedule,
            "cleanliness": candidate.profile.cleanliness,
        })

    # Sort by score descending, return top 20
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:20]
