from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Collection
from .serializers import (
    UserSerializer, CollectionListSerializer, CollectionSerializer)
from .register.token_manager import TokenManager
from .movies.third_party_api import ThirdPartyApiWrapper
from .collection.top_genres import calc_top_genres
from .collection.decorators import fetch_collection_object
from .response import register_response, collection_response


class UserRegister(APIView):
    """
    Endpoint: register/
    POST: Accept username and password, then return JWT Acess Token.

    Refresh token is not used here, so user must register again after 
    access token expires (Ex: 5 minutes) to get a new access token
    User's collection will remain in DB even after the access token 
    expires, so user can access the collections previously created 
    by registering again.
    
    Since requests to all endpoints except this endpoint needs to be 
    authenticated with JWT token, the default permission class is set 
    to 'IsAuthenticated' to ensure requests to all endpoints are 
    authenticated. To allow unauthenticated requests to this endpoint, 
    permission class is set empty.
    """
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # TokenManager takes care of creating new users and 
            # verifying password of old users, and returns access token 
            # only if user is verified.
            # Throws exception if unverified user tries to obtain access token

            tm = TokenManager(
                serializer.validated_data['username'], 
                serializer.validated_data['password'])
            try:
                access_token = tm.get_access_token()
            except:
                return register_response.incorrect_password_response()
                    
            return register_response.access_token_response(access_token)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieList(APIView):
    """
    Endpoint: movies/
    GET: Return list of movies from Third Party API
    """
    def get(self, request):
        try:
            # ThirdPartyApiWrapper takes
            # home_url (Ex: 127.0.0.1:8000/movies/?page=2)
            # and returns data which is serialized from Third Party API's 
            # Json response. The links in the Json response which point 
            # to the Third Party API have been changed to point to this API 
            # in the serialized data.

            # Ex: Next link in JSON response is 
            #       www.thirdpartyapi.com/movies/?page=3
            #     Next link in serialized data is 
            #       127.0.0.1:8000/movies/?page=3

            tpa_wrapper = ThirdPartyApiWrapper(request.build_absolute_uri())
            serialized_data = tpa_wrapper.get_serialized_data()
        except:
            # ThirdPartyApiWrapper throws exception when Third Party API fails
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serialized_data, status=status.HTTP_200_OK)


class CollectionList(APIView):
    """
    Endpoint: collection/
    GET: Return list of all collections
    POST: Create new collection
    """
    def get(self, request):
        collections = Collection.objects.filter(owner=request.user)
        serializer = CollectionListSerializer(collections, many=True)
        return collection_response.list_collections_response(
                collections=serializer.data,
                favourite_genres=','.join(calc_top_genres(request.user)[:3])
        )

    def post(self, request):
        serializer = CollectionSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            collection = serializer.save()
            return collection_response.create_collection_response(collection.uuid)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDetail(APIView):
    """
    Endpoint: collection/<collection_uuid>/
    GET: Return details of a specific collection
    PUT: Update details of a specific collection
    DELETE: Delete a specific collection
    """
    @fetch_collection_object
    def get(self, request, collection):
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    @fetch_collection_object
    def put(self, request, collection):
        serializer = CollectionSerializer(
            data=request.data, instance=collection, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @fetch_collection_object
    def delete(self, request, collection):
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
