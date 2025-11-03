from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .engine import missions as missions_engine
from .engine.db import migrate


class ActionMisionHoy(Action):
    def name(self) -> Text:
        return "action_mision_hoy"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        migrate()
        age_range = tracker.get_slot("edad_rango")
        m = missions_engine.daily_mission(age_range)
        dispatcher.utter_message(text=f"Misión de hoy: {m.get('title')}\n\n{m.get('description')}")
        return [SlotSet("mission_title", m.get("title"))]


class ActionCompletarMision(Action):
    def name(self) -> Text:
        return "action_completar_mision"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        migrate()
        user_id = tracker.sender_id
        title = tracker.get_slot("mission_title") or "Misión"
        missions_engine.complete_mission(user_id, {"title": title})
        dispatcher.utter_message(text="¡Misión completada! Ganaste 20 XP.")
        return []


