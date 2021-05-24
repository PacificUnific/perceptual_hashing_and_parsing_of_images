from django import forms


ALGO = [
    ('1', 'aHash'),
    ('2', 'pHash (simple)'),
    ('3', 'pHash'),
    ('4', 'dHash (horizontal)'),
    ('5', 'dHash (vertical)')
]


class Form(forms.Form):
    img1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'textbox_url'}))
    img2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'textbox_url'}))
    algo = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'algorithm'}), choices=ALGO)


class ParseForm(forms.Form):
    req = forms.CharField(widget=forms.TextInput(attrs={'class': 'textbox_url'}))
    n = forms.CharField(widget=forms.TextInput(attrs={'class': 'textbox_url'}))


class SearchImagesForm(forms.Form):
    req = forms.CharField(widget=forms.TextInput(attrs={'class': 'textbox_url'}), required=False)
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'textbox_url', 'placeholder': 'YYYY-MM-DD'}),
                           required=False)
