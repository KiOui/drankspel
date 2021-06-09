from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import random

from drankspel.api.serializers import DialogflowResponseSerializer

from games.models import DrinkingGame


class DialogflowView(APIView):
    """Dialogflow View."""

    def _get_intent(self):
        """Get the intent from a request."""
        return self.request.data["queryResult"]["intent"]

    def post(self, request, **kwargs):
        """Handle a Dialogflow request."""
        try:
            intent = self._get_intent()
            if intent["displayName"] == "Random drinking game":
                items = DrinkingGame.objects.all()
                random_item = random.choice(items)
                serializer = DialogflowResponseSerializer(
                    {"fullfillmentText": "Hier is je drankspel: {}".format(random_item.name)}, many=False
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
