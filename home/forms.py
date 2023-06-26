from django import forms


class EssayForm(forms.Form):
    writing_task = forms.CharField(label = '',widget=forms.Textarea(attrs={"rows":20, 'class':'form-control', 'placeholder': 'Write your answer here...'}))
    question = forms.CharField(widget=forms.HiddenInput())
