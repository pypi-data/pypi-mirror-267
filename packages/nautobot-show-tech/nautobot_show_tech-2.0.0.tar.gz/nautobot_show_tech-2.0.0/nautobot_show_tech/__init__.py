"""App declaration for nautobot_show_tech."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotShowTechConfig(NautobotAppConfig):
    """App configuration for the nautobot_show_tech app."""

    name = "nautobot_show_tech"
    verbose_name = "Nautobot Show Tech"
    version = __version__
    author = "Network to Code, LLC"
    description = "An app to aid in troubleshooting a Nautobot environment.."
    base_url = "show-tech"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {
        "nautobot_cloud_api_host": "https://nautobot.cloud",
        "nautobot_cloud_api_organization_id": "",
        "nautobot_cloud_api_token": "",
    }
    caching_config = {}


config = NautobotShowTechConfig  # pylint:disable=invalid-name
