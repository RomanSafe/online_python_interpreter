import subprocess

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .forms import PythonInterpreterForm


class InterpreterView(View):
    """View for the main page logic.

    Attributes:
        template_name: template of the main page;
        optional_input: store input-output;
        timeout: server's response timeout in seconds.

    """

    template_name = "online_interpreter/index.html"
    optional_input = ""
    timeout = 5

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Serves GET HTTP requests.

        Args:
            request: HTTP request.

        Returns:
            HttpResponse: whose content is filled with the passed arguments
            (rendered to string).

        """

        return render(
            request,
            self.template_name,
            {"form": PythonInterpreterForm()},
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Serves POST HTTP requests.

        Args:
            request: HTTP request.

        Returns:
            HttpResponse: whose content is filled with the passed arguments
            (rendered to string).

        """

        form = PythonInterpreterForm(request.POST)
        if form.is_valid():
            self.optional_input = form.cleaned_data["std_io"]
            self.timeout = form.cleaned_data["timeout"]
            try:
                completed_process = subprocess.run(
                    ["python", "-I", "-c", form.cleaned_data["user_code"]],
                    input=self.optional_input,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=form.cleaned_data["timeout"],
                    text=True,
                )
                output = completed_process.stdout
            except subprocess.TimeoutExpired as exc:
                output = f"Timeout {exc.timeout} sec. expired."
            finally:
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
