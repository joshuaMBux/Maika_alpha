from __future__ import annotations

from datetime import datetime, timedelta
from .db import upsert_srs_review, get_due_srs_items, add_xp
from .utils import load_json, get_content_path


def verse_of_the_day(age_range: str | None = None) -> dict:
    bank = load_json(get_content_path("bible_content.json"), {"verses": []})
    verses = bank.get("verses", [])
    if not verses:
        return {"reference": "Juan 3:16", "text": "Porque de tal manera amó Dios al mundo..."}
    # Para simplicidad, rotar por día
    idx = int(datetime.utcnow().strftime("%j")) % len(verses)
    verse = verses[idx]
    return {
        "reference": f"{verse.get('book')} {verse.get('chapter')}:{verse.get('verse')}",
        "text": verse.get("text"),
        "item_id": f"{verse.get('book')}::{verse.get('chapter')}::{verse.get('verse')}",
    }


def srs_schedule(ease: float, interval_days: int, result: str) -> tuple[float, int]:
    # Algoritmo SM-2 simplificado
    if result == "again":
        return max(1.3, ease - 0.2), 0
    if interval_days == 0:
        next_interval = 1
    elif interval_days == 1:
        next_interval = 3
    else:
        next_interval = int(round(interval_days * ease))
    new_ease = max(1.3, ease + (0.1 if result == "easy" else (0.0 if result == "good" else -0.2)))
    return new_ease, next_interval


def review_result(user_id: str, item_id: str, ease: float, interval_days: int, result: str) -> dict:
    new_ease, next_interval = srs_schedule(ease, interval_days, result)
    due_at = datetime.utcnow() + timedelta(days=max(1, next_interval))
    upsert_srs_review(
        user_id=user_id,
        item_id=item_id,
        due_at_iso=due_at.isoformat(),
        ease=new_ease,
        interval_days=next_interval,
        last_result=result,
    )
    # XP por repaso
    add_xp(user_id, "srs_review", 5, None)
    return {"ease": new_ease, "interval_days": next_interval, "due_at": due_at.isoformat()}


def due_reviews(user_id: str) -> list[dict]:
    now_iso = datetime.utcnow().isoformat()
    rows = get_due_srs_items(user_id, now_iso)
    return [dict(r) for r in rows]


