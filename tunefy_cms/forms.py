from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelChoiceField, Textarea
from tunefy_cms.models import Artist, Song, Genre, Album, Playlist
from tunefy_cms.validators import is_empty, is_max_length_exceeded, ValidationMessages


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name': 'Nazwa'
        }

    def clean(self):
        cleaned_data = super(GenreForm, self).clean()

        if is_empty(cleaned_data.get('name')):
            self.add_error('name', ValidationMessages.FIELD_IS_REQUIRED)
        else:
            max_lth = self.fields.get('name').max_length
            if is_max_length_exceeded(cleaned_data.get('name'), max_lth):
                self.add_error('name', ValidationMessages.MAX_LENGTH_EXCEEDED % (self.fields.get('name').name, max_lth))

        if not self.errors.items:
            raise ValidationError()

        return cleaned_data


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