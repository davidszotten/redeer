from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render

from reeder.feeds.upload import import_google_reader


class UploadForm(forms.Form):
    reader_xml = forms.FileField()


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            import_google_reader(request.FILES['reader_xml'])
            redirect('upload-succes')
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


def upload_success(request):
    return HttpResponse("Upload successful")
