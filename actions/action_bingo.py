from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .engine import bingo as bingo_engine
from .engine.db import migrate


class ActionBingo(Action):
    def name(self) -> Text:
        return "action_bingo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        migrate()
        board = bingo_engine.generate_bingo_board(3)
        lines = [" | ".join(row) for row in board]
        dispatcher.utter_message(text="Bingo de valores 3x3:\n\n" + "\n".join(lines))
        return [SlotSet("bingo_board", board)]


