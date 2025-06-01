from django.core.management.base import BaseCommand
from movies.models import Movie, Cast
import json
import os

class Command(BaseCommand):
    help = 'Load movie and cast data from JSON files'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Movie.objects.all().delete()
        Cast.objects.all().delete()

        # Load movies
        with open(os.path.join("database", "movies.json")) as f:
            movies = json.load(f)
            for m in movies:
                Movie.objects.create(
                    id=m["id"],
                    movie_name=m["movie_name"],
                    release_year=m["release_year"],
                    director=m["director"],
                    summary=m["summary"],
                    rating = 0.0 if m["rating"] == "N/A" else float(m["rating"])

                )

        # Load casts
        with open(os.path.join("database", "casts.json")) as f:
            casts = json.load(f)
            for c in casts:
                Cast.objects.create(
                    id=c["id"],
                    movie_id=c["movie_id"],
                    actor_name=c["actor_name"],
                    character_name=c["character_name"]
                )

        self.stdout.write(self.style.SUCCESS("Data loaded successfully after truncation."))
