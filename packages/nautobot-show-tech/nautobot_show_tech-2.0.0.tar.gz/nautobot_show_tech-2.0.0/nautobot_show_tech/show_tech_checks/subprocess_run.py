"""This is an entry_point for checks to be ran against the OS."""

import ast
import re
import shlex
import subprocess


class ResultHandler:
    """ResultHandler holds and builds the return of the check being run."""

    stdout = ""


class Check:
    """Uses python subprocess.run() method as a check against the sub-system."""

    @staticmethod
    def run(check_name: str = None, command: str = None, **kwargs) -> dict:
        """
        This function performs a subprocess to run commands against the host, we can then return the response from the command via raw or yaml formats.

        Args:
            check_name: name of the check
            command: os level command to run
            **kwargs: any other key word arguments
                timeout: subprocess.run(timeout=timeout)
                return_type: format to return command_result

        Returns:
            response: a dictionary of check information
        """
        # process additional key value pairs
        timeout = kwargs.pop("timeout", int(15))

        # due to splitting the command to handle pipe "|" commands, uses ResultHandler to store each piece.
        commands = command.split("|")
        result = ResultHandler

        # build a standardized schema for response data as a json payload, currently on revision v1
        response = {"output_version": "v1"}
        response[check_name] = {
            "entry_point_error": "",
            "command": "",
            "command_result": "",
            "command_result_status": "Failure",
            "command_result_type": "",
            "command_result_error": "",
        }
        try:
            for next_command in commands:
                # https://docs.python.org/3/library/subprocess.html
                result = subprocess.run(
                    shlex.split(next_command.strip()),
                    capture_output=True,
                    text=True,
                    shell=False,
                    check=True,
                    universal_newlines=True,
                    input=result.stdout.strip(),
                    timeout=timeout,
                )
        except Exception as e:
            print(f"subprocess.run error: {e}")
            response[check_name]["entry_point_error"] = f"{e}"
        else:
            unparsed_result = result.stdout.strip()
            response[check_name].update(Check._parse_result(unparsed_result=unparsed_result, **kwargs))
            response[check_name]["command"] = command

            if "" not in result.stderr:
                response[check_name]["command_result_error"] = result.stderr
                response[check_name]["command_result_status"] = "Error"

        return response

    @staticmethod
    def _parse_result(unparsed_result: str = None, **kwargs) -> dict:
        """
        This function parses the result from the run method.

        Args:
            unparsed_result: str = None
            **kwargs:
                return_type

        Returns:
            parsed_result: a dict of result information after being parsed
        """
        # look for possible kwargs, provide defaults if not found
        return_type = kwargs.pop("return_type", str("json"))

        parsed_result = {}
        try:
            # https://docs.python.org/3/library/ast.html#ast.literal_eval
            parsed_result["command_result"] = ast.literal_eval(unparsed_result)
            parsed_result["command_result_type"] = "json"
        except (SyntaxError, ValueError):
            if return_type == "raw":
                parsed_result["command_result_type"] = "raw text"
            # separate newlines into a list
            if "\n" in unparsed_result:
                cleaned_result = re.sub(" +", " ", unparsed_result)
                parsed_result["command_result"] = cleaned_result.split("\n")
                parsed_result["command_result_type"] = "list"
            # replace whitespaces and give the result back
            else:
                parsed_result["command_result"] = re.sub(" +", " ", unparsed_result)
                parsed_result["command_result_type"] = "string"
        if parsed_result["command_result"] is not None:
            parsed_result["command_result_status"] = "Success"
        return parsed_result
