from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .engine import srs as srs_engine
from .engine.db import migrate


class ActionMostrarVerso(Action):
    def name(self) -> Text:
        return "action_mostrar_verso"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        migrate()
        age_range = tracker.get_slot("edad_rango")
        verse = srs_engine.verse_of_the_day(age_range)
        dispatcher.utter_message(text=f"Verso del día:\n\n{verse['reference']}\n{verse['text']}")
        # guardar item_id en slot para repaso
        return [SlotSet("ultimo_versiculo", verse.get("item_id"))]


class ActionRepasoVerso(Action):
    def name(self) -> Text:
        return "action_repaso_verso"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        migrate()
        user_id = tracker.sender_id
        item_id = tracker.get_slot("ultimo_versiculo") or "Juan::3::16"
        ease = float(tracker.get_slot("srs_ease") or 2.5)
        interval_days = int(tracker.get_slot("srs_interval") or 0)
        text = tracker.latest_message.get("text", "").lower()
        if any(k in text for k in ["fácil", "facil", "easy"]):
            result = "easy"
        elif any(k in text for k in ["bien", "good"]):
            result = "good"
        else:
            result = "again"
        out = srs_engine.review_result(user_id, item_id, ease, interval_days, result)
        dispatcher.utter_message(text=f"¡Anotado! Próximo repaso en {out['interval_days']} días.")
        return [SlotSet("srs_ease", out["ease"]), SlotSet("srs_interval", out["interval_days"]) ]


