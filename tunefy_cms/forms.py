from django.forms import ModelForm, ModelChoiceField
from tunefy_cms.models import Artist, Song, Genre, Album


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class ThumbModelForm(ModelForm):
    initial_thumb = None

    def __init__(self, *args, **kwargs):
        super(ThumbModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance')
        if instance:
            setattr(self, 'initial_thumb', getattr(instance, 'thumb'))


class CreateArtistForm(ThumbModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'image']


class CreateSongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artists', 'audio']

    def __init__(self, *args, **kwargs):
         super(CreateSongForm, self).__init__(*args, **kwargs)
         #self.fields['artist'].empty_label = 'None'


class CreateAlbumForm(ThumbModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'name', 'date_released', 'genres', 'image']

    initial_tracks = []

    def __init__(self, initial_tracks, *args, **kwargs):
        super(CreateAlbumForm, self).__init__(*args, **kwargs)
        self.initial_tracks = initial_tracks

