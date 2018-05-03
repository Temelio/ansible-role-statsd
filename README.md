# statsd

[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-statsd/master.svg?label=travis_master)](https://travis-ci.org/Temelio/ansible-role-statsd)
[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-statsd/develop.svg?label=travis_develop)](https://travis-ci.org/Temelio/ansible-role-statsd)
[![Updates](https://pyup.io/repos/github/Temelio/ansible-role-statsd/shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-statsd/)
[![Python 3](https://pyup.io/repos/github/Temelio/ansible-role-statsd/python-3-shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-statsd/)
[![Ansible Role](https://img.shields.io/ansible/role/12562.svg)](https://galaxy.ansible.com/Temelio/statsd/)

Install statsd package with SystemD, and ssmtp for email alert on failure.

## Requirements

This role requires Ansible 2.2 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- Ubuntu Xenial
- Debian Jessie
- Debian Stretch

and use:
- Ansible 2.2.x
- Ansible 2.3.x
- Ansible 2.4.x

### Running tests

#### Using Docker driver

```
$ tox
```
## Role Variables

### Default role variables

``` yaml
# Repository & package management
# -----------------------------------------------------------------------------
statsd_prerequisites_packages: "{{ _statsd_prerequisites_packages }}"
statsd_prerequisites_packages_stretch: "{{ _statsd_prerequisites_packages_stretch }}"
statsd_repository_cache_valid_time: 3600
statsd_repository_update_cache: 'True'


# Statsd user and group
# -----------------------------------------------------------------------------
statsd_user:
  name: 'statsd'
  shell: '/usr/sbin/nologin'
  home: '/var/lib/statsd'
  create_home: 'False'

statsd_group:
  name: "{{ statsd_user.name }}"

# Installation management
statsd_install_method: 'git'
statsd_version: 'v0.8.0'
statsd_nodejs_binary: '/usr/bin/nodejs'

nodejs_prerequisites_packages_stretch: "{{ _nodejs_prerequisites_packages_stretch }}"


# Service management
# -----------------------------------------------------------------------------
statsd_service_description: 'StatsD Service'
statsd_service_name: 'statsd'
statsd_service_enabled: 'True'
statsd_service_state: 'started'
statsd_log_storage: 'persistent'
statsd_log_compress: 'yes'

systemd_service_name: 'systemd'

# Statsd systemd services specific settings
is_systemd_managed_system: "{{ _is_systemd_managed_system | default(False) }}"
statsd_service_systemd:
  dest: '/etc/systemd/system/statsd.service'
  handler: 'Restart statsd'
  options:
    Install:
      WantedBy: 'multi-user.target'
    Restart: 'on_failure'
    Service:
      Group: "{{ statsd_group.name }}"
      PrivateTmp: 'true'
      Restart: 'on-failure'
      RestartSec: '10s'
      Type: 'simple'
      User: "{{ statsd_user.name }}"
    Unit:
      After: ''
      Description: 'Network daemon for aggregating statistics'
      Wants: 'network.target'

# Path management
# -----------------------------------------------------------------------------
statsd_paths:
  dirs:
    config:
      path: '/etc/statsd'
    root:
      path: "{{ statsd_user.home }}"
    pid:
      path: '/var/run/statsd'
    service:
      path: '/etc/systemd/system'
  files:
    main_config:
      path: '/etc/statsd/config.js'
      owner: "{{ statsd_user.name }}"
      group: "{{ statsd_group.name }}"
      mode: '0750'
    pid:
      path: '/var/run/statsd/statsd.pid'
    service:
      path: '/var/lib/statsd/stats.js'
statsd_config_mode: '0750'


# Statsd options
# -----------------------------------------------------------------------------

# Statsd git options
statsd_git:
  repository_url: 'https://github.com/etsy/statsd.git'
  dest_folder: "{{ statsd_user.home }}"
  bare: 'False'
  clone: 'True'
  force: 'True'
  do_update: 'False'

# NPM options
statsd_npm:
  global: 'False'
  path: "{{ statsd_user.home }}"
  production: 'True'
  state: 'present'

# Statsd configuration
statsd_config:
  port: 8125
  backends:
    - './backends/console'
  debug: 'False'
  address: '127.0.0.1'
  mgmt_address: '127.0.0.1'
  mgmt_port: 8126
  title: 'statsd'
  healthStatus: 'up'
  dumpMessages: 'False'
  deleteIdleStats: 'False'
  prefixStats: 'statsd'

# Ssmtp config and path
# -----------------------------------------------------------------------------

ssmtp_root_recipient: 'toto@example.com'
ssmtp_mailhub: 'mail.example.com:587'
ssmtp_from_line_oeverride: 'YES'
ssmtp_use_STARTTLS: 'YES'
ssmtp_authUser: 'toto@example.com'
ssmtp_authPass: 'change me'
ssmtp_fromEmail: 'admin@example.com'
ssmtp_toEmail: 'titi@example.com'

ssmtp_paths:
  files:
    main_config:
      path: '/etc/ssmtp/ssmtp.conf'
      owner: 'root'
      group: 'mail'
      mode: '0640'

revaliases_paths:
  files:
    main_config:
      path: '/etc/ssmtp/revaliases'


# Notify user and group
# -----------------------------------------------------------------------------
notify_systemd_unit_description: 'status email for %i to user'
notify_systemd_unit_after: 'network.target'
notify_systemd_type: 'oneshot'
notify_systemd_execstart: '/usr/local/bin/systemd-email {{ ssmtp_toEmail }} %i'
notify_systemd_restartsec: '600'
notify_user: 'nobody'
notify_group: 'systemd-journal'
notify_service_state: 'started'
notify_service_enabled: 'True'
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: Temelio.statsd }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Temelio company)
- http://www.temelio.com
- alexandre.chaussier [at] temelio.com
