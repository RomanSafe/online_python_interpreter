import io
import sys

from django.shortcuts import render
from django.views import View

from .forms import CodeForm, StdIOForm


class InterpreterView(View):
    template_name = "online_interpreter/index.html"
    initial_code = "# Type your Python code here and push Launch button.\n"
    optional_input = ""

    def get(self, request, *args, **kwargs):
        left_form = CodeForm(initial={"user_code": self.initial_code})
        right_form = StdIOForm()
        return render(
            request,
            self.template_name,
            {
                "code_form": left_form,
                "stdio_form": right_form,
            },
        )

    def post(self, request, *args, **kwargs):
        left_form = CodeForm(request.POST)
        right_form = StdIOForm(request.POST)
        if left_form.is_valid() and right_form.is_valid():
            self.optional_input = right_form.cleaned_data["std_io"]

            _stdout = io.StringIO()
            _stdin = io.StringIO()
            # capture sys.stdout, sys.stdin
            _stdout = sys.stdout
            _stdin = sys.stdin

            codeOut = io.StringIO()
            codeIn = io.StringIO(initial_value=self.optional_input)
            # replace sys.stdout, sys.stdin
            sys.stdout = codeOut
            sys.stdin = codeIn
            # run code and catch exceptions
            try:
                exec(left_form.cleaned_data["user_code"])
            except Exception as exc:
                print(sys.exc_info()[0])
                print(exc.args)

            # restore sys.stdout and sys.stdin
            sys.stdout = _stdout
            sys.stdin = _stdin

            output = codeOut.getvalue()

            codeOut.close()
            codeIn.close()

            if self.optional_input:
                self.optional_input = f'{self.optional_input}\n{output}'
            else:
                self.optional_input = output
            right_form = StdIOForm(initial={"std_io": self.optional_input})
            return render(
                request,
                self.template_name,
                {
                    "code_form": left_form,
                    "stdio_form": right_form,
                },
            )

        return render(
            request,
            self.template_name,
            {
                "code_form": left_form,
                "stdio_form": right_form,
            },
        )
