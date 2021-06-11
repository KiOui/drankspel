from .models import IntentManager
from .intents import intents

intent_manager = IntentManager.create_from_list(intents)
