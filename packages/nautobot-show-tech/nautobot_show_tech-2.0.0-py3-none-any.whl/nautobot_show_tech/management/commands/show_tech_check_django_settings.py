"""Management command to run show_tech from nautobot."""

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.conf import settings


###
# this management command allows show_tech to pull information from the running Nautobot Instance
# the command and parameters are defined in the nautobot-server commands in show_tech_checks/
###


class Command(BaseCommand):
    """Run show_tech checks against operational Nautobot Instance."""

    help = "Run show_tech checks against Nautobot"

    def handle(self, *args, **kwargs) -> None:
        """Publish command to run show_tech check."""
        try:
            response = {}
            for setting in dir(settings):
                if setting.startswith("__") and setting.endswith("__"):  # Check for dunder aka "magic" method
                    continue
                setting_value = getattr(settings, f"{setting}")
                response[setting] = f"{setting_value}"
            print(response)
        except IntegrityError:
            self.stdout.write(self.style.ERROR("IntegrityError performing checks."))
        except AttributeError:
            self.stdout.write(self.style.ERROR("AttributeError performing checks."))
