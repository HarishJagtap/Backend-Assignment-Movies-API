from rest_framework.response import Response
from rest_framework import status


def list_collections_response(collections, favourite_genres):
    return Response(
        {
            'is_success': True,
            'data': {
                'collections': collections,
                'favourite_genres': favourite_genres
            }
        },
        status=status.HTTP_200_OK)


def create_collection_response(uuid):
    return Response(
        {
            'collection_uuid': uuid
        }, 
        status=status.HTTP_201_CREATED)
