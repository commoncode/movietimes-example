from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField(blank=True, null=True)
    overview = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)

    actors = models.ManyToManyField('Actor', related_name='movies')

    def __str__(self):
        return self.title


class Actor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
