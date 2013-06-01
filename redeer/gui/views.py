from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


from redeer.feeds.models import Group
from redeer.feeds.upload import import_google_reader
from redeer.gui.forms import UploadForm


def index(request):
    if request.user.is_authenticated():
        groups = Group.objects.order_by('title')
    else:
        groups = []

    return render(request, 'index.html', {
        'groups': groups
    })


def login(request):
    pass


def logout(request):
    pass


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            import_google_reader(request.FILES['reader_xml'])
            return redirect('upload-succes')
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


@login_required
def upload_success(request):
    return render(request, "upload_success.html", {
        'groups': Group.objects.order_by('title'),
    })
