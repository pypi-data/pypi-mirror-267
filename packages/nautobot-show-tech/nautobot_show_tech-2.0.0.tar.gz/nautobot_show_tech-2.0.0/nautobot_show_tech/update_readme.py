#!/usr/bin/env python
"""This python script will update the README in show_tech_tests directory with information about each test in the directory."""

from inspect import cleandoc
import glob
import os
import yaml


dir_path = os.path.dirname(os.path.realpath(__file__))


def _main() -> None:
    """
    Run all the things!!!

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    # load all checks under show_tech_checks/
    checks = []
    for file in glob.iglob(dir_path + "/show_tech_checks/*.yaml"):
        with open(file, "r", encoding="utf-8") as text:
            check = yaml.load(text, Loader=yaml.SafeLoader)
        checks.append(check)

    header = """# Description
    This file contains information about the checks show_tech performs and should be used as reference for what this app can do.  Alternatively, you can use the commandline `show_tech --help`.

    # How to Read each YAML file
    * **Name:** name of the command to be run
    * **Description:** a short description of the command to be run and any considerations about that command
    * **Linux command:** exact command to be run against a Linux host
    * **Enabled:** do we want to run the command or turn it off

    # Current Commands
    """
    header = cleandoc(header)

    with open(dir_path + "/show_tech_checks/README.md", "w", encoding="utf-8") as file:
        file.write(f"{header}\n")
        # process checks
        for check in checks:
            check_name = check.get("name")
            command = check.get("os").get("linux").get("command")
            description = check.get("description")
            enabled = check.get("enabled")

            file.write(f"## {check_name}\n")
            file.write(f"* **Linux command:** {command}\n")
            file.write(f"* **Description:** {description}\n")
            file.write(f"* **Enabled:** {enabled}\n\n")


if __name__ == "__main__":
    _main()
