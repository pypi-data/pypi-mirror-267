import os

import click

from highlighter.cli.config import config_group
from highlighter.cli.dataset import dataset_group
from highlighter.cli.experiment import experiment_group
from highlighter.cli.data_files import data_file_group
from highlighter.cli.object_class import object_class_group
from highlighter.cli.assessment import assessment_group
from highlighter.cli.task import task_group
from highlighter.cli.training_run import training_run_group
from highlighter.cli.step import step_group
from highlighter.gql_client import (
    CONST_DEFAULT_GRAPHQL_PROFILES_YAML, ENV_HL_WEB_GRAPHQL_API_TOKEN,
    ENV_HL_WEB_GRAPHQL_ENDPOINT, HLClient)
from highlighter.logging import LOG as logger


class NoHLClientCredentialsError(Exception):
    def __init__(self):
        message = (
            "\nNo way of determining credentials for HLClient "
            "could be found. \n"
            "\tOption 1: Use the --profile flag in the cli\n"
            "\tOption 2: Use the --api-token and --endpoint-url flags in the cli\n"
            "\tOption 3: export environment variables"
        )
        super().__init__(message)


class NoHLClient:
    """
    Fallback class for when a user does not provide a way
    of deterimining Highlighter credentials. This allows them
    to run help commands and other commands like 'config' that
    do not rely on a working HLClient, but will give a nice
    error message when they do.
    """

    def __getattr__(self, key):
        raise NoHLClientCredentialsError()

    def __repr__(self):
        return "NoHLClient"


@click.group("highlighter")
@click.option("--api-token", type=str)
@click.option("--endpoint-url", type=str)
@click.option("--profile", type=str, default=None)
@click.option("--profiles-path", type=str, default=CONST_DEFAULT_GRAPHQL_PROFILES_YAML)
@click.pass_context
def highlighter_group(ctx, api_token, endpoint_url, profile, profiles_path):
    if profile is not None:
        client = HLClient.from_profile(profile=profile)
    elif (endpoint_url is not None) and (api_token is not None):
        client = HLClient.from_credential(
            api_token=api_token,
            endpoint_url=endpoint_url,
        )
    elif ENV_HL_WEB_GRAPHQL_ENDPOINT in os.environ:
        client = HLClient.from_env()
    else:

        client = NoHLClient()

    ctx.obj = {"client": client}
    logger.debug(f"HLClient: {client}")


@highlighter_group.command("write")
@click.argument("outfile", type=str)
@click.pass_context
def write(ctx, outfile):
    """Write credentials to a file.

    Each credential is appended to the given file.

    eg: highlighter-v2 --profile abc .envrc

    Results in the following lines being appended
    the .envrc

    export HL_WEB_GRAPHQL_ENDPOINT=...
    export HL_WEB_GRAPHQL_API_TOKEN=...
    """
    client = ctx.obj["client"]
    client.append_credentials_to_env_file(outfile)


@highlighter_group.command("export")
@click.pass_context
def export(ctx):
    """Export a profile's credentials to env

    Wrap this command in `back ticks` to export a profile's credentials to
    your environment

    eg: `highlighter-v2 --profile abc export`

    Results in the following credentials being
    added to your environment variables

    HL_WEB_GRAPHQL_ENDPOINT=...
    HL_WEB_GRAPHQL_API_TOKEN=...
    """
    client = ctx.obj["client"]

    click.echo("Wrap the command in `back ticks` to execute the exports", err=True)
    click.echo(
        f"export {ENV_HL_WEB_GRAPHQL_ENDPOINT}={client.endpoint_url} {ENV_HL_WEB_GRAPHQL_API_TOKEN}={client.api_token}"
    )


highlighter_group.add_command(config_group)
highlighter_group.add_command(object_class_group)
highlighter_group.add_command(data_file_group)
highlighter_group.add_command(dataset_group)
highlighter_group.add_command(assessment_group)
highlighter_group.add_command(training_run_group)
highlighter_group.add_command(step_group)
highlighter_group.add_command(experiment_group)
highlighter_group.add_command(task_group)


if __name__ == "__main__":
    highlighter_group()
