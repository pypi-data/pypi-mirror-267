"""This provides functions which aid in the running of this app and are usable across my actions/checks."""

import shutil
import os
import yaml


def build_output_yaml(file: str, data: dict) -> None:
    """
    This function outputs yaml files given the filename and the data in dictionary format to populate the file.

    Args:
        file:  This is the name of the file to be created.
        data:  This is the python dicitonary, json formated data, to be dumped to the file.

    Returns:
        None

    Raises:
        Try/Except used to catch errors when dumping data to yaml file.
    """
    try:
        with open(file, "w", encoding="utf-8") as text:
            yaml.safe_dump(data, text)
    except Exception as e:
        print(f"build_output_yaml: {e}")


def build_output_txt(file: str, string: str) -> None:
    """
    This function outputs a file given the filename and a string to populate the file.

    Args:
        file:  This is the name of the file to be created.
        string:  This is the data to be written to the file.

    Returns:
        None

    Raises:
        Try/Except used to catch errors when writing string file.
    """
    try:
        with open(file, "w", encoding="utf-8") as text:
            text.write(string)
    except Exception as e:
        print(f"build_output_txt: {e}")


def create_dir(directory: str) -> None:
    """
    This function checks if a directory exists and if not, creates it.

    Args:
        directory:  This is the directory to be created if it does not exist.

    Returns:
        None

    Raises:
        None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def zip_directory(directory: str) -> None:
    """
    This function takes a directory and zips it together.

    Args:
        directory:  This is the directory in which we want to create a zip file from.

    Returns:
        None

    Raises:
        None
    """
    # make_archive - https://docs.python.org/3.7/library/shutil.html#shutil.make_archive
    shutil.make_archive(f"{directory}", "zip", directory)


def open_yaml_file(file: str) -> dict:
    """
    This function opens a yaml file and returns as a dictionary.

    Args:
        file:  This is the yaml file to be opened and loaded as a python dictionary.

    Returns:
        A python dictionary of data from the opened file.

    Raises:
        Try/Except used to capture issues with opening the file or loading the yaml into a python dictionary.
    """
    data = None
    try:
        with open(file, "r", encoding="utf-8") as text:
            data = yaml.load(text, Loader=yaml.SafeLoader)
    except Exception as e:
        print(f"error with open_yaml_file: {e}")
    if not data:
        print(f"File: {file} may not exist or did not have any content.")
    return data
