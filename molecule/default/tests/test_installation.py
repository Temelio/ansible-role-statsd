"""
Role tests
"""

import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_user(host):
    """
    Test statsd user
    """

    user = host.user('statsd')
    assert user.group == 'statsd'
    assert user.home == '/var/lib/statsd'
    assert user.shell == '/usr/sbin/nologin'


@pytest.mark.parametrize('item_type,path,user,group,mode', [
    ('directory', '/etc/statsd', 'statsd', 'statsd', 0o700),
    ('directory', '/var/lib/statsd', 'statsd', 'statsd', 0o700),
    ('file', '/etc/statsd/config.js', 'statsd', 'statsd', 0o400),
    ('file', '/etc/systemd/system/statsd.service', 'root', 'root', 0o500),
])
def test_paths_properties(host, item_type, path, user, group, mode):
    """
    Test statsd folders and files properties
    """

    current_item = host.file(path)

    if item_type == 'directory':
        assert current_item.is_directory
    elif item_type == 'file':
        assert current_item.is_file

    assert current_item.exists
    assert current_item.user == user
    assert current_item.group == group
    assert current_item.mode == mode


def test_service(host):
    """
    Test statsd service
    """

    service = host.service('statsd')

    assert service.is_enabled

    if host.system_info.codename in ['xenial']:
        assert 'is running' in \
          host.check_output('servicectl status statsd.service')
    else:
        assert service.is_running


def test_process(host):
    """
    Test statsd process
    """

    assert len(host.process.filter(user='statsd', comm='statsd')) == 1


@pytest.mark.parametrize('socket', [
    ('tcp://127.0.0.1:8126'),
    ('udp://127.0.0.1:8125'),
])
def test_sockets(host, socket):
    """
    Test all statsd sockets
    """

    assert host.socket(socket).is_listening
