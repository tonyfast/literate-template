# `{{cookiecutter.name}}` command line interface

        import typer, {{cookiecutter.name}}

        def main(ctx: typer.Context):

the {{cookiecutter.name}} command line application

        app = typer.Typer()        
        app.command(context_settings=dict())(main)
