from drankspel.dialogflow.models import intent
from .handlers import drinking_game_handler
from django.conf import settings

intents = [intent("Random drinking game", drinking_game_handler, [settings.GOOGLE_INTENT_TRAINING_PHRASE])]
