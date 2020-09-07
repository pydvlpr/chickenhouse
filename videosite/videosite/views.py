
from django.shortcuts import get_object_or_404,render, redirect
from django.urls import reverse_lazy, reverse
from django import forms
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView

# Modells
from .models.cam import Cam


# Index site
def index(request):
    """
        call index site
    """

    return render(request, 'videosite/index.html')

# Cam views
def cam_list(request):
    """
        call list of cameras
    """
    cam_list = Cam.objects.order_by('id')
    context = {'cam_list':'cam_list'}
    return render(request, 'videosite/camera-list.html',context)


class CreateCam(CreateView):
    """
        Create camera object by form
    """

    template_name = 'cam_create_form.html'
    model = Cam

    fields = ['name','position','url']

    success_url = reverse_lazy('cam_list')

    class Meta:
        pass

    def generate_urls(self,host):
        """
            generate urls to preview and videostream and store them in specific url fields
        """
        pass

    def get_form(self, form_class=None):
        """
            generate form to create camera object
        """

        form = super(CreateCam, self).get_form(form_class)
        form.fields['host'].required = True
        form.fields['name'].required = True
        

        # Form-Felder modifizieren
        form.fields['host'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Host-Adresse der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['name'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Name der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})


        form.fields['position'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Position der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['preview_url'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"URL der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})
        
        form.fields['stream_url'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"URL der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        
        return form

class ModifyCam(UpdateView):
    """
        Modify camera settings by form
    """

    template_name = 'cam_modify_form.html'
    model = Cam

    fields = ['name','position','url']

    success_url = reverse_lazy('cam_list')

    class Meta:
        pass

    def get_form(self, form_class=None):
        """
            generate form to modify camera settings
        """
        
        form = super(CreateCam, self).get_form(form_class)
        form.fields['host'].required = True
        form.fields['name'].required = True
        

        # Form-Felder modifizieren

        form.fields['host'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Host-Adresse der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['name'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Name der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})


        form.fields['position'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Position der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['preview_url'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"URL der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})
        
        form.fields['stream_url'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"URL der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        return form

class CamDetails(DetailView):
    """
        Show details of camera
    """

    model = Cam
    template_name_suffix = '_details_form'

    class Meta:
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
class DeleteCam(DeleteView):
    """
        Delete camera from application
    """

    model = Cam
    success_url = reverse_lazy('cam_list')


def CamPreview(request):
    """
        Call url from raspi, get and show preview image
    """
    
    pass

def CamStream(request):
    """
        Call url form rapsi, get and show video stream
    """
    
    pass