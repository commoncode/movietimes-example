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
