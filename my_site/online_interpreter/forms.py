from django import forms


class CodeForm(forms.Form):
    user_code = forms.CharField(widget=forms.Textarea, label=False)


class StdIOForm(forms.Form):
    std_io = forms.CharField(widget=forms.Textarea, label=False, required=False)
