"""This module implements the command line interface for tgcf."""

import asyncio
import logging
import os
import sys
from enum import Enum
from typing import Optional

import typer
from dotenv import load_dotenv
from rich import console, traceback
from rich.logging import RichHandler

from test_tele import __version__

load_dotenv(".env")

FAKE = bool(os.getenv("FAKE"))
app = typer.Typer(add_completion=False)

con = console.Console()


def topper():
    print("tgcf")
    print("\n")


class Mode(str, Enum):
    """tgcf works in two modes."""

    PAST = "past"
    LIVE = "live"


def verbosity_callback(value: bool):
    """Set logging level."""
    traceback.install()
    if value:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                markup=True,
            )
        ],
    )
    # topper()
    logging.info("Verbosity turned on! This is suitable for debugging")


def version_callback(value: bool):
    """Show current version and exit."""

    if value:
        con.print(__version__)
        raise typer.Exit()
    

@app.command()
def main(
    mode: Mode = typer.Argument(
        ..., help="Choose the mode in which you want to run tgcf.", envvar="TGCF_MODE"
    ),
    verbose: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
        None,
        "--loud",
        "-l",
        callback=verbosity_callback,
        envvar="LOUD",
        help="Increase output verbosity.",
    ),
    version: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
        None,
        "--version",
        "-v",
        callback=version_callback,
        help="Show version and exit.",
    ),
):
    """The ultimate tool to automate custom telegram message forwarding.

    Source Code: https://github.com/aahnik/tgcf

    For updates join telegram channel @aahniks_code

    To run web interface run `tgcf-web` command.
    """
    if FAKE:
        logging.critical(f"You are running fake with {mode} mode")
        sys.exit(1)

    if mode == Mode.PAST:
        from test_tele.past import forward_job  # pylint: disable=import-outside-toplevel

        asyncio.run(forward_job())
    else:
        from test_tele.live import start_telethon, start_pyrogram  # pylint: disable=import-outside-toplevel
        
        async def main():
            await asyncio.gather(
                start_telethon(),
                start_pyrogram()
            )       

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()

