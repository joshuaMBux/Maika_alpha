import random
from .utils import load_json, get_content_path
from .db import add_xp


def generate_bingo_board(size: int = 3) -> list[list[str]]:
    bank = load_json(get_content_path("bible_content.json"), {"values": [
        "Amor", "Gozo", "Paz", "Paciencia", "Bondad", "Fe", "Mansedumbre", "Templanza", "Gratitud"
    ]})
    values = list(bank.get("values", []))
    random.shuffle(values)
    needed = size * size
    picked = (values[:needed] if len(values) >= needed else (values * ((needed // len(values)) + 1))[:needed])
    return [picked[i*size:(i+1)*size] for i in range(size)]


def reward_bingo(user_id: str, completed: bool) -> None:
    if completed:
        add_xp(user_id, "bingo_complete", 30, None)


