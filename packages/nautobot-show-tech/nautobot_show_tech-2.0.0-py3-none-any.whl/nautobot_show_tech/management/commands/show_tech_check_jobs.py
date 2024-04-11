"""Management command to run show_tech from nautobot."""

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils import timezone
from nautobot.extras.models import Job
from nautobot.extras.choices import JobResultStatusChoices

###
# this management command allows show_tech to pull information about jobs from the running Nautobot Instance
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
            jobs = Job.objects.prefetch_related("results", "scheduled_jobs").all()
            for job in jobs:
                if job.get("scheduled_jobs"):
                    jobs_executed_in_last_24h = job.scheduled_jobs.filter(start_time__gt=last_24h_datetime).count()
                if job.get("results"):
                    jobs_errored_in_last_24h = job.results.filter(
                        completed__gt=last_24h_datetime, status=JobResultStatusChoices.STATUS_FAILED
                    ).count()
                response[job.name] = {
                    "enabled": job.enabled,
                    "is_job_hook": job.is_job_hook_receiver,
                    "is_job_button": job.is_job_button_receiver,
                    "is_scheduled": True if job.scheduled_jobs else False,
                    "last_run": (
                        timezone.localtime(job.latest_result.created).strftime("%Y-%m-%d %H:%M:%S %Z")
                        if job.latest_result
                        else None
                    ),
                    "last_run_status": job.latest_result.status if job.latest_result else None,
                    "number_of_runs_last_day": jobs_executed_in_last_24h,
                    "number_of_failed_runs_last_day": jobs_errored_in_last_24h,
                }
            print(response)
        except IntegrityError:
            self.stdout.write(self.style.ERROR("IntegrityError performing checks."))
        except AttributeError:
            self.stdout.write(self.style.ERROR("AttributeError performing checks."))
