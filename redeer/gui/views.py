from django.shortcuts import redirect, render

from redeer.feeds.models import Group
from redeer.feeds.upload import import_google_reader
from redeer.gui.forms import UploadForm


def index(request):
    return render(request, 'index.html', {
        'groups': Group.objects.order_by('title'),
    })


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            import_google_reader(request.FILES['reader_xml'])
            return redirect('upload-succes')
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


def upload_success(request):
    return render(request, "upload_success.html", {
        'groups': Group.objects.order_by('title'),
    })
