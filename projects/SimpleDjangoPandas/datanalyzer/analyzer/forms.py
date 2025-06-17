# analyzer/forms.py
from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Upload your CSV file')

