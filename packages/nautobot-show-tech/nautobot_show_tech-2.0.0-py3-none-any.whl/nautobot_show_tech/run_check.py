"""This script runs commands from yaml formated files against a host and returns the command response as files based on instructions from the yaml files."""

import datetime
import glob
import os
import platform
import sys
from django.conf import settings
from importlib import import_module
from pprint import pprint
import click
import requests
from nautobot_show_tech import helpers
from . import __version__


# Global - run command `show_tech`` from any directory
dir_path = os.path.dirname(os.path.realpath(__file__))

###
# Schemas and Standards
###
# check schema
# {
# "name" = string,
# "description" = string,
# "os" = {
#   "linux" = {
#     "command" = string,
#   },
# },
# "enabled" = boolean,
# "prompt_warning" = string,
# "entry_point" = string,
# "entry_point_options" = {},
# }

# API Output Schema
# {
# 'check_name': {'command': 'date',
#          'command_result': 'Tue Nov 21 16:28:19 UTC 2023',
#          'command_result_error': '',
#          'command_result_status': 'Success',
#          'command_result_type': 'string',
#          'entry_point_error': ''},
# 'output_version': 'v1'}
# }


###
# Run check and process checks
###
def run_check(check: dict = None) -> dict:
    """
    This function runs a show_tech_check using the entry_point defined.

    Args:
        check:
            example: {"name": "pip_freeze", "command": "pip freeze", "entry_point_options" = {}}

    Returns:
        response: {check_name: {data}} where data is json or raw format
    """
    if not check:
        print("No check provided.")
        sys.exit()
    # confirm host os and only run the command for the correct os
    # https://docs.python.org/3/library/sys.html#sys.platform
    if platform.system().lower():
        host_os = "linux"
    else:
        print("Aborted.")
        sys.exit()
    # grab the required fields to run the check: check_name, command, entry_point kwargs
    check_name = check.get("name")
    command = check.get("os").get(host_os).get("command")
    entry_point_options = check.pop("entry_point_options")
    entry_point_kwargs = {}
    if entry_point_options:
        for option, option_details in entry_point_options.items():
            entry_point_kwargs[option] = option_details.get("value")

    # dynamically import Check.run() method from check.yaml entry_point
    entry_point = check.pop("entry_point").strip(".py")
    module = getattr(import_module(f"nautobot_show_tech.show_tech_checks.{entry_point}"), "Check")

    response = module.run(check_name=check_name, command=command, **entry_point_kwargs)

    return response


def retrieve_all_checks(enabled_only: bool = False) -> list:
    """
    This function finds all enabled checks in /show_tech_checks/*yaml.

    Args:
        enabled_only: true/false - only returns a list of enabled checks

    Returns:
        checks: a list of all or all enabled checks in /show_tech_checks.
    """
    checks = []
    for file in glob.iglob(dir_path + "/show_tech_checks/*.yaml"):
        check = helpers.open_yaml_file(file)
        # search for enabled checks if true
        if enabled_only:
            enabled = check.get("enabled")
            if enabled:
                checks.append(check)
        else:
            checks.append(check)

    return checks


def validate_check(check_name: str = None) -> dict:
    """
    This function prepares and parses checks.

    Args:
        check_name: the name of a check based on file name

    Returns:
        check: a dictionary of a check
    """
    # find required checks based on inputs
    if check_name:
        check = helpers.open_yaml_file(file=f"{dir_path}/show_tech_checks/{check_name}.yaml")
        enabled = check.get("enabled")
        prompt_warning = check.get("prompt_warning")
        if not enabled:
            prompt = f"{prompt_warning}. Are you sure you want to override?"
            confirm_override = click.confirm(prompt, default=False, abort=True, prompt_suffix=": ")
            if not confirm_override:
                print("Aborted.")
                sys.exit()

    return check


def override_entry_point_options(checks: list = None, entry_point_options: dict = None) -> list:
    """
    This function takes entry_point_options provided by main() and overrides the check defaults.

    Args:
        checks: list of checks as provided by main.
        entry_point_options: a json formatted object of options to override the check defaults.

    Returns:
        check
    """
    updated_checks = []
    for check in checks:
        check["entry_point_options"] = entry_point_options
        updated_checks.append(check)
    return updated_checks


###
# Output Choices
###
def output_to_files(path: str = None, return_data: dict = None) -> None:
    """
    This function outputs data to files on the local system.

    Args:
        path: path to place Show Tech outputs
        return_data: output from running Show Tech

    Returns:
        None
    """
    # Note: Storage of the Tech Support files will be in /tmp.
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")  # ISO 8601 similar 2022-11-28T19:31:37
    directory = path + "TechSupport" + date
    helpers.create_dir(directory)
    for check_name, check_response in return_data.items():
        filename = f"{directory}/{check_name}.yaml"
        helpers.build_output_yaml(filename, check_response)

    helpers.zip_directory(directory)
    print(f"show_tech zip file can be located at: {directory}.zip")


def output_to_screen(return_data: str = None) -> None:
    """
    This function runs a show_tech_check using the entry_point defined.

    Args:
        return_data: output from running show_tech we want to print to screen.

    Returns:
        None
    """
    pprint(return_data)


