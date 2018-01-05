# statsd

[![Build Status](https://travis-ci.org/Temelio/ansible-role-statsd.svg?branch=master)](https://travis-ci.org/Temelio/ansible-role-statsd)

Install statsd package.

## Requirements

This role requires Ansible 2.2 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- Debian Jessie
- Ubuntu Trusty
- Ubuntu Xenial

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
# Statsd user
statsd_user_name: 'statsd'
statsd_group_name: 'statsd'
statsd_user_shell: '/usr/sbin/nologin'
statsd_user_home: '/var/lib/statsd'
statsd_user_create_home: False

# Installation management
statsd_install_method: 'git'
statsd_version: 'v0.8.0'
statsd_nodejs_binary: '/usr/bin/nodejs'
statsd_prerequisites_packages:
  - 'git'
  - 'nodejs'
  - 'npm'
statsd_prerequisites_state: 'present'
statsd_prerequisites_cache_valid_time: 3600

# Service management
statsd_service_name: 'statsd'
statsd_service_state: 'started'
statsd_service_enabled: True

# Path management
statsd_folders_mode: '0700'
statsd_init_file: '/etc/init.d/statsd'
statsd_init_mode: '0500'
statsd_config_file: '/etc/statsd/config.js'
statsd_config_mode: '0400'
statsd_lock_file: '/var/lock/subsys/statsd'
statsd_log_file: '/var/log/statsd/statsd.log'
statsd_log_error_file: '/var/log/statsd/statsd-err.log'
statsd_pid_file: '/var/run/statsd.pid'

# Statsd git options
statsd_git_repository_url: 'https://github.com/etsy/statsd.git'
statsd_git_dest_folder: "{{ statsd_user_home }}"
statsd_git_option_bare: False
statsd_git_option_clone: True
statsd_git_option_force: True
statsd_git_option_update: False

# NPM options
statsd_npm_option_global: False
statsd_npm_option_path: "{{ statsd_user_home }}"
statsd_npm_option_production: True

# Statsd configuration
statsd_config:
  port: 8125
  backends:
    - './backends/console'
  debug: False
  address: '127.0.0.1'
  mgmt_address: '127.0.0.1'
  mgmt_port: 8126
  title: 'statsd'
  healthStatus: 'up'
  dumpMessages: False
  deleteIdleStats: False
  prefixStats: 'statsd'
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
