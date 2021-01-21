import io
import sys

from django.shortcuts import render
from django.views import View

from .forms import PythonInterpreterForm


class InterpreterView(View):
    template_name = "online_interpreter/index.html"
    optional_input = ""
    timeout = 10

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"form": PythonInterpreterForm()},
        )

    def post(self, request, *args, **kwargs):
        form = PythonInterpreterForm(request.POST)
        if form.is_valid():
            self.optional_input = form.cleaned_data["std_io"]
            self.timeout = form.cleaned_data["timeout"]

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
                exec(form.cleaned_data["user_code"])
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
                self.optional_input = f"{self.optional_input}\n{output}"
            else:
                self.optional_input = output
            form = PythonInterpreterForm(
                {
                    "user_code": form.cleaned_data["user_code"],
                    "std_io": self.optional_input,
                    "timeout": self.timeout,
                }
            )
            return render(request, self.template_name, {"form": form})

        return render(request, self.template_name, {"form": form})
