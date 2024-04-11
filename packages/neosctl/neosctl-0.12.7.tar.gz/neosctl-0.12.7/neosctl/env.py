"""Environment commands, like env initialisation, deletion, and listing."""

import re
import typing

import click
import httpx
import tabulate
import typer

from neosctl import constant, schema, util

app = typer.Typer()


r = re.compile(r"http[s]?:\/\/.*")


def _validate_url(value: str) -> str:
    """Validate a given url is a valid url with schema."""
    m = r.match(value)
    if m is None:
        msg = f"Invalid url, must match pattern: `{r}`."
        raise click.UsageError(msg)
    return value


@app.command()
def init(
    ctx: typer.Context,
    name: str,
    *,
    hub_api_url: str = typer.Option(..., "--hub-api-url", "-h", callback=util.sanitize),
    username: str = typer.Option(..., "--username", "-u", callback=util.sanitize),
    account: str = typer.Option(..., "--account", "-a", callback=util.sanitize),
    ignore_tls: bool = typer.Option(
        False,
        "--ignore-tls",
        help="Ignore TLS errors (useful in local/development environments",
    ),
) -> None:
    """Initialise an environment.

    Create an environment that can be reused in later commands to define which
    services to interact with, and which user to interact as.

    Call `init` on an existing environment will update it.
    """
    typer.echo(f"Initialising [{name}] environment.")

    existing = ctx.obj.env.get(name, {})
    env = schema.Env(  # nosec: B106
        name=name,
        user=username,
        access_token="",
        refresh_token="",
        ignore_tls=ignore_tls,
        account=account,
        active=existing.get("active", False),
        active_core=existing.get("active_core"),
        hub_api_url=_validate_url(hub_api_url),
    )

    util.upsert_env(ctx, env)


@app.command()
def activate(
    ctx: typer.Context,
    name: str,
) -> None:
    """Activate an environment.

    Activate an environment to use its configuration for subsequent requests.
    """
    typer.echo(f"Activating [{name}] environment.")

    for name_ in ctx.obj.env:
        env = util.get_env_section(ctx.obj.env, name_)
        env.active = name == name_

        util.upsert_env(ctx, env)


@app.command(name="list")
def list_envs(
    ctx: typer.Context,
) -> None:
    """List available environments."""
    data = []
    for name in ctx.obj.env:
        env = util.get_env_section(ctx.obj.env, name)
        data.append([name, "*" if env.active else ""])
    typer.echo(tabulate.tabulate(data, headers=("Environment Name", "Active")))


@app.command()
def delete(
    ctx: typer.Context,
    name: str,
) -> None:
    """Delete an environment."""
    typer.confirm(f"Remove [{name}] environment", abort=True)
    util.remove_env(ctx, name)


@app.command()
def view(
    ctx: typer.Context,
    name: str,
) -> None:
    """View configuration for an environment."""
    env = util.get_env_section(ctx.obj.env, name)
    raise util.exit_with_output(
        msg=util.prettify_json(env.model_dump(mode="json")),
    )


@app.command()
def active(
    ctx: typer.Context,
) -> None:
    """View configuration for active environment."""
    util.check_env_active(ctx)

    raise util.exit_with_output(
        msg=util.prettify_json(ctx.obj.active_env.model_dump(mode="json")),
    )


@app.command()
def credentials(
    ctx: typer.Context,
    name: str,
    access_key_id: str,
    secret_access_key: str,
) -> None:
    """Configure access keys for an environment."""
    util.upsert_credential(ctx, access_key_id, secret_access_key, name=name)


def _auth_url(iam_api_url: str) -> str:
    return "{}".format(iam_api_url.rstrip("/"))


@app.command()
def login(
    ctx: typer.Context,
    password: typing.Optional[str] = typer.Option(None, "--password", "-p", callback=util.sanitize),
) -> None:
    """Login to environment."""
    util.check_env_active(ctx)

    if password is None:
        password = typer.prompt(
            f"[{ctx.obj.active_env.name}] Enter password for user ({ctx.obj.active_env.user})",
            hide_input=True,
        )

    r = util.post(
        ctx,
        "iam",
        f"{_auth_url(ctx.obj.get_hub_api_url())}/iam/login",
        json={"user": ctx.obj.active_env.user, "password": password},
    )

    if not util.is_success_response(r):
        util.process_response(r)

    d = r.json()
    ctx.obj.active_env.access_token = d["access_token"]
    ctx.obj.active_env.refresh_token = d["refresh_token"]

    util.upsert_env(ctx, ctx.obj.active_env)

    raise util.exit_with_output(
        msg="Login success",
        exit_code=0,
    )


@app.command()
def logout(ctx: typer.Context) -> None:
    """Logout from neos."""
    util.check_env_active(ctx)

    util.check_refresh_token_exists(ctx)

    r = util.post(
        ctx,
        "iam",
        f"{_auth_url(ctx.obj.get_hub_api_url())}/iam/logout",
        json={"refresh_token": ctx.obj.active_env.refresh_token},
    )

    if not util.is_success_response(r):
        util.process_response(r)

    ctx.obj.active_env.access_token = ""
    ctx.obj.active_env.refresh_token = ""

    util.upsert_env(ctx, ctx.obj.active_env)

    raise util.exit_with_output(
        msg="Logout success",
        exit_code=0,
    )


def _core_url(hub_api_url: str) -> str:
    return "{}/registry/core".format(hub_api_url.rstrip("/"))


@app.command(name="list-cores")
def list_cores(
    ctx: typer.Context,
) -> None:
    """List available cores."""
    util.check_env_active(ctx)

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.REGISTRY,
            _core_url(ctx.obj.get_hub_api_url()),
        )

    def tabulate_cores(data: dict[str, list]) -> str:
        ret = [
            [
                core["name"],
                core["version"],
                core["host"],
                core["account"],
                core["urn"],
                "*" if ctx.obj.active_env.active_core and core["name"] == ctx.obj.active_env.active_core.name else "",
            ]
            for core in data["cores"]
        ]
        return tabulate.tabulate(ret, headers=("Core Name", "Version", "Host", "Account", "Urn", "Active"))

    r = _request(ctx)
    util.process_response(r, render_callable=tabulate_cores)


@app.command(name="activate-core")
def activate_core(
    ctx: typer.Context,
    name: str,
) -> None:
    """Activate a core in current environment."""
    util.check_env_active(ctx)

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            constant.REGISTRY,
            _core_url(ctx.obj.get_hub_api_url()),
        )

    r = _request(ctx)
    if not util.is_success_response(r):
        util.process_response(r)

    active_core = None
    data = r.json()
    for core in data["cores"]:
        if core["name"] == name:
            active_core = core

    if active_core is None:
        raise util.exit_with_output(
            msg=f"Core {name} not found.",
            exit_code=1,
        )

    ctx.obj.active_env.active_core = schema.Core(**active_core)

    util.upsert_env(ctx, ctx.obj.active_env)


@app.command(name="set-account")
def set_account(
    ctx: typer.Context,
    account: str,
) -> None:
    """Switch active environment account."""
    util.check_env_active(ctx)

    ctx.obj.active_env.account = account

    util.upsert_env(ctx, ctx.obj.active_env)
