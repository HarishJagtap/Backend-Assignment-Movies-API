from django.urls import path

from .views import UserRegister, MovieList, CollectionList, CollectionDetail

urlpatterns = [
    path('register/', UserRegister.as_view(), name='user_register'),
    path('movies/', MovieList.as_view(), name='movies_list'),
    path('collection/', CollectionList.as_view(), name='collection_list'),
    path(
        'collection/<uuid:uuid>/', CollectionDetail.as_view(), 
        name='collection_detail'),
]
