import click
import yaml

from .cloud import ServerManager


__version__ = "0.1.2"


def load_applications(config_path):
    with open(config_path) as file:
        config = yaml.safe_load(file)
    return config["applications"]

def load_access(config_path):
    with open(config_path) as file:
        config = yaml.safe_load(file)
    return config["access"]

def list_applications(applications):
    for i, app in enumerate(applications, start=1):
        click.echo(f"{i}. {app['name']}")


@click.group()
def main():
    """CLI Tool for Managing Application Updates on Remote Servers."""
    pass


@click.command()
@click.version_option(version=__version__, prog_name='My CLI Application')
def version():
    """Display the version and exit."""
    click.echo(f"Version: {__version__}")


@click.command()
@click.option(
    "-a",
    "--application-name",
    default=None,
    help="Name of the application to update. If not provided, lists all applications.",
)
@click.option(
    "-c",
    "--config-yaml",
    default="./cloud.yaml",
    show_default=True,
    help="Path to the YAML configuration file.",
)
def update(application_name, config_yaml):
    """Updates the specified application on the remote server or lists all applications."""
    applications = load_applications(config_yaml)
    access = load_access(config_yaml)

    if application_name is None:
        click.echo("Available applications:")
        list_applications(applications)
        choice = click.prompt(
            "Please enter a number to update an application", type=int
        )
        if 0 < choice <= len(applications):
            application = applications[choice - 1]
        else:
            click.echo("Invalid choice.")
            return
    else:
        application = next(
            (app for app in applications if app["name"] == application_name), None
        )
        if not application:
            click.echo(f"Application '{application_name}' not found in configuration.")
            return
    server = next((i for i in access if i['profile']==application['profile']),None)
    server_ip, ssh_user, ssh_password = (
        server["host"],
        server["username"],
        server["password"],
    )
    manager = ServerManager(server_ip, ssh_user, ssh_password)
    output = manager.git_pull(application["git_repo_path"])
    if output:
        click.echo(f"Git pull output for '{application['name']}':\t{output}")
    else:
        click.echo(f"Git pull output for '{application['name']}':\tUnable to Get changes.")
    output = manager.restart_application(socket=application["socket_name"],service=application["service_name"])
    if output:
        click.echo(f"Restart application output for '{application['name']}':\t{output}")
    else:
        click.echo(f"Restart application output for '{application['name']}':\tUnable to Restart Application.")
    output = manager.git_application_status(service=application["service_name"])
    if output:
        click.echo(f"Application status for '{application['name']}':\t{output}")
    else:
        click.echo(f"Application status for '{application['name']}':\tUnable to Get Application Status.")
    
    manager.ssh_connect_close()


main.add_command(update)
main.add_command(version)

if __name__ == "__main__":
    main()
