import os
import click
import requests
from colorama import Fore, Style

# Set the base URL for the prompt library (default or from environment variable)
PROMPT_LIBRARY_URL = os.getenv("PROMPT_LIBRARY_URL", "http://prompt-library.org")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("repository")
def clone(repository):
    try:
        # Send a GET request to the prompt library URL
        response = requests.get(f"{PROMPT_LIBRARY_URL}/{repository}")
        response.raise_for_status()

        # Extract the repo name from the repository argument
        repo_name = repository.split("/")[-1]

        # Create a directory for the cloned repository
        os.makedirs(repo_name, exist_ok=True)

        # Save the prompt content to a file in the repository directory
        with open(f"{repo_name}/prompt.txt", "w") as file:
            file.write(response.text)

        click.echo(
            Fore.GREEN
            + f"Successfully cloned repository: {repository}"
            + Style.RESET_ALL
        )
    except requests.exceptions.RequestException as e:
        click.echo(
            Fore.RED + f"Error cloning repository: {repository}" + Style.RESET_ALL
        )
        click.echo(Fore.RED + str(e) + Style.RESET_ALL)


@cli.command()
@click.argument("repo_name")
def run(repo_name):
    try:
        # Load the prompt from the cloned repository
        with open(f"{repo_name}/prompt.txt", "r") as file:
            prompt = file.read()

        click.echo(Fore.BLUE + "Running prompt:" + Style.RESET_ALL)
        click.echo(prompt)

        # Execute the prompt using the appropriate agent or interpreter
        # (You need to implement this part based on your specific requirements)
        result = execute_prompt(prompt)

        click.echo(Fore.GREEN + "Prompt execution result:" + Style.RESET_ALL)
        click.echo(result)
    except FileNotFoundError:
        click.echo(
            Fore.RED
            + f'Error: Repository "{repo_name}" not found. Please clone the repository first.'
            + Style.RESET_ALL
        )
    except Exception as e:
        click.echo(Fore.RED + f"Error running prompt: {repo_name}" + Style.RESET_ALL)
        click.echo(Fore.RED + str(e) + Style.RESET_ALL)


def execute_prompt(prompt):
    # Placeholder function for executing the prompt
    # Replace this with your actual implementation
    return f"Executed prompt: {prompt}"


if __name__ == "__main__":
    cli()
