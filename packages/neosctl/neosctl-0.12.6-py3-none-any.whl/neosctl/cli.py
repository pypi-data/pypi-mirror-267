"""Command line interface for neosctl."""

import configparser
import importlib.metadata
import logging
import os
import typing

import click
import typer
from rich.logging import RichHandler

from neosctl import (
    auth,
    constant,
    profile,
    schema,
    services,
    util,
)
from neosctl.util import get_user_profile, read_config_dotfile, read_credential_dotfile, user_profile_callback

logger = logging.getLogger(__name__)

VERBOSITY = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}


def _generate_common_schema(
    gateway_api_url: str,
    hub_api_url: str,
    storage_api_url: str,
    profile_name: str,
    config: configparser.ConfigParser,
    credential: configparser.ConfigParser,
    profile: typing.Union[schema.Profile, schema.OptionalProfile, None] = None,
) -> schema.Common:
    """Generate a common schema object.

    Set the default api values using user_profile and cli provided defaults.
    """
    common_schema = schema.Common(
        gateway_api_url=gateway_api_url,
        hub_api_url=hub_api_url,
        storage_api_url=storage_api_url,
        profile_name=profile_name,
        config=config,
        credential=credential,
        profile=profile,
    )
    common_schema.gateway_api_url = common_schema.get_gateway_api_url()
    common_schema.hub_api_url = common_schema.get_hub_api_url()
    common_schema.storage_api_url = common_schema.get_storage_api_url()

    return common_schema


def _version_callback(*, value: bool) -> None:
    """Get current cli version."""
    if value:
        version = importlib.metadata.version("neosctl")
        typer.echo(f"neosctl {version}")
        raise typer.Exit


def setup_logging(verbose: int = 0) -> None:
    """Configure the logging."""
    logging.basicConfig(
        level=VERBOSITY.get(verbose, logging.DEBUG),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                show_level=False,
                show_path=False,
                show_time=False,
                tracebacks_suppress=[click],
            ),
        ],
    )
    asyncio_logger = logging.getLogger("asyncio")
    asyncio_logger.disabled = True
    root_logger = logging.getLogger("")
    root_logger.setLevel(VERBOSITY.get(verbose, logging.DEBUG))


def _callback(
    ctx: typer.Context,
    version: typing.Optional[bool] = typer.Option(  # noqa: ARG001
        None,
        "--version",
        callback=_version_callback,
        help="Print version and exit.",
    ),
    gateway_api_url: str = typer.Option(
        "",
        "--gateway-api-url",
        "--gurl",
        help="Gateway API URL",
        callback=util.sanitize,
    ),
    hub_api_url: str = typer.Option(
        "",
        "--hub-api-url",
        "--hurl",
        help="Hub API URL",
        callback=util.sanitize,
    ),
    storage_api_url: str = typer.Option(
        "",
        "--storage-api-url",
        "--surl",
        help="Storage API URL",
        callback=util.sanitize,
    ),
    profile: str = typer.Option(
        os.getenv("NEOSCTL_PROFILE", constant.DEFAULT_PROFILE),
        "--profile",
        "-p",
        help="Profile name",
        callback=util.sanitize,
    ),
    verbose: int = typer.Option(
        0,
        "-v",
        "--verbose",
        help="Verbose output. Use multiple times to increase level of verbosity.",
        count=True,
        max=3,
    ),
) -> None:
    """Inject common configuration defaults into context.

    Allow missing user_profile to support profile generation etc.
    """
    setup_logging(verbose)
    config = read_config_dotfile()
    credential = read_credential_dotfile()
    user_profile = get_user_profile(config, profile, allow_missing=True)

    logger = logging.getLogger("neosctl.error")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(constant.LOG_FILEPATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    common_schema = _generate_common_schema(
        gateway_api_url=gateway_api_url,
        hub_api_url=hub_api_url,
        storage_api_url=storage_api_url,
        profile_name=profile,
        config=config,
        credential=credential,
        profile=user_profile,
    )

    ctx.obj = common_schema


app = typer.Typer(name="neosctl", callback=_callback)
app.add_typer(profile.app, name="profile", help="Manage profiles.")
app.add_typer(auth.app, name="auth", callback=user_profile_callback, help="Manage authentication status.")
app.add_typer(services.iam.app, name="iam", callback=user_profile_callback, help="Manage access policies.")
app.add_typer(
    services.storage.app,
    name="storage",
    callback=user_profile_callback,
    help="Interact with Storage (as a service).",
)
app.add_typer(
    services.gateway.app,
    name="gateway",
    callback=user_profile_callback,
    help="Interact with Gateway service.",
)
app.add_typer(
    services.registry.app,
    name="registry",
    callback=user_profile_callback,
    help="Manage cores and search data products.",
)
