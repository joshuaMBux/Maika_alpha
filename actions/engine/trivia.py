import random
import json
from .utils import load_json, get_content_path
from .db import add_xp


def load_trivia_bank() -> dict:
    return load_json(get_content_path("trivia_bank.json"), {"questions": []})


def start_trivia(user_id: str, num_questions: int = 5) -> dict:
    bank = load_trivia_bank()
    questions = list(bank.get("questions", []))
    if not questions:
        return {"questions": []}
    random.shuffle(questions)
    selected = questions[:num_questions]
    return {"questions": selected, "current": 0, "score": 0}


def answer_trivia(user_id: str, session: dict, answer_index: int) -> tuple[dict, str]:
    idx = session.get("current", 0)
    questions = session.get("questions", [])
    if idx >= len(questions):
        return session, "done"
    q = questions[idx]
    correct = int(q.get("correct", 0))
    is_correct = (answer_index == correct)
    if is_correct:
        session["score"] = int(session.get("score", 0)) + 1
        add_xp(user_id, "trivia_correct", 10, json.dumps({"q": q.get("question")}))
        verdict = "correct"
    else:
        verdict = "incorrect"
    session["current"] = idx + 1
    return session, verdict


