import re

from django import forms
from django.core.validators import RegexValidator


regex_validator_open = RegexValidator(
    regex=re.compile("open", flags=re.ASCII),
    message="You can't use open function",
    inverse_match=True,
)
regex_validator_eval = RegexValidator(
    regex=re.compile("eval", flags=re.ASCII),
    message="You can't use eval function",
    inverse_match=True,
)
regex_validator_exec = RegexValidator(
    regex=re.compile("exec", flags=re.ASCII),
    message="You can't use exec function",
    inverse_match=True,
)
regex_validator_os = RegexValidator(
    regex=re.compile(r"[%0-9\b]?os[\b%0-9]?", flags=re.ASCII),
    message="You can't use os module",
    inverse_match=True,
)
regex_validator_subprocess = RegexValidator(
    regex=re.compile("subprocess", flags=re.ASCII),
    message="You can't use subprocess module",
    inverse_match=True,
)
regex_validator_pathlib = RegexValidator(
    regex=re.compile("pathlib", flags=re.ASCII),
    message="You can't use pathlib module",
    inverse_match=True,
)
regex_validator_fileinput = RegexValidator(
    regex=re.compile("fileinput", flags=re.ASCII),
    message="You can't use fileinput module",
    inverse_match=True,
)
regex_validator_shutil = RegexValidator(
    regex=re.compile("shutil", flags=re.ASCII),
    message="You can't use shutil module",
    inverse_match=True,
)
regex_validator_parent_path = RegexValidator(
    regex=re.compile(r"\.\.[/\\]{1}", flags=re.ASCII),
    message="You can't go to the parent path",
    inverse_match=True,
)
regex_validator_ftp = RegexValidator(
    regex=re.compile(r".?ftp.?", flags=re.ASCII),
    message="You can't use ftp protocol",
    inverse_match=True,
)


class CodeForm(forms.Form):
    user_code = forms.CharField(
        widget=forms.Textarea,
        label=False,
        validators=[
            regex_validator_open,
            regex_validator_eval,
            regex_validator_exec,
            regex_validator_os,
            regex_validator_subprocess,
            regex_validator_pathlib,
            regex_validator_fileinput,
            regex_validator_shutil,
            regex_validator_parent_path,
            regex_validator_ftp,
        ],
    )


class StdIOForm(forms.Form):
    std_io = forms.CharField(widget=forms.Textarea, label=False, required=False)
