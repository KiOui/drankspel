from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class DialogflowView(APIView):

    def get(self, request, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        print(request.data)
        return Response(status=status.HTTP_200_OK)
