import random
import json
from typing import Dict, Tuple
from .utils import load_json, get_content_path
from .db import add_xp


def load_trivia_bank() -> Dict:
    return load_json(get_content_path("trivia_bank.json"), {"questions": []})


def start_trivia(user_id: str, num_questions: int = 5, difficulty: str = None) -> Dict:
    """
    Inicia una trivia con preguntas filtradas por dificultad

    Args:
        user_id: ID del usuario
        num_questions: Número de preguntas
        difficulty: Nivel de dificultad ('facil', 'medio', 'dificil', None para todas)

    Returns:
        Dict con las preguntas seleccionadas
    """
    import time
    bank = load_trivia_bank()
    questions = list(bank.get("questions", []))

    if not questions:
        return {"questions": []}

    # Filtrar por dificultad si se especifica
    if difficulty:
        difficulty = difficulty.lower()
        filtered_questions = [q for q in questions if q.get("difficulty", "").lower() == difficulty]

        # Si no hay suficientes preguntas del nivel, usar todas
        if len(filtered_questions) >= num_questions:
            questions = filtered_questions

    # Mejorar aleatoriedad con semilla basada en tiempo y user_id
    seed_value = int(time.time() * 1000) + hash(user_id) % 10000
    random.seed(seed_value)

    # Usar random.sample para mejor distribución
    if len(questions) >= num_questions:
        selected = random.sample(questions, num_questions)
    else:
        # Si no hay suficientes, repetir preguntas pero mezclar
        selected = random.sample(questions * ((num_questions // len(questions)) + 1), num_questions)

    return {"questions": selected, "current": 0, "score": 0, "difficulty": difficulty}


def answer_trivia(user_id: str, session: Dict, answer_index: int) -> Tuple[Dict, str]:
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


