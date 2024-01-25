class Album:
    # Initialize a new Album document class
    def __init__(self, uid, position, release_name, artist_name, release_type,
                 primary_genres, secondary_genres, descriptors, avg_rating,
                 rating_count, review_count):
            self.uid = uid
            self.position = position
            self.release_name = release_name
            self.artist_name = artist_name
            self.release_type = release_type
            self.primary_genres = primary_genres
            self.secondary_genres = secondary_genres
            self.descriptors = descriptors
            self.avg_rating = avg_rating
            self.rating_count = rating_count
            self.review_count = review_count

    def __repr__(self):
        return (f"Artist: {self.artist_name} \
                Album name: {self.release_name} \
                Primary genres: {self.primary_genres} \
                Secondary genres: {self.secondary_genres} \
                {self.avg_rating} across {self.rating_count} ratings")
