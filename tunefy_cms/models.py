
from django.db.models import Model, CharField, ForeignKey, IntegerField, CASCADE, ManyToManyField, PositiveSmallIntegerField, ImageField
from tunefy_cms.file_manager import create_thumb, path_and_rename, wrapper


class Artist(Model):
    name = CharField(max_length=50)
    #image = ImageField(upload_to=wrapper, blank=True)
    #thumb = ImageField(upload_to=wrapper, null=True, blank=True)
    image = ImageField(upload_to=path_and_rename('artists'), blank=True)
    thumb = ImageField(upload_to=path_and_rename('artists/thumbs'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        create_thumb(self)
        super(Artist, self).save(*args, **kwargs)





class Album(Model):
    name = CharField(max_length=64)
    artist = ForeignKey(Artist, on_delete=CASCADE)
    year = IntegerField()
    # cover = models.FilePathField()
    # cover_thumb = models.FilePathField()
    genres = ManyToManyField('Genre')

    def __str__(self):
        return '[{}]{} - {}'.format(self.year, self.artist, self.name)

    class Meta:
        ordering = ('year',)


class Track(Model):
    order = PositiveSmallIntegerField()
    song = ForeignKey('Song', on_delete=CASCADE)
    album = ForeignKey('Album', on_delete=CASCADE)

    def __str__(self):
        return '{}. {}'.format(self.order, self.song)

    class Meta:
        ordering = ('order',)


class Song(Model):
    artist = ForeignKey(Artist, on_delete=CASCADE)
    title = CharField(max_length=64)

    def __str__(self):
        return self.title


class Genre(Model):
    name = CharField(max_length=32)
    albums = ManyToManyField('Album', blank=True)

    def __str__(self):
        return self.name
