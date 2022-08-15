from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import PersonSerializer
from .models import Person


class PersonViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        queryset = Person.objects.all()
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)
