from django.db.models import Model, CharField, ForeignKey, IntegerField, CASCADE, ManyToManyField, \
    PositiveSmallIntegerField, ImageField, FileField, DateField
from tunefy_cms.file_manager import create_thumb, path_and_rename, wrapper
from django.contrib.auth.models import User
import datetime


class Genre(Model):
    name = CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ImageThumbModel(Model):
    image = ImageField(blank=True)
    thumb = ImageField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
       create_thumb(self)
       super(ImageThumbModel, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(ImageThumbModel, self).__init__(*args, **kwargs)


class Artist(ImageThumbModel):
    name = CharField(max_length=50)
    description = CharField(max_length=1024, blank=True)
    image = ImageField(upload_to=path_and_rename('artists'), blank=True)
    thumb = ImageField(upload_to=path_and_rename('artists/thumbs'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Song(Model):
    title = CharField(max_length=64)
    artists = ManyToManyField(Artist, blank=True, related_name='artists+')
    audio = FileField(upload_to=path_and_rename('songs'), blank=True)
    #audio = FileField(blank=True)

    def __str__(self):
        all_artists = self.artists.all()
        return '%s - %s' % (', '.join([str(a) for a in all_artists]), self.title)


class Track(Model):
    order = PositiveSmallIntegerField()
    song = ForeignKey('Song', on_delete=CASCADE)
    album = ForeignKey('Album', on_delete=CASCADE)
    popularity = IntegerField(default=0)

    def __str__(self):
        return '{} {}. {}'.format(self.song_id, self.order, self.song)

    class Meta:
        ordering = ('popularity', 'album', 'order', 'song')


class Album(ImageThumbModel):
    name = CharField(max_length=64)
    artist = ForeignKey(Artist, on_delete=CASCADE)
    date_released = DateField('Date', default=datetime.date.today)
    genres = ManyToManyField('Genre', blank=True, related_name='genres+')
    image = ImageField(upload_to=path_and_rename('albums'), blank=True)
    thumb = ImageField(upload_to=path_and_rename('albums/thumbs'), null=True, blank=True)

    def __str__(self):
        return '[{}]{} - {}'.format(self.date_released.year, self.artist, self.name)

    class Meta:
        ordering = ('date_released',)


class PlaylistElement(Model):
    order = PositiveSmallIntegerField()
    track = ForeignKey('Track', on_delete=CASCADE)
    playlist = ForeignKey('Playlist', on_delete=CASCADE)


class Playlist(Model):
    name = CharField(max_length=64)
    owner = ForeignKey(User, on_delete=CASCADE, null=True)
#