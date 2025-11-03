from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlite_metrics import MetricsManager


def create_manager(tmp_path: Path) -> MetricsManager:
    """Helper to create an isolated MetricsManager for testing."""
    db_path = tmp_path / "metrics.db"
    return MetricsManager(str(db_path))


def test_quiz_result_persists_and_updates_leaderboard(tmp_path):
    manager = create_manager(tmp_path)

    payload = {"questions": ["Q1", "Q2", "Q3"], "answers": ["1", "2", "3"]}
    assert manager.save_quiz_result("user-123", 2, 3, payload)

    history = manager.get_user_quiz_history("user-123")
    assert len(history) == 1
    first = history[0]
    assert first["score"] == 2
    assert first["total_questions"] == 3
    assert first["percentage"] == pytest.approx(66.666, rel=1e-3)

    leaderboard = manager.get_leaderboard()
    assert any(entry["user_id"] == "user-123" for entry in leaderboard)


def test_user_queries_and_usage_stats(tmp_path):
    manager = create_manager(tmp_path)

    assert manager.save_user_query("user-abc", "preguntar_versiculo", "[{\"entity\": \"libro\"}]", True)
    assert manager.save_usage_stat("user-abc", "verse_search", success=True)

    stats = manager.get_usage_stats(days=7)
    assert stats["total_queries"] == 1
    assert stats["total_quizzes"] == 0
    assert stats["queries_by_intent"].get("preguntar_versiculo") == 1
