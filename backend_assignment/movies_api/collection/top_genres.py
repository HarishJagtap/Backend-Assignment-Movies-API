from movies_api.models import Collection, Movie


def calc_top_genres(user):
    """
    Returns list of genres sorted descending by frequency of occurence 
    in all the movies of user's collections
    """
    # Movie INNERJOIN collection_movies INNERJOIN Collection 
    query_set = Movie.objects.all().filter(collection__owner=user)
    # query_set contains all the movies from all the user's collection

    # Keep track of how many times each genre is repeated in all the movies.
    genre_count = dict()

    for movie in query_set:
        if movie.genres:
            # movie.genres is comma seperated string of genres
            for genre in movie.genres.split(','):
                if genre not in genre_count:
                    genre_count[genre] = 1
                else:
                    genre_count[genre] += 1 

    # Ex: genre_count.items() is [('action', 3), ('drama', 5) ,... ]
    # sorted() in this case sort's genre_count.items() based on second 
    # value of tuple which is genre's count
    top_genres = sorted(
        genre_count.items(), key=lambda item: item[1], reverse=True)

    return [genre for genre, count in top_genres]
