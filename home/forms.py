from django import forms


class EssayForm(forms.Form):
    user_answer = forms.CharField(label = '',widget=forms.Textarea(attrs={"rows":20, 'class':'form-control', 'style':'line-height: 2.0; text-align: justify;', 'placeholder': 'Write your answer here...'}))
    question_type = forms.CharField(widget=forms.HiddenInput())
    question_text = forms.CharField(widget=forms.HiddenInput())
    question_topic = forms.CharField(widget=forms.HiddenInput())
