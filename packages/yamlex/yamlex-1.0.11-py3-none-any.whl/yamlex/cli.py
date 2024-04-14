import json
import logging
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated
from rich import print

from yamlex.mapper import (
    validate_json_schemas_dir,
    map_schema_to_sources,
    read_vscode_settings_json_file,
    extract_definitions_into_standalone_schemas,
)
from yamlex.splitter import split_yaml
from yamlex.joiner import (
    assemble_recursively,
    remove_yaml_comments,
)
from yamlex.util import (
    adjust_root_logger,
    get_default_extension_dir_path,
    get_default_extension_source_dir_path,
    is_manually_created,
    write_file,
    read_version_properties,
    write_version_properties,
    parse_version,
    bump_version,
    get_version,
)


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


app = typer.Typer(
    name="yamlex",
    rich_markup_mode="rich",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

force_option = Annotated[
    bool,
    typer.Option(
        "--force",
        "-f",
        help="Overwrite the files even if they were created manually.",
    ),
]
comment_option = Annotated[
    str,
    typer.Option(
        "--comment",
        "-c",
        help="Comment to add at the top of the YAML.",
    ),
]
verbose_option = Annotated[
    bool,
    typer.Option(
        "--verbose",
        help="Enable verbose output.",
    ),
]
quiet_option = Annotated[
    bool,
    typer.Option(
        "--quiet",
        help="Disable any informational output. Only errors.",
    ),
]
debug_option = Annotated[
    bool,
    typer.Option(
        "--debug",
        hidden=True,
    ),
]
version_option = Annotated[
    Optional[bool],
    typer.Option(
        "--version",
        "-v",
        show_default=False,
        is_eager=True,
    ),
]


@app.command(help="Map JSON schema to YAML files in VS Code settings")
def map(
    settings: Annotated[
        Path,
        typer.Argument(
            help="Path to the VS Code settings.json file.",
        ),
    ] = Path(".vscode/settings.json"),
    schema: Annotated[
        Path,
        typer.Option(
            "--json",
            "-j",
            help="Path to directory with valid extensions JSON schema files.",
            exists=True,
            readable=True,
            dir_okay=True,
            file_okay=False,
        ),
    ] = Path("schema"),
    source: Annotated[
        Optional[Path],
        typer.Option(
            "--source",
            "-s",
            help=(
                "Path to directory where YAML source files will be stored. "
                "[dim]\\[default: source or src/source][/dim]"
            ),
            show_default=False,
            dir_okay=True,
            file_okay=False,
        )
    ] = None,
    root: Annotated[
        Path,
        typer.Option(
            "--root",
            "-r",
            help="Root directory relative to which the paths in settings file will be mapped.",
            dir_okay=True,
            file_okay=False,
        )
    ] = Path("."),
    extension_yaml: Annotated[
        Optional[Path],
        typer.Option(
            "--extension-yaml",
            "-e",
            help=(
                "Path to output extension.yaml file. "
                "[dim]\\[default: extension/extension.yaml or src/extension/extension.yaml][/dim]"
            ),
            show_default=False,
            dir_okay=False,
            file_okay=True,
        )
    ] = None,
    verbose: verbose_option = False,
    quiet: quiet_option = False,
) -> None:
    """Map YAML files to JSON schema."""
    adjust_root_logger(verbose, quiet)
    logger.debug(f"JSON schema files directory: {schema}")
    logger.debug(f"VS Code settings.json file: {settings}")
    logger.debug(f"Root dir: {root}")

    source = source or get_default_extension_source_dir_path()
    logger.debug(f"Extension YAML source files directory: {source}")

    extension_yaml = extension_yaml or get_default_extension_dir_path() / "extension.yaml"
    logger.debug(f"extension.yaml file: {extension_yaml}")

    # Make sure schemas directory contains extension.schema.json
    validate_json_schemas_dir(schema)

    # Make schema more granular by extracting embedded definitions into
    # separate schema files.
    extract_definitions_into_standalone_schemas(schema)

    # Update yaml.schemas mapping in settings.json
    vscode_settings = read_vscode_settings_json_file(settings)

    # Delete existing extension.yaml mapping
    mapping: dict = vscode_settings.get("yaml.schemas", {})
    for k, v in mapping.items():
        if "extension.yaml" in str(v):
            del mapping[k]
            break
    
    # Update the mapping
    mapping_update = map_schema_to_sources(schema, source, root, extension_yaml)
    mapping.update(mapping_update)

    # Write the updated settings.json file
    vscode_settings["yaml.schemas"] = mapping
    with open(settings, "w") as f:
        vscode_settings_file_text = json.dumps(vscode_settings, indent=2)
        f.write(vscode_settings_file_text)
        logger.info(f"Updated {settings} with new YAML schema mappings.")


@app.command(help="Split central YAML file into parts.")
def split(
    source: Annotated[
        Optional[Path],
        typer.Option(
            "--source",
            "-s",
            help=(
                "Path to source extension.yaml file. "
                "[dim]\\[default: extension/extension.yaml or src/extension/extension.yaml][/dim]"
            ),
            show_default=False,
            dir_okay=False,
            file_okay=True,
            exists=True,
            readable=True,
        ),
    ] = None,
    target: Annotated[
        Optional[Path],
        typer.Option(
            "--target",
            "-t",
            help=(
                "Path to directory where split YAML source files will be stored. "
                "[dim]\\[default: source or src/source][/dim]"
            ),
            show_default=False,
            dir_okay=True,
            file_okay=False,
            exists=True,
            writable=True,
        ),
    ] = None,
    comment: comment_option = 'This file was generated by yamlex',
    force: force_option = False,
    verbose: verbose_option = False,
    quiet: quiet_option = False,
) -> None:
    adjust_root_logger(verbose, quiet)

    source = source or get_default_extension_dir_path() / "extension.yaml"
    logger.debug(f"Source file: {source}")

    target = target or get_default_extension_source_dir_path()
    logger.debug(f"Target directory: {target}")

    split_parts = split_yaml(source, target)

    for path, part in split_parts.items():
        if is_manually_created(path) and not force:
            logger.info(f"(Skipping) Part: {path}")
        else:
            write_file(path, part, comment)
            logger.info(f"Part written: {path}")


@app.command(help="Join YAML files into a single file.")
def join(
    source: Annotated[
        Optional[Path],
        typer.Option(
            "--source",
            "-s",
            help=(
                "Path to directory where split YAML source files are stored. "
                "[dim]\\[default: csource or src/source][/dim]"
            ),
            show_default=False,
            dir_okay=True,
            file_okay=False,
            exists=True,
            readable=True,
        )
    ] = None,
    target: Annotated[
        Optional[Path],
        typer.Option(
            "--target",
            "-t",
            help=(
                "Path for target extension.yaml file that will be assembled from parts. "
                "[dim]\\[default: extension/extension.yaml or src/extension/extension.yaml][/dim]"
            ),
            show_default=False,
            dir_okay=False,
            file_okay=True,
        )
    ] = None,
    dev: Annotated[
        bool,
        typer.Option(
            "--dev",
            "-d",
            help="Prefix extension name with 'custom:' and use explicit version.",
        ),
    ] = False,
    bump: Annotated[
        bool,
        typer.Option(
            "--bump",
            "-b",
            help="Bump version in the version.properties file.",
        ),
    ] = False,
    multiline_strings: Annotated[
        bool,
        typer.Option(
            "--multiline",
            "-m",
            help="Non YAML files are embedded as multiline strings.",
        ),
    ] = True,
    version: Annotated[
        Optional[str],
        typer.Option(
            "--version",
            "-v",
            help="Explicitly set the version to use during assembly or bump process."
        ),
    ] = None,
    comment: comment_option = 'This file was generated by yamlex',
    force: force_option = False,
    verbose: verbose_option = False,
    quiet: quiet_option = False,
    debug: debug_option = False,
) -> None:
    adjust_root_logger(verbose, quiet)

    source = source or get_default_extension_source_dir_path()
    logger.debug(f"Source files directory: {source}")

    extension = assemble_recursively(
        source,
        non_yaml_files_as_multiline_string=multiline_strings,
        debug=debug,
    )

    # Figure out the current version
    yaml_version = extension.get("version")
    is_read_from_version_properties = False
    # If new version is not explicitly specified
    if not version:
        current_version = parse_version(yaml_version)
        if not current_version:
            current_version = read_version_properties("version.properties")
            is_read_from_version_properties = True
        logger.info(f"Current version: {current_version}")

    
    # Bump version, if requested
    if bump:
        # If new version is not explicitly specified
        if not version:
            # If new explicit version is not specified, then
            # parse current version and bump it.
            version = bump_version(current_version)

        if is_read_from_version_properties:
            write_version_properties("version.properties", version)
        logger.info(f"Bumped version to {version}")

    if dev:
        name = extension.get("name")
        if isinstance(name, str) and not name.startswith("custom:"):
            name = f"custom:{name}"
            extension["name"] = name
            logger.info(f"Set extension name to: {name}")

    # Update version, if new explicit version was specified
    if not version:
        version = current_version
    if yaml_version != version:
        extension["version"] = version
        logger.info(f"Set extension version to: {version}")

    target = target or get_default_extension_dir_path() / "extension.yaml"
    logger.debug(f"Target file: {target}")

    # Check if the target file exists and was created manually
    if is_manually_created(target) and not force:
        logger.error(f"The {target} file was created manually. Use --force to overwrite it.")
        exit(2)

    # Remove comments
    remove_yaml_comments(extension)

    # Write to output file
    write_file(target, extension, comment)

    if debug:
        print(extension)


@app.callback(
    invoke_without_command=True,
    no_args_is_help=True,
)
def callback(
    ctx: typer.Context,
    version: version_option = None,
) -> None:
    if version:
        prog_version = get_version()
        print(prog_version)

        raise typer.Exit()
    
    if ctx.invoked_subcommand:
        return


def run() -> None:
    app.command(name="j", hidden=True)(join)
    app.command(name="s", hidden=True)(split)
    app()