def output_to_api(
    return_data: dict = None,
    api_host: str = None,
    api_organization_id: str = None,
    api_token: str = None,
) -> None:
    """
    This function runs a show_tech_check using the entry_point defined.

    Args:
        return_data: dict = None,
        api_host: str = None,
        api_organization_id: str = None,
        api_token: str = None,

    Returns:
        None
    """
    # TODO: show_tech settings - I'm waffling on this. This works better if nautobot is working and django is working... so maybe not the best way to do this
    PLUGIN_CFG = settings.PLUGINS_CONFIG["nautobot_show_tech"]
    nautobot_cloud_api_organization_id = PLUGIN_CFG["nautobot_cloud_api_organization_id"]
    nautobot_cloud_api_token = PLUGIN_CFG["nautobot_cloud_api_token"]
    nautobot_cloud_api_host = PLUGIN_CFG["nautobot_cloud_api_host"]
    # Setup API configuration
    if api_host is None:
        api_host = os.environ.get("NAUTOBOT_CLOUD_API_HOST")
        if api_host is None:
            api_host = nautobot_cloud_api_host
            if api_host is None:
                api_host = click.prompt("Please provide API host to post show_tech output: ")
    if api_organization_id is None:
        api_organization_id = os.environ.get("NAUTOBOT_CLOUD_API_ORGANIZATION_ID")
        if api_organization_id is None:
            api_organization_id = nautobot_cloud_api_organization_id
            if api_organization_id is None:
                api_organization_id = click.prompt("Please provide API Organization ID to post show_tech output: ")
    if api_token is None:
        api_token = os.environ.get("NAUTOBOT_CLOUD_API_TOKEN")
        if api_token is None:
            api_token = nautobot_cloud_api_token
            if api_token is None:
                api_token = click.prompt("Please provide API token to connect to API Host: ")
    # Prepare to send via API
    if api_host and api_organization_id and api_token:
        url = os.path.join(api_host, f"api/organization/{api_organization_id}/support-diagnostics/")
        # build json data
        hostname = platform.node()
        payload = {
            "name": "Show Tech Output",
            "description": "Nautobot Support Diagnostics",
            "hostname": hostname,
            "config": return_data,
        }
        # send to api
        response = requests.post(url, json=payload, headers={"Authorization": f"Token {api_token}"}, timeout=5)
        response.raise_for_status()


###
# Click inputs and main()
###
@click.command()
@click.option(
    "--api_output",
    is_flag=True,
    help="Enabling output to API requires api_host, api_organization_id, and api_token to be included.",
)
@click.option(
    "--console_output",
    is_flag=True,
    help="Enable console output will return show_tech responses to the CLI screen.",
)
@click.option(
    "--zip_output/--no-zip_output",
    default=True,
    help="This flag is default True to enable a tech support zip file of show_tech check results.",
)
@click.option(
    "--check_name",
    default=None,
    help="This flag runs a single check by name - where {check_name}.yaml is the check name.",
)
@click.option(
    "--zip_output_directory",
    default="/tmp/",
    help="Zip output requires a local directory to be used when creating and zipping files. Directory /tmp/ is used by default and will be erased on host reboot.",
)
@click.option(
    "--entry_point_options",
    default=None,
    help="Add a json payload to control entry_point_options. If added but left empty, you will be prompted per option.",
)
@click.version_option(__version__)
def _main(
    api_output: bool = False,
    console_output: bool = False,
    zip_output: bool = True,
    check_name: str = None,
    zip_output_directory: str = "/tmp/",
    entry_point_options: dict = None,
) -> None:
    """
    By default, this runs enabled checks in show_tech_checks/*.yaml. But can be run in other behaviors based on user inputs.

    Args:
        api_output: bool = False,
        console_output: bool = False,
        zip_output: bool = True,
        check_name: str = None,
        zip_output_directory: str = "/tmp/",
        entry_point_options: dict = {}

    Returns:
        None
    """
    # confirm check_name exists and is valid or grab all enabled checks
    check_list = []
    if check_name:
        check = validate_check(check_name=check_name)
        check_list.append(check)
    else:
        # default behavior is to run all enabled checks
        check_list.extend(retrieve_all_checks(enabled_only=True))

    # confirm zip_output_directory exists on local host and is valid
    if zip_output_directory[-1] != "/":
        zip_output_directory = f"{zip_output_directory}/"
    if zip_output_directory != "/tmp/":
        helpers.create_dir(zip_output_directory)

    # TODO: confirm entry_point_options is valid
    # entry_point_options_check(entry_point_options=entry_point_options)
    # override entry_point_options if provided
    if entry_point_options:
        override_entry_point_options(checks=check_list, entry_point_options=entry_point_options)

    # run the checks and hold it as return_data to be sent to outputs
    return_data = {}
    for check in check_list:
        return_data.update(run_check(check=check))

    # confirm boolean click behavior and output return_data
    if api_output:
        output_to_api(return_data=return_data)

    if console_output:
        output_to_screen(return_data=return_data)

    if zip_output:
        output_to_files(path=zip_output_directory, return_data=return_data)


if __name__ == "__main__":
    _main()
