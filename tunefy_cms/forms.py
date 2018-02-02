from django.forms import ModelForm, ModelChoiceField
from tunefy_cms.models import Artist, Song, Genre


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class CreateArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'image']

    initial_thumb = None

    def __init__(self, *args, **kwargs):
        super(CreateArtistForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance')
        if instance:
            setattr(self, 'initial_thumb', getattr(instance, 'thumb'))


class CreateSongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'all_artists', 'audio']

    def __init__(self, *args, **kwargs):
    #     # user = kwargs.pop('user','')
         super(CreateSongForm, self).__init__(*args, **kwargs)
         self.fields['artist'].empty_label = 'None'
    #     self.fields['user_defined_code'] = ModelChoiceField(queryset = Artist.objects.all())


class CreateAlbumForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'image']

    initial_thumb = None

    def __init__(self, *args, **kwargs):
        super(CreateArtistForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance')
        if instance:
            setattr(self, 'initial_thumb', getattr(instance, 'thumb'))

