"""
Role tests
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user(host):
    """
    Ensure statsd user exists
    """

    user = host.user('statsd')
    assert user.group == 'statsd'
    assert user.home == '/var/lib/statsd'
    assert user.shell == '/usr/sbin/nologin'


@pytest.mark.parametrize('codename,item_type,path,user,group,mode', [
    (['trusty'], 'directory', '/var/log/statsd', 'statsd', 'statsd', 0o700),
    (['trusty'], 'file', '/var/log/statsd/statsd.log', 'root', 'root', 0o644),
    (['trusty'], 'file', '/etc/init.d/statsd.service', 'root', 'root', 0o755),
    (
        ['xenial', 'jessie', 'stretch', 'trusty'], 'directory',
        '/etc/statsd', 'statsd', 'statsd', 0o700
    ),
    (
        ['xenial', 'jessie', 'stretch', 'trusty'], 'file',
        '/etc/statsd/config.js', 'statsd', 'statsd', 0o750
    ),
    (
        ['xenial', 'jessie', 'stretch', 'trusty'], 'directory',
        '/var/lib/statsd', 'statsd', 'statsd', 0o700
    ),
    (
        ['xenial', 'jessie', 'stretch'], 'file',
        '/etc/systemd/system/statsd.service', 'root', 'root', 0o644
    ),
])
def test_paths_properties(host, codename, item_type, path, user, group, mode):
    """
    Test statsd folders and files properties
    """

    current_item = host.file(path)

    if host.system_info.distribution not in codename:
        pytest.skip('{} ({}) distribution not managed'.format(
            host.system_info.distribution, host.system_info.release))
    if item_type == 'directory':
        assert current_item.is_directory
    elif item_type == 'file':
        assert current_item.is_file

    assert current_item.exists
    assert current_item.user == user
    assert current_item.group == group
    assert current_item.mode == mode


def test_service(host):
    if host.system_info.codename == 'trusty':
        """
        Test statsd service for trusty
        """
        service = host.service('statsd')

        assert service.is_enabled

        assert service.is_running
    else:
        """
        Test statsd service for jessie, stretch, xenial
        """

        service = host.service('statsd')

        assert service.is_enabled

        assert 'running' in \
            host.check_output('service statsd status')


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
