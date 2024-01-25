import pandas
class Album:
    # Initialize a new Album document class with secondary genres
    def __init__(self, position, release_name, artist_name,
                 primary_genres, secondary_genres, avg_rating,
                 rating_count):
        self.position = position
        self.release_name = release_name
        self.artist_name = artist_name
        self.primary_genres = primary_genres

        # If secondary genres do not exist: do not define (secondary field)
        if pandas.isna(secondary_genres):
            self.secondary_genres = secondary_genres
        self.avg_rating = avg_rating
        self.rating_count = rating_count

    # Return an album description
    def __repr__(self):
        return (f"Artist: {self.artist_name} \
                Album name: {self.release_name} \
                Primary genres: {self.primary_genres} \
                Secondary genres: {self.secondary_genres} \
                {self.avg_rating} across {self.rating_count} ratings")
