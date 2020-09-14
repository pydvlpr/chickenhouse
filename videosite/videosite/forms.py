from django import forms
from django.urls import reverse_lazy

from .models.cam import Cam


class CamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CamForm,self).__init__(*args, **kwargs)
        
        self.fields['host'].required = True
        self.fields['name'].required = True
        self.fields['position'].required = False
        self.fields['img_url'].required = False
        self.fields['img_url'].disabled = True
        self.fields['stream_url'].required = False
        self.fields['stream_url'].disabled =True
        
        
        for field in self.fields:
            help_text = self.fields[field].help_text
            # to be improved
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class':'has-popover', 'data-content':help_text,
                    'data-placement':'right', 'data-container':'body'})
        
    class Meta:
        template_name = "cam_create_form.html"
        model = Cam

        fields = (  'host', 'name', 'position',
                    'img_url', 'stream_url'
                 )
        
        success_url = reverse_lazy('cam_list')
        pass

   