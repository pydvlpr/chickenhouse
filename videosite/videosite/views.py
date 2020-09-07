
from django.shortcuts import get_object_or_404,render, redirect
from django.urls import reverse_lazy, reverse
from django import forms
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView

# Modells
from .models.cam import Cam
from .models.preview import Preview
from .models.stream import Stream


# Index site
def index(request):
    return render(request, 'videosite/index.html')

# Cam views
def cam_list(request):
    cam_list = Cam.objects.order_by('id')
    context = {'cam_list':'cam_list'}
    return render(request, 'videosite/camera-list.html',context)

def CamPreview(request):
    pass

class CreateCam(CreateView):
    template_name = 'cam_create_form.html'
    model = Cam

    fields = ['name','position','url']

    success_url = reverse_lazy('cam_list')

    class Meta:
        pass
    def get_form(self, form_class=None):
        form = super(CreateCam, self).get_form(form_class)
        #form.fields['position'].required = False
        

        # Form-Felder modifizieren
        form.fields['name'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Name der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['position'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Position der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['url'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"URL der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})
        
        return form

class ModifyCam(UpdateView):
    template_name = 'cam_modify_form.html'
    model = Cam

    fields = ['name','position','url']

    success_url = reverse_lazy('cam_list')

    class Meta:
        pass
    def get_form(self, form_class=None):
        form = super(CreateCam, self).get_form(form_class)
        #form.fields['position'].required = False
        

        # Form-Felder modifizieren
        form.fields['name'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Name der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['position'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"Position der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})

        form.fields['url'].widget = forms.TextInput(attrs={ 'class':'has-popover',
                                                                        'data-content':"URL der Kamera eingeben.",
                                                                        'data-placement':'right',
                                                                        'data-container':'body'})
        return form

class CamDetails(DetailView):

    model = Cam
    template_name_suffix = '_details_form'

    class Meta:
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
class DeleteCam(DeleteView):
    model = Cam
    success_url = reverse_lazy('cam_list')

