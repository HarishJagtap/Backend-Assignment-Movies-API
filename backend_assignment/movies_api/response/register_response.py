from rest_framework.response import Response
from rest_framework import status


def incorrect_password_response():
    return Response(
        {
            'message': "Incorrect password provided"
        }, 
        status=status.HTTP_403_FORBIDDEN)


def access_token_response(access_token):
    return Response(
        {
            'access_token': str(access_token)
        }, 
        status=status.HTTP_201_CREATED)
        