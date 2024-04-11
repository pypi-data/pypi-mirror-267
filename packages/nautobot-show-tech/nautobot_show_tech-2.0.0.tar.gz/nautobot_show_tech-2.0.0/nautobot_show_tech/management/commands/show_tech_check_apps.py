"""Management command to run show_tech from nautobot."""

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.apps import apps
from django.conf import settings

###
# this management command allows show_tech to pull information about plugins from the running Nautobot Instance
# the command and parameters are defined in the nautobot-server commands in show_tech_checks/
###


class Command(BaseCommand):
    """Run show_tech checks against operational Nautobot Instance."""

    help = "Run show_tech checks against Nautobot"

    def handle(self, *args, **kwargs) -> None:
        """Publish command to run show_tech check."""
        response = {}
        try:
            plugins = [apps.get_app_config(plugin) for plugin in settings.PLUGINS]
            for plugin in plugins:
                response[plugin.name] = plugin.version
            print(response)
        except IntegrityError:
            self.stdout.write(self.style.ERROR("IntegrityError performing checks."))
        except AttributeError:
            self.stdout.write(self.style.ERROR("AttributeError performing checks."))
