from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .engine import trivia as trivia_engine
from .engine.db import migrate


class ActionIniciarTrivia(Action):
    def name(self) -> Text:
        return "action_iniciar_trivia"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        migrate()
        user_id = tracker.sender_id
        session = trivia_engine.start_trivia(user_id, 5)
        if not session.get("questions"):
            dispatcher.utter_message(text="No hay preguntas disponibles ahora.")
            return []
        q = session["questions"][0]
        options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(q.get("options", []))])
        dispatcher.utter_message(text=f"Trivia bíblica (1/5)\n\n{q.get('question')}\n\n{options}")
        return [SlotSet("quiz_session_id", "local"), SlotSet("quiz_data", session)]


class ActionResponderTrivia(Action):
    def name(self) -> Text:
        return "action_responder_trivia"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        migrate()
        user_id = tracker.sender_id
        session = tracker.get_slot("quiz_data") or {}
        text = tracker.latest_message.get("text", "").strip()
        try:
            ans = int(text) - 1
        except Exception:
            dispatcher.utter_message(text="Responde con 1, 2, 3 o 4.")
            return []
        session, verdict = trivia_engine.answer_trivia(user_id, session, ans)
        idx = session.get("current", 0)
        total = len(session.get("questions", []))
        if idx >= total:
            dispatcher.utter_message(text=f"¡Terminaste! Puntaje: {session.get('score',0)}/{total}")
            return [SlotSet("quiz_data", None)]
        q = session["questions"][idx]
        options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(q.get("options", []))])
        prefix = "¡Correcto!" if verdict == "correct" else "Incorrecto."
        dispatcher.utter_message(text=f"{prefix} Siguiente ({idx+1}/{total}):\n\n{q.get('question')}\n\n{options}")
        return [SlotSet("quiz_data", session)]


