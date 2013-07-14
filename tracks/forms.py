from django import forms

class CreateTrack(forms.Form):
    title = forms.CharField()
    file  = forms.FileField()

class UpdateTrack(forms.Form):
    title = forms.CharField()
