import random

from drankspel.api.serializers import DialogflowResponseSerializer
from games.models import DrinkingGame
from django.conf import settings


def drinking_game_handler(data, request):
    """'get drinking game' Intent handler."""
    items = DrinkingGame.objects.all()
    random_item = random.choice(items)
    serializer = DialogflowResponseSerializer(
        {"fullfillmentText": settings.GOOGLE_INTENT_RESPONSE_PHRASE.format(random_item.name)}, many=False
    )
    return serializer.data
