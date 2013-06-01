from django import forms


class UploadForm(forms.Form):
    reader_xml = forms.FileField()
