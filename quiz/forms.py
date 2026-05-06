from django import forms


class StartForm(forms.Form):
    email = forms.EmailField(
        label="Votre email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'votre@email.com'
        })
    )
    consent = forms.BooleanField(
        label="J’accepte que mes données soient utilisées pour recevoir mon résultat.",
        required=True
    )
