from drankspel.dialogflow.models import intent
from .handlers import drinking_game_handler

intents = [intent("Random drinking game", drinking_game_handler, ["Geef mij een random drankspel"])]
