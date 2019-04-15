# statsd

[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-statsd/master.svg?label=travis_master)](https://travis-ci.org/Temelio/ansible-role-statsd)
[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-statsd/develop.svg?label=travis_develop)](https://travis-ci.org/Temelio/ansible-role-statsd)
[![Updates](https://pyup.io/repos/github/Temelio/ansible-role-statsd/shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-statsd/)
[![Python 3](https://pyup.io/repos/github/Temelio/ansible-role-statsd/python-3-shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-statsd/)
[![Ansible Role](https://img.shields.io/ansible/role/12562.svg)](https://galaxy.ansible.com/Temelio/statsd/)

Install statsd package.

## Requirements

This role requires Ansible 2.2, 2.3 or 2.4
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- Ubuntu Trusty
- Ubuntu Xenial
- Ubuntu Bionic
- Debian Jessie
- Debian Stretch

and use:
- Ansible 2.4.x
- Ansible 2.5.x
- Ansible 2.6.x

### Running tests

#### Using Docker driver

```
$ tox
```
## Role Variables

### Default role variables

``` yaml
# Defaults vars file for statsd role

# Dependencies management
statsd_use_ansible_galaxy_dependencies: True  # Use role dependencies in meta

# Repository & package management
# -----------------------------------------------------------------------------
statsd_prerequisites_packages: "{{ _statsd_prerequisites_packages }}"
statsd_repository_cache_valid_time: 3600
statsd_repository_update_cache: True


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


# Service management
# -----------------------------------------------------------------------------
statsd_log_storage: 'persistent'
statsd_log_compress: 'yes'


# Statsd systemd services specific settings
is_systemd_managed_system: "{{ _is_systemd_managed_system | default(False) }}"
systemd_service_name: 'systemd'
service_systemd_conf_files:
  journal:
    name: 'journald.conf.j2'
    dest: '/etc/systemd/journald.conf'
    mode: '0644'
    owner: 'root'
    group: 'root'
statsd_service_systemd:
  - dest: '/etc/systemd/system/statsd.service'
    options:
      Unit:
        Description: 'Network daemon for aggregating statistics'
        Wants: 'network.target'
      Service:
        Type: 'simple'
        User: "{{ statsd_user.name }}"
        PIDFile: "{{ statsd_paths.files.pid.path }}"
        ExecStart: "{{ statsd_nodejs_binary }} {{statsd_paths.files.service.path}} {{ statsd_paths.files.main_config.path }}"
        Restart: 'on-failure'
        RestartSec: '10s'
      Install:
        WantedBy: 'multi-user.target'

# Statsd initd specific settings
is_initd_managed_system: "{{ _is_initd_managed_system | default(False) }}"
statsd_service_initd:
  - src: "{{ role_path }}/templates/init.d.j2"
    dest: '/etc/init.d/statsd'

statsd_service_states:
  - name: 'statsd'
    enabled: True
    state: 'started'


# Path management
# -----------------------------------------------------------------------------
statsd_paths:
  dirs:
    config:
      path: '/etc/statsd'
    log:
      path: [ ]
    pid:
      path: '/var/run/statsd'
    root:
      path: "{{ statsd_user.home }}"
    service:
      path: '/etc/systemd/system'
  files:
    main_config:
      path: '/etc/statsd/config.js'
      owner: "{{ statsd_user.name }}"
      group: "{{ statsd_group.name }}"
      mode: '0750'
    lock:
      path: [ ]
    log:
      path: [ ]
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
```

## Dependencies

> You can disable role dependencies using *statsd_use_ansible_galaxy_dependencies* and setting *False*

* [geerlingguy.nodejs](https://github.com/geerlingguy/ansible-role-nodejs/)
and nodejs version 6.x or 8.x

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: geerlingguy.nodejs }
    - { role: Temelio.statsd }
```

## License

MIT

## Author Information

Alexandre Chaussier, update by Lise Machetel (for Temelio company)
- http://www.temelio.com
