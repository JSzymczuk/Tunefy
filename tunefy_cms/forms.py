from django.forms import ModelForm, Textarea
from tunefy_cms.models import Artist, Song, Genre, Album, Playlist
from tunefy_cms.validators import validate_text_field, validate_file, validate_selection_box


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name': 'Nazwa'
        }

    def clean_name(self):
        return validate_text_field(self, 'name', True, 30)


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
        fields = ['name', 'image', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    def clean_name(self):
        return validate_text_field(self, 'name', True, 50)

    def clean_image(self):
        return validate_file(self, 'image', False, ['.jpg', '.jpeg', '.png'])


class CreateSongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artists', 'audio']

    def __init__(self, *args, **kwargs):
        super(CreateSongForm, self).__init__(*args, **kwargs)
        # self.fields['artist'].empty_label = 'None'

    def clean_title(self):
        return validate_text_field(self, 'title', True, 64)

    def clean_audio(self):
        return validate_file(self, 'audio', False, ['.mp3', '.wav'])

    def clean_artists(self):
        return validate_selection_box(self, 'artists')


class CreateAlbumForm(ThumbModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'name', 'date_released', 'genres', 'image']

    initial_tracks = []

    def __init__(self, initial_tracks, *args, **kwargs):
        super(CreateAlbumForm, self).__init__(*args, **kwargs)
        self.initial_tracks = initial_tracks

    def clean_name(self):
        return validate_text_field(self, 'name', True, 64)

    def clean_image(self):
        return validate_file(self, 'image', False, ['.jpg', '.jpeg', '.png'])
