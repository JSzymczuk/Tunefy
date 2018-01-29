from django.db import models
from mongoengine import Document, StringField, IntField


class Artist(models.Model):
    name = models.CharField(max_length=48)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Album(models.Model):
    name = models.CharField(max_length=64)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    year = models.IntegerField()
    # cover = models.FilePathField()
    # cover_thumb = models.FilePathField()
    genres = models.ManyToManyField('Genre')

    def __str__(self):
        return '[{}]{} - {}'.format(self.year, self.artist, self.name)

    class Meta:
        ordering = ('year',)


class Track(models.Model):
    order = models.PositiveSmallIntegerField()
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)

    def __str__(self):
        return '{}. {}'.format(self.order, self.song)

    class Meta:
        ordering = ('order',)


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=32)
    albums = models.ManyToManyField('Album', blank=True)

    def __str__(self):
        return self.name


class Test(Document):
    meta = {'collection': 'testdoc'}
    name = StringField(max_length=50)
    number = IntField()
