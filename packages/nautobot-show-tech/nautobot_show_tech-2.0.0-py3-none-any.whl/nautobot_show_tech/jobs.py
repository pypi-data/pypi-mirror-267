"""Jobs to run Nautobot Show Tech for support diagnostics."""

import os

from nautobot.apps.jobs import BooleanVar, ChoiceVar, Job, StringVar, register_jobs

from nautobot_show_tech.run_check import output_to_api, validate_check, retrieve_all_checks, run_check


class show_tech_run_check(Job):
    """Nautobot job class for Show Tech."""

    class Meta:
        """Show Tech job metadata."""

        name = "Show Tech: Run check by name"
        description = "Provides Nautobot os.environment diagnostics. Similar to a 'show tech' output."
        time_limit = 300
        soft_time_limit = 60

    all_checks = retrieve_all_checks(enabled_only=True)
    check_choices = [(check["name"], check["name"]) for check in all_checks]

    check_name = ChoiceVar(choices=check_choices, label="Select Show Tech check to run", required=True)

    def run(self, check_name):
        """Run nautobot_show_tech --check_name {{check_name}}."""
        self.logger.info("Running Show Tech via Nautobot Job.")

        # prepare the checks to run
        check_list = []
        check = validate_check(check_name=check_name)
        check_list.append(check)

        # run the checks
        return_data = {}
        for check in check_list:
            check_name = check.get("name")
            self.logger.info(f"Running check: {check_name}")
            check_result = run_check(check=check)
            check_name_result = check_result.get(check_name)
            only_result = check_name_result.get("command_result")
            self.logger.info(f"Result: {only_result}")
            return_data.update(check_result)

        self.logger.info("Show Tech has completed diagnostics!")


class show_tech_run_checks_and_upload(Job):
    """Nautobot job class for Show Tech."""

    class Meta:
        """Show Tech job metadata."""

        name = "Show Tech: Run checks and upload to API"
        description = "Provides Nautobot os.environment diagnostics. Similar to a 'show tech' output."
        time_limit = 300
        soft_time_limit = 60

    # TODO: this looks messy in the GUI. Maybe we can clean it up a bit? Curretly functions at least.
    api_submit = BooleanVar(
        label="Submit Show Tech results to Nautobot Cloud Console API", default=True, required=False
    )
    api_host = StringVar(label="Nautobot Cloud Console host", default="https://nautobot.cloud", required=False)
    api_organization_id = StringVar(
        label="Nautobot Cloud Console Organization",
        default=os.environ.get("SHOW_TECH_NCLOUD_ORGANIZATION_ID"),
        required=False,
    )
    api_token = StringVar(
        label="Nautobot Cloud Console API token", default=os.environ.get("SHOW_TECH_NCLOUD_TOKEN"), required=False
    )
    enabled_only = BooleanVar(label="Enabled Show Tech checks only", default=True, required=False)

    def run(self, api_submit, api_host, api_organization_id, api_token, enabled_only):
        """Run Show Tech job."""
        self.logger.info("Running Show Tech via Nautobot Job.")
        self.logger.info(f"Submit to API: {api_submit}")

        # prepare the checks to run
        check_list = []
        check_list.extend(retrieve_all_checks(enabled_only=enabled_only))

        # run the checks
        return_data = {}
        for check in check_list:
            check_name = check.get("name")
            self.logger.info(f"Running check: {check_name}")
            check_result = run_check(check=check)
            check_name_result = check_result.get(check_name)
            only_result = check_name_result.get("command_result")
            self.logger.info(f"Result: {only_result}")
            return_data.update(check_result)

        # Currently we request these via click if not present, that won't work in a GUI. Let's make sure these are set or we error for now.
        if api_submit:
            # confirm api key,values required for submitting exist
            if all(v is not None for v in [api_host, api_organization_id, api_token]):
                self.logger.info(
                    f"api host: {api_host}, api org id: {api_organization_id}, and api token: [redacted], will be used."
                )
            else:
                self.logger.critical(
                    "Host, Organization, or Token were missing. Cannot submit results to Nautobot Cloud Console"
                )

            # output the checks
            output_to_api(
                return_data=return_data, api_host=api_host, api_organization_id=api_organization_id, api_token=api_token
            )

        self.logger.info("Show Tech has completed diagnostics!")


register_jobs(show_tech_run_check, show_tech_run_checks_and_upload)
