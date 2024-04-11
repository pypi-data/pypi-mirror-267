"""Management command to run show_tech from nautobot."""

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import nautobot.dcim.models as models_dcim
import nautobot.ipam.models as model_ipam
from django.utils import timezone

###
# this management command allows show_tech to pull information from the running Nautobot Instance
# the command and parameters are defined in the nautobot-server commands in show_tech_checks/
###


class Command(BaseCommand):
    """Run show_tech checks against operational Nautobot Instance."""

    help = "Run show_tech checks against Nautobot"

    def handle(self, *args, **kwargs) -> None:
        """Publish command to run show_tech check."""
        response = {}
        current_datetime = timezone.now()
        last_24h_datetime = current_datetime - timezone.timedelta(hours=24)
        try:
            models = [models_dcim, model_ipam]
            for model in models:
                for item in dir(model):
                    if item.startswith("__") and item.endswith("__"):  # Check for dunder aka "magic" method
                        continue
                    model_attr = getattr(model, item)
                    if "objects" in dir(model_attr) and model_attr._meta.app_label in ("dcim", "ipam"):
                        field_names = [field.name for field in model_attr._meta.get_fields()]
                        if "created" and "last_updated" not in field_names:
                            continue
                        response[".".join([model_attr._meta.app_label, model_attr.__name__])] = {
                            "total": model_attr.objects.count(),
                            "created_last_day": model_attr.objects.filter(created__gt=last_24h_datetime).count(),
                            "updated_last_day": model_attr.objects.filter(last_updated__gt=last_24h_datetime).count(),
                        }

            print(response)
        except IntegrityError:
            self.stdout.write(self.style.ERROR("IntegrityError performing checks."))
        except AttributeError:
            self.stdout.write(self.style.ERROR("AttributeError performing checks."))
