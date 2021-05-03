from rest_framework import serializers

from .models import Movie, Collection


class UserSerializer(serializers.Serializer):
    """Endpoint: 'register/' : deserialize POST data"""
    username = serializers.CharField()
    password = serializers.CharField()


class MovieSerializer(serializers.ModelSerializer):
    """Used in CollectionSerializer as nested serializer"""
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']

        # Will produce 400 bad request if collection is created or updated 
        # with existing movies in db (movie with uuid already exists).
        extra_kwargs = {
            'uuid': {'validators': []},
        }


class CollectionListSerializer(serializers.ModelSerializer):
    """Endpoint: 'collection/': serialize collection objects for GET data"""
    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']


class CollectionSerializer(serializers.ModelSerializer):
    """
    Endpoint: 'collection/'                   : deserialize POST data
    Endpoint: 'collection/<collection_uuid>/' : serialize collection 
                                                    object for GET data
    Endpoint: 'collection/<collection_uuid>/' : deserialize PUT data
    """
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']

    def add_movies_to_collection(self, movies, collection):
        for movie in movies:
            try:
                movie_instance = Movie.objects.get(uuid=movie['uuid'])
            except Movie.DoesNotExist:
                movie_instance = Movie.objects.create(**movie)
            finally:
                collection.movies.add(movie_instance)

    def create(self, validated_data):
        """Endpoint: POST 'collection/': create new collection"""
        movies = validated_data.pop('movies')
        collection = Collection(**validated_data)
        collection.owner = self.context['user']
        collection.save()

        self.add_movies_to_collection(movies, collection)

        return collection

    def update(self, instance, validated_data):
        """
        Endpoint: PUT 'collection/<collection_uuid>/' : update specific 
            collection
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        
        if 'movies' in validated_data:
            instance.movies.clear()
            movies = validated_data.get('movies')
            self.add_movies_to_collection(movies, instance)
    
        return instance


class ThirdPartyApiSerializer(serializers.Serializer):
    """Used to deserialize Third Party API data"""
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = MovieSerializer(many=True)
