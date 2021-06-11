from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import random

from drankspel.api.serializers import DialogflowResponseSerializer, DialogflowRequestSerializer

from games.models import DrinkingGame

from drankspel.dialogflow.services import intent_manager


class DialogflowView(APIView):
    """Dialogflow View."""

    def _get_intent(self):
        """Get the intent from a request."""
        return self.request.data["queryResult"]["intent"]

    def post(self, request, **kwargs):
        """Handle a Dialogflow request."""
        dialogflow_request = DialogflowRequestSerializer(data=request.data, many=False)
        try:
            matched_intent = intent_manager.match(
                dialogflow_request.to_internal_value(request.data).get("queryResult").get("intent").get("displayName")
            )
            if matched_intent is not None:
                return Response(matched_intent.handler(dialogflow_request, request), status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
