import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import typer

from igs_toolbox.file_utils import read_json_file
from igs_toolbox.log_utils import setup_logging
from igs_toolbox.version_utils import version_callback

if sys.version_info >= (3, 10):
    from typing import Annotated

    from zoneinfo import ZoneInfo
else:
    from backports.zoneinfo import ZoneInfo
    from typing_extensions import Annotated

TIMESTAMP = datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%dT%H-%M-%S")  # type: ignore[abstract]
app = typer.Typer()


def convert_valueset(
    input_path: Path,
    output_path: Path,
    pathogen: str,
) -> int:
    valueset_paths = Path.glob(input_path, f"*{pathogen}.json")
    output_path.mkdir(exist_ok=True, parents=True)
    try:
        valueset_path = next(valueset_paths)
    except StopIteration:
        logging.warning(f"No valueset given for pathogen {pathogen}. Aborting.")
        return 1
    try:
        # get vocabulary for the pathogen
        valueset = read_json_file(Path(valueset_path))
    except FileNotFoundError:
        logging.warning(f"{valueset_path} does not point to a file. Aborting.")
        return 1
    except json.JSONDecodeError:
        logging.warning(f"{valueset_path} is not a valid json file. Aborting.")
        return 1

    valueset_list = [species["display"] for species in valueset["compose"]["include"][0]["concept"]]

    with (output_path / f"valueSet{pathogen}.txt").open("w") as fp:
        for item in valueset_list:
            fp.write(f"{item}\n")
        logging.info(f"Converted {valueset_path}")
    return 0


@app.command(name="convertValueSets", help="Convert json valuesets to txt files.")
def convert_valuesets(
    input_folder: Annotated[
        Path,
        typer.Option(
            ...,
            "--input",
            "-i",
            dir_okay=True,
            file_okay=False,
            exists=True,
            help="Path to input folder containing valueset json files.",
        ),
    ],
    output_folder: Annotated[
        Path,
        typer.Option(
            ...,
            "--output",
            "-o",
            dir_okay=True,
            file_okay=False,
            help="Path to output folder for txt files.",
        ),
    ],
    pathogens: Annotated[
        Tuple[str, ...],
        typer.Option("--pathogens", "-p", help="List of pathogens for which to convert valuesets."),
    ] = (
        "EHCP",
        "LISP",
        "SALP",
        "STYP",
        "INVP",
        "NEIP",
        "MSVP",
        "MYTP",
        "CVDP",
        "HIVP",
        "NEGP",
        "EBCP",
        "ACBP",
        "CDFP",
        "MRAP",
        "SALP",
        "HEVP",
        "HAVP",
        "LEGP",
        "SPNP",
        "WNVP",
    ),
    log_file: Annotated[
        Path,
        typer.Option("--log_file", "-l", dir_okay=False, help="Path to log file."),
    ] = Path(f"./convertValueSets_{TIMESTAMP}.log"),
    version: Annotated[  # noqa: ARG001
        Optional[bool],
        typer.Option("--version", "-V", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    setup_logging(log_file=log_file, debug=False)
    output_folder.mkdir(parents=True, exist_ok=True)
    for pathogen in pathogens:
        convert_valueset(input_folder, output_folder, pathogen)
    print("Convertion finished. Check log file for info about converted and skipped valuesets.")  # noqa: T201


def main() -> None:
    app()


if __name__ == "__main__":
    main()
