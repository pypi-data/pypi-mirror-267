import os
import re
import string
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Tuple, TypedDict

import click
import git
from git.exc import GitCommandError
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version
from pyproject_parser import PyProject
from ruamel.yaml import YAML


class DisplayMessage(TypedDict):
    message: str
    fallback: str


DisplayMessageType = List[DisplayMessage]


def _get_passed_params(ctx: click.Context) -> Dict:
    return {
        k: v
        for k, v in ctx.params.items()
        if ctx.get_parameter_source(k) == click.core.ParameterSource.COMMANDLINE
    }


def _get_toml_config(defaults: Dict) -> Dict:
    try:
        toml_file: PyProject = PyProject.load(
            os.path.join(os.getcwd(), "pyproject.toml")
        )
        return {**defaults, **toml_file.tool["pre-commit-update"]}
    except (FileNotFoundError, KeyError):
        return defaults


def _get_color(text: str, color: str) -> str:
    return click.style(str(text), fg=color)


def _get_yaml_file_contents(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        content: str = f.read()
    return content


def _set_yaml_file_contents(file_path: str, yaml_doc: YAML, data: Any) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        yaml_doc.dump(data, f)


def _get_target_tag(tags: List, all_versions: bool) -> str:
    if all_versions:
        return tags[0]
    for t in tags:
        if not any(v in t for v in ("a", "b", "rc")):
            return t
    return tags[0]


def _get_parsed_tags(repo: Dict) -> List:
    url: str = repo["repo"]
    try:
        remote_tags: List = (
            git.cmd.Git()
            .ls_remote("--exit-code", "--tags", url, sort="v:refname")
            .split("\n")
        )
        tags: List = []
        for tag in remote_tags:
            parsed_tag: str = re.split(r"\t+", tag)[1]
            if parsed_tag.endswith("^{}"):
                continue
            parsed_tag = parsed_tag.replace("refs/tags/", "")
            tags.append(parsed_tag)
        return tags
    except GitCommandError as ex:
        if ex.status == 2:
            message = f"No tags found for repo: {url}"
        else:
            message = f"Failed to list tags for repo: {url}"
        raise Exception(message)


def _get_repo_head_hash(repo: Dict) -> str:
    url: str = repo["repo"]
    return git.cmd.Git().ls_remote("--exit-code", url, "HEAD").split()[0]


def _is_a_hash(ver: str) -> bool:
    # The minimum length for an abbreviated hash is 4:
    # <https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreabbrev>.
    if len(ver) < 4:
        return False
    else:
        # Credit goes to Levon (https://stackoverflow.com/users/1209279/levon)
        # for this idea: <https://stackoverflow.com/a/11592279/7593853>.
        return all(character in string.hexdigits for character in ver)


def _get_target_ver(repo: Dict, tags: List, all_versions: bool) -> str:
    current_ver: str = repo["rev"]
    if current_ver in tags:
        return _get_target_tag(tags, all_versions)
    elif _is_a_hash(current_ver):
        return _get_repo_head_hash(repo)
    return current_ver


def _get_fixed_tag_versions(tag_versions: List) -> List:
    # Due to various prefixes that devs choose for tags, strip them down to semantic version numbers only.
    # Store it inside the dict ("ver1.2.3": "1.2.3") and parse the value to get the correct sort.
    # Return the original value (key) once everything is parsed/sorted.
    fixed_tag_versions: Dict = {}
    for tag in tag_versions:
        for prefix in re.findall("([a-zA-Z ]*)\\d*.*", tag):
            if not prefix:
                continue
            fixed_tag_versions[tag] = tag[len(prefix) :]
    try:
        fixed_tag_versions = {
            k: v
            for k, v in sorted(
                fixed_tag_versions.items(),
                key=lambda item: parse_version(item[1]),
                reverse=True,
            )
        }
    except InvalidVersion:
        pass
    return list(fixed_tag_versions.keys())


def _output_display_message(value: DisplayMessageType) -> None:
    try:
        click.echo("\n".join(x["message"] for x in value))
    except UnicodeEncodeError:
        click.echo("\n".join(x["fallback"] for x in value))


def run(
    dry_run: bool, all_versions: bool, verbose: bool, exclude: Tuple, keep: Tuple
) -> None:
    # Backup and set needed env variables
    git_terminal_prompt = os.getenv("GIT_TERMINAL_PROMPT", "0")
    python_io_encoding = os.getenv("PYTHONIOENCODING", "UTF-8")
    python_utf_8 = os.getenv("PYTHONUTF8", "1")
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    os.environ["PYTHONIOENCODING"] = "UTF-8"
    os.environ["PYTHONUTF8"] = "1"
    try:
        yaml: YAML = YAML()
        yaml.indent(sequence=4)
        yaml.preserve_quotes = True
        file_path: str = os.path.join(os.getcwd(), ".pre-commit-config.yaml")
        yaml_str: str = _get_yaml_file_contents(file_path)
        data: Any = yaml.load(yaml_str)
        no_update: DisplayMessageType = []
        to_update: DisplayMessageType = []
        ignored: DisplayMessageType = []
        kept: DisplayMessageType = []

        with ThreadPoolExecutor(max_workers=10) as pool:
            tasks: List = []
            for i in range(len(data["repos"])):
                repo: Dict = data["repos"][i]
                tasks.append(pool.submit(_get_parsed_tags, repo))

        for i, repository in enumerate(data["repos"]):
            if not repository["repo"].startswith("http"):
                continue
            repo = data["repos"][i]
            repo_name: str = repo["repo"].split("/")[-1]
            tag_versions: List = _get_fixed_tag_versions(tasks[i].result())
            target_ver: str = _get_target_ver(repo, tag_versions, all_versions)
            if repo_name in exclude:
                ignored_message: str = (
                    f"{repo_name} - {_get_color(repo['rev'], 'magenta')}"
                )
                ignored.append(
                    DisplayMessage(
                        message=f"{ignored_message} {_get_color(click.style('★', bold=True), 'magenta')}",
                        fallback=f"{ignored_message} {_get_color(click.style('*', bold=True), 'magenta')}",
                    )
                )
                continue
            if repo_name in keep:
                if repo["rev"] != target_ver:
                    kept_message: str = (
                        f"{repo_name} - {_get_color(repo['rev'] + ' -> ' + target_ver, 'blue')}"
                    )
                    kept.append(
                        DisplayMessage(
                            message=f"{kept_message} {_get_color(click.style('◉', bold=True), 'blue')}",
                            fallback=f"{kept_message} {_get_color(click.style('●', bold=True), 'blue')}",
                        )
                    )
                else:
                    kept_message = f"{repo_name} - {_get_color(repo['rev'], 'blue')}"
                    kept.append(
                        DisplayMessage(
                            message=f"{kept_message} {_get_color(click.style('◉', bold=True), 'blue')}",
                            fallback=f"{kept_message} {_get_color(click.style('●', bold=True), 'blue')}",
                        )
                    )
                continue
            if repo["rev"] != target_ver:
                to_update_message: str = (
                    f"{repo_name} - {_get_color(repo['rev'], 'yellow')} -> {_get_color(target_ver, 'red')}"
                )
                to_update.append(
                    DisplayMessage(
                        message=f"{to_update_message} {_get_color(click.style('✘', bold=True), 'red')}",
                        fallback=f"{to_update_message} {_get_color(click.style('×', bold=True), 'red')}",
                    )
                )
                data["repos"][i]["rev"] = target_ver
            else:
                no_update_message: str = (
                    f"{repo_name} - {_get_color(repo['rev'], 'green')}"
                )
                no_update.append(
                    DisplayMessage(
                        message=f"{no_update_message} {_get_color(click.style('✔', bold=True), 'green')}",
                        fallback=f"{no_update_message} {_get_color(click.style('√', bold=True), 'green')}",
                    )
                )

        if verbose:
            for output in (ignored, kept, no_update):
                if not output:
                    continue
                _output_display_message(output)

        if to_update:
            _output_display_message(to_update)
            if not dry_run:
                _set_yaml_file_contents(".pre-commit-config.yaml", yaml, data)
                click.echo(_get_color("Changes detected and applied", "green"))
            else:
                raise click.ClickException(_get_color("Changes detected", "red"))
        else:
            click.echo(_get_color("No changes detected", "green"))

    except Exception as ex:
        sys.exit(str(ex))

    finally:
        # Restore env variables
        os.environ["GIT_TERMINAL_PROMPT"] = git_terminal_prompt
        os.environ["PYTHONIOENCODING"] = python_io_encoding
        os.environ["PYTHONUTF8"] = python_utf_8


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-d/-nd",
    "--dry-run/--no-dry-run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry run only checks for the new versions without updating",
)
@click.option(
    "-a/-na",
    "--all-versions/--no-all-versions",
    is_flag=True,
    show_default=True,
    default=False,
    help="Include the alpha/beta versions when updating",
)
@click.option(
    "-v/-nv",
    "--verbose/--no-verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Display the complete output",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    default=(),
    help="Exclude specific repo(s) by the `repo` url trim",
)
@click.option(
    "-k",
    "--keep",
    multiple=True,
    default=(),
    help="Keep the version of specific repo(s) by the `repo` url trim (still checks for the new versions)",
)
@click.pass_context
def cli(ctx: click.Context, **_: Any):
    defaults: Dict = {p.name: p.default for p in ctx.command.params}
    cmd_params: Dict = _get_passed_params(ctx)
    toml_params: Dict = _get_toml_config(defaults)
    is_default: bool = defaults == ctx.params and len(cmd_params) == 0

    if is_default:
        run(**{**defaults, **toml_params})
        return

    run(**{**toml_params, **cmd_params})


if __name__ == "__main__":
    cli()
