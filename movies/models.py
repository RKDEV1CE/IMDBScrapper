from django.db import models

class Movie(models.Model):
    id = models.CharField(primary_key=True, max_length=20)  # IMDB ID like 'tt6495770'
    movie_name = models.CharField(max_length=255)
    release_year = models.CharField(max_length=4)
    director = models.CharField(max_length=255)
    summary = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.movie_name

class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='casts')
    actor_name = models.CharField(max_length=255)
    character_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.actor_name} in {self.movie.movie_name}"
