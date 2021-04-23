from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import renderers
# from rest_framework.permissions import IsAuthenticated
from .premissions import MyCustomIsAuthenticated
from .service import run


# Create your views here.


class ManagerView(APIView):
    permission_classes = [MyCustomIsAuthenticated]
    renderer_classes = (
        renderers.JSONRenderer,
    )

    def post(self, request, format=None):
        data = request.data
        command = data.get('command', '')
        if command:
            return Response(run(command, data))
        else:
            return Response({'detail': 'No command was provided!'})

