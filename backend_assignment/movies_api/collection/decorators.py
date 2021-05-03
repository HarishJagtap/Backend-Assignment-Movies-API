"""
Decorator for views of endpoint: 'collection/<collection_uuid>/'
This decorator fetches the collection object with the uuid that is requested
and passes it to the view functions.
In case, the collection object does not exist, it returns HTTP_404_NOT_FOUND.
"""
from rest_framework.response import Response
from rest_framework import status

from movies_api.models import Collection


def fetch_collection_object(func):
    def wrapper(self, request, uuid):
        try:
            collection = Collection.objects.get(pk=uuid, owner=request.user)
        except Collection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return func(self, request, collection)
    
    return wrapper