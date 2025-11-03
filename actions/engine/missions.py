from datetime import datetime
import json
from .utils import load_json, get_content_path
from .db import add_xp


def daily_mission(age_range: str | None = None) -> dict:
    data = load_json(get_content_path("missions_weekly.json"), {"daily": [], "weekly": []})
    daily = data.get("daily", [])
    if not daily:
        return {"title": "Lee un versículo", "description": "Lee y comparte un versículo que te inspire hoy."}
    idx = int(datetime.utcnow().strftime("%j")) % len(daily)
    return daily[idx]


def weekly_mission(age_range: str | None = None) -> dict:
    data = load_json(get_content_path("missions_weekly.json"), {"daily": [], "weekly": []})
    weekly = data.get("weekly", [])
    if not weekly:
        return {"title": "Aprende un Salmo", "description": "Memoriza un verso del Salmo 23 esta semana."}
    idx = int(datetime.utcnow().strftime("%U")) % len(weekly)
    return weekly[idx]


def complete_mission(user_id: str, mission: dict) -> None:
    add_xp(user_id, "mission_complete", 20, json.dumps({"title": mission.get("title")}))


