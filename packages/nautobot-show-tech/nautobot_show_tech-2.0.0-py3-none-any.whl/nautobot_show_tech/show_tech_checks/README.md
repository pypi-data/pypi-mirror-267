# Description
This file contains information about the checks show_tech performs and should be used as reference for what this app can do.  Alternatively, you can use the commandline `show_tech --help`.

# How to Read each YAML file
* **Name:** name of the command to be run
* **Description:** a short description of the command to be run and any considerations about that command
* **Linux command:** exact command to be run against a Linux host
* **Enabled:** do we want to run the command or turn it off

# Current Commands
## pip_--version
* **Linux command:** pip --version
* **Description:** Returns pip --version about pip
* **Enabled:** True

## lscpu
* **Linux command:** lscpu
* **Description:** Returns CPU architecture information from sysfs, /proc/cpuinfo and any applicable architecture-specific libraries
* **Enabled:** True

## nautobot-server_health_check
* **Linux command:** nautobot-server health_check
* **Description:** Returns nautobot-server health_check from the nautobot instance
* **Enabled:** True

## disk_space
* **Linux command:** df -lhT
* **Description:** Returns utilization information of local disk space about the host in human-readable format
* **Enabled:** True

## nautobot-server_version
* **Linux command:** nautobot-server --version
* **Description:** Returns nautobot-server --version from the nautobot instance
* **Enabled:** True

## date
* **Linux command:** date
* **Description:** Returns date from the host.
* **Enabled:** True

## nautobot-server_django_settings
* **Linux command:** nautobot-server show_tech_check_django_settings
* **Description:** Returns show_tech management command from running nautobot
* **Enabled:** True

## whoami
* **Linux command:** whoami
* **Description:** Returns whoami from the host
* **Enabled:** True

## nautobot-server_counts
* **Linux command:** nautobot-server show_tech_check_counts
* **Description:** Returns object counts from running nautobot
* **Enabled:** True

## pip_freeze
* **Linux command:** pip freeze
* **Description:** Returns pip list as requirements.txt
* **Enabled:** True

## dns
* **Linux command:** grep nameserver /etc/resolv.conf | sed 's/nameserver //'
* **Description:** Returns domain nameserer from the host.
* **Enabled:** True

## ansible_--versio
* **Linux command:** ansible --version
* **Description:** Returns ansible --version on host system
* **Enabled:** False

## python_--version
* **Linux command:** python --version
* **Description:** Returns python --version about python
* **Enabled:** True

## which_python
* **Linux command:** which python
* **Description:** Returns which python about python
* **Enabled:** True

## which_pip
* **Linux command:** which pip
* **Description:** Returns which pip about pip
* **Enabled:** True

## available_commands
* **Linux command:** compgen -c
* **Description:** Returns list of commands available to the user from the host
* **Enabled:** False

## hostname
* **Linux command:** hostname
* **Description:** Returns hostname from the host
* **Enabled:** True

## uname_-a
* **Linux command:** uname -a
* **Description:** Returns the name of the operating system implementation. -a includes the following flags -m, -n, -r, -s, -v
* **Enabled:** True

## pwd
* **Linux command:** pwd
* **Description:** Returns the working directory starting from root. currently disabled for host_details.yaml
* **Enabled:** True

## os-release
* **Linux command:** cat /etc/os-release
* **Description:** Returns os-release information about the host
* **Enabled:** True

## host_uptime
* **Linux command:** cat /proc/uptime | awk '{print int($1/86400)"d:"int($1/3600)"h:"int(($1%3600)/60)"m:"int($1%60)"s"}'
* **Description:** Proceses /proc/uptime and converts to day,hour,min,sec
* **Enabled:** True

## nautobot-server_apps
* **Linux command:** nautobot-server show_tech_check_apps
* **Description:** Returns information about jobs from running nautobot
* **Enabled:** True

## nautobot-server_jobs
* **Linux command:** nautobot-server show_tech_check_jobs
* **Description:** Returns information about jobs from running nautobot
* **Enabled:** True

## alias
* **Linux command:** alias
* **Description:** Returns list of alias for this user on host. This is not a default command on all operating systems.
* **Enabled:** False

## meminfo
* **Linux command:** cat /proc/meminfo | grep -oEi 'Mem[TF].+'
* **Description:** Returns memory information about the host
* **Enabled:** True
