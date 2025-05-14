from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'message-input', 'placeholder': 'Message...', 'required': True}))
    file = forms.FileField(widget=forms.FileInput(attrs={'id': 'id_file', 'accept': 'image/*', 'hidden': True}), required=False)