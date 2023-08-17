from typing import Callable


class Intent:
    """Intent class."""

    def __init__(self, name: str, handler: Callable, training_phrases: [str], webhook_state=False):
        """Initialize an Intent."""
        self.name = name
        self.handler = handler
        self.training_phrases = training_phrases
        self.webhook_state = webhook_state

    def to_dict(self):
        """Convert this to dictionary that Google Dialogflow can process."""
        return {
            "display_name": self.name,
            "webhook_state": True,
            "training_phrases": [{"parts": [{"text": x} for x in self.training_phrases]}],
        }


def intent(name: str, handler: Callable, training_phrases: [str], **kwargs):
    """Generate an Intent."""
    return Intent(name, handler, training_phrases, **kwargs)


class IntentManager:
    """Intent Manager class."""

    def __init__(self):
        """Initialize Intent Manager."""
        self.intents = dict()

    @staticmethod
    def create_from_list(intents: list):
        """Create IntentManager from list of Intents."""
        intent_manager = IntentManager()
        intent_manager.add_all(intents)
        return intent_manager

    def match(self, intent_name):
        """Check if an Intent already exists."""
        if intent_name in self.intents.keys():
            return self.intents[intent_name]
        return None

    def add_all(self, intents: list):
        """Recursively add all Intents in a list of Intents (lists in the lists will be recursively added)."""
        for intent in intents:
            if isinstance(intent, Intent):
                self.add_intent(intent.name, intent)
            elif isinstance(intent, list):
                self.add_all(intent)
            else:
                raise RuntimeError("Error while adding intents to intent list. Got type {}.".format(type(intent)))

    def add_intent(self, name: str, intent: Intent):
        """Add an Intent to the IntentManager."""
        self.intents[name] = intent
