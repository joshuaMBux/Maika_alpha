#!/usr/bin/env python3
"""
Script para probar la aleatoriedad del RNG en quiz y trivia
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from actions.engine.trivia import start_trivia
from actions.actions import QUIZ_DATA, BibleIndexer

# Cargar datos
BibleIndexer.load_bible_data()

def test_trivia_rng():
    print("=== PRUEBA DE RNG PARA TRIVIA ===")

    # Probar con diferentes dificultades
    difficulties = ["facil", "medio", "dificil", None]

    for diff in difficulties:
        print(f"\n--- Dificultad: {diff} ---")
        results = []

        # Ejecutar 5 veces para ver variabilidad
        for i in range(5):
            session = start_trivia(f"user_{i}", 3, diff)
            questions = session.get("questions", [])
            if questions:
                first_question = questions[0].get("question", "")[:50]
                results.append(first_question)

        print(f"Primeras preguntas en 5 ejecuciones:")
        for i, q in enumerate(results, 1):
            print(f"  {i}. {q}...")

        # Verificar si son diferentes
        unique_results = set(results)
        print(f"Preguntas únicas: {len(unique_results)}/5")
        if len(unique_results) < 5:
            print("⚠️  POSIBLE PROBLEMA: Preguntas repetidas")
        else:
            print("✅ Buen RNG: Todas las preguntas diferentes")

def test_quiz_rng():
    print("\n=== PRUEBA DE RNG PARA QUIZ ===")

    import random
    import time

    # Simular el código del quiz
    all_questions = QUIZ_DATA["questions"]
    difficulties = ["facil", "medio", "dificil", None]

    for diff in difficulties:
        print(f"\n--- Dificultad: {diff} ---")

        # Filtrar como en el código
        questions_pool = all_questions
        if diff:
            filtered = [q for q in all_questions if q.get("difficulty", "").lower() == diff.lower()]
            if len(filtered) >= 3:
                questions_pool = filtered

        print(f"Preguntas disponibles: {len(questions_pool)}")

        results = []

        # Ejecutar 5 veces
        for i in range(5):
            # Simular semilla como en el código
            seed_value = int(time.time() * 1000) + hash(f"user_{i}") % 10000
            random.seed(seed_value)

            selected = random.sample(questions_pool, min(3, len(questions_pool)))
            if selected:
                first_question = selected[0].get("question", "")[:50]
                results.append(first_question)

        print(f"Primeras preguntas en 5 ejecuciones:")
        for i, q in enumerate(results, 1):
            print(f"  {i}. {q}...")

        unique_results = set(results)
        print(f"Preguntas únicas: {len(unique_results)}/5")
        if len(unique_results) < 5:
            print("⚠️  POSIBLE PROBLEMA: Preguntas repetidas")
        else:
            print("✅ Buen RNG: Todas las preguntas diferentes")

def check_difficulty_distribution():
    print("\n=== VERIFICACIÓN DE DISTRIBUCIÓN POR DIFICULTAD ===")

    all_questions = QUIZ_DATA["questions"]
    difficulties = ["facil", "medio", "dificil"]

    for diff in difficulties:
        count = len([q for q in all_questions if q.get("difficulty", "").lower() == diff])
        print(f"{diff.capitalize()}: {count} preguntas")

    print(f"Total: {len(all_questions)} preguntas")

if __name__ == "__main__":
    test_trivia_rng()
    test_quiz_rng()
    check_difficulty_distribution()