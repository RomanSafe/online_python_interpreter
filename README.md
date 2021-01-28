# Online_python_interpreter

It’s a simple web-form with two text fields and launch button.
We type source Python code in the left field, optionally can use the right field as stdin.
When you push the launch button source code and input data (if is) are sent to a server for execution. After execution stdout and stderr are shown in the right field.
There is a Python syntax highlighting.
The programme is packed using docker-compose.

## To run the programme use a follow command from folder where docker-compose-deploy.yml is located:
```docker-compose -f docker-compose-deploy.yml up --build```

This command build or rebuild services, create and start containers.

## To run the programme in debug mode use a follow command from folder where docker-compose.yml is located:
```docker-compose up```
