import factory
from factory.django import DjangoModelFactory

from .models import Actor, Movie


class MovieFactory(DjangoModelFactory):

    class Meta:
        model = Movie

    title = factory.Faker('sentence', nb_words=4)
    release_date = factory.Faker('date_time_this_century', before_now=True)
    overview = factory.Faker('paragraph')
    rating = factory.Faker(
        'pydecimal', left_digits=1, right_digits=1, positive=True
    )

    @factory.post_generation
    def actors(self, create, extracted, **kwargs):
        if create and extracted:
            for actor in extracted:
                self.actors.add(actor)


class ActorFactory(DjangoModelFactory):

    class Meta:
        model = Actor

    name = factory.Faker('name')


"""
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
"""