
from django.shortcuts import get_object_or_404,render, redirect
from django.urls import reverse_lazy, reverse
from django import forms
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView

# Modells
from .models.cam import Cam

# Forms
from .forms import CamForm

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
    context = {'cam_list':cam_list}
    return render(request, 'videosite/camera-list.html',context)

# Cam previews
def cam_preview(request):
    """
        prepare cam list for preview site
    """
    cam_list = Cam.objects.order_by('id')
    context = {'cam_list':cam_list}
    return render(request, 'videosite/cam_preview.html',context)


def create_cam(request):
    """
        Create cam with individual form and automized generated host based urls
    """
    args = {}
    if request.method == "POST":
        post = True
        form = CamForm(request.POST)
        if form.is_valid():
            valid = True

            # take form data
            new_cam = form.save(commit=False)
            
            # build urls by hostname
            new_cam.img_url = "{}://{}/preview/".format(new_cam.protocol,new_cam.host)
            new_cam.stream_url = "{}://{}/stream/".format(new_cam.protocol,new_cam.host)

            new_cam.save()
            return redirect('cam_list')
        else:
            error_message = "Error during form processing."
            return render(request, "videosite/cam_creation_error.html",
                {'error_message':error_message})
    else:
        form = CamForm()

    args['form']=form
    return render(request, "videosite/cam_create_form.html", args)

def modify_cam(request,pk):
    """
        Create cam with individual form and automized generated host based urls
    """
    args = {}
    cam = get_object_or_404(Cam,pk=pk)
    if request.method == "POST":
        post = True
        form = CamForm(request.POST, instance=cam)
        if form.is_valid():
            valid = True
            # take form data
            new_cam = form.save(commit=False)
            print("valid: ",new_cam)
            
            # build urls by hostname
            new_cam.img_url = "http://{}/preview/".format(new_cam.host)
            new_cam.stream_url = "http://{}/stream/".format(new_cam.host)

            new_cam.save()
            return redirect('cam_list')
        else:
            error_message = "Error during form processing."
            return render(request, "videosite/cam_creation_error.html",
                {'error_message':error_message})
    else:
        form = CamForm(instance=cam)

    args['form']=form
    return render(request, "videosite/cam_modify_form.html", args)

class ModifyCam(UpdateView):
    """
        Modify camera settings by form
    """  
    model = Cam
    fields = ['host','name','position','img_url','stream_url']

    template_name = 'cam_modify_form.html'
    success_url = reverse_lazy('cam_list')

    class Meta:
        pass

    def get_form(self, form_class=None):
        """
            generate form to modify camera settings
        """
        
        form = super(ModifyCam, self).get_form(form_class)
        form.fields['host'].required = True
        form.fields['name'].required = True
        form.fields['position'].required = False
        form.fields['img_url'].readonly = True
        form.fields['img_url'].required = False
        form.fields['stream_url'].required = False
        

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

        form.fields['img_url'].widget = forms.TextInput(attrs={ 'class':'has-popover',
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

def CamStream(request,pk):
    """
        Call video url form rapsi and show stream
    """

    cam = get_object_or_404(Cam, pk=pk)
    context = {'cam':cam}
    return render(request, 'videosite/cam_stream.html',context)

    