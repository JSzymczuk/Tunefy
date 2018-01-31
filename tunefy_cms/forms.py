from django.forms import ModelForm
from tunefy_cms.models import Artist


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
