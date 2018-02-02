from django.db.models import Model, CharField, ForeignKey, IntegerField, CASCADE, ManyToManyField, PositiveSmallIntegerField, ImageField, FileField

from tunefy_cms.file_manager import create_thumb, path_and_rename, wrapper


class Genre(Model):
    name = CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


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


class Song(Model):
    title = CharField(max_length=64)
    artist = ForeignKey(Artist, on_delete=CASCADE, related_name='artist+')
    all_artists = ManyToManyField(Artist, blank=True, related_name='artists+')
    audio = FileField(upload_to=path_and_rename('songs'), blank=True)
    #audio = FileField(blank=True)

    def __str__(self):
        artists = self.all_artists.exclude(id = self.artist_id).all()
        return '%s - %s (feat. %s)' % (self.artist, self.title, ', '.join([str(a) for a in artists]))


class Track(Model):
    order = PositiveSmallIntegerField()
    song = ForeignKey('Song', on_delete=CASCADE)
    album = ForeignKey('Album', on_delete=CASCADE)

    def __str__(self):
        return '{}. {}'.format(self.order, self.song)

    class Meta:
        ordering = ('order',)


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






