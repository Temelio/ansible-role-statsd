"""
Role tests
"""
import pytest

# To run all the tests on given docker images:
pytestmark = pytest.mark.docker_images(
    'infopen/ubuntu-trusty-ssh:0.1.0',
    'infopen/ubuntu-xenial-ssh-py27:0.2.0'
)


def test_user(User):
    """
    Test statsd user
    """

    user = User('statsd')
    assert user.group == 'statsd'
    assert user.home == '/var/lib/statsd'
    assert user.shell == '/usr/sbin/nologin'


def test_folders(File):
    """
    Test statsd folders exists
    """

    folders = [
        '/etc/statsd',
        '/var/lib/statsd',
        '/var/log/statsd',
    ]

    for current_folder in folders:
        folder = File(current_folder)
        assert folder.exists
        assert folder.is_directory
        assert folder.user == 'statsd'
        assert folder.group == 'statsd'


def test_config_file(File):
    """
    Test statsd configuration file exists
    """

    config_file = File('/etc/statsd/config.js')

    assert config_file.exists
    assert config_file.is_file
    assert config_file.user == 'statsd'
    assert config_file.group == 'statsd'
    assert config_file.mode == 0o400


def test_init_file(File):
    """
    Test statsd init file exists
    """

    init_file = File('/etc/init.d/statsd')

    assert init_file.exists
    assert init_file.is_file
    assert init_file.user == 'statsd'
    assert init_file.group == 'statsd'
    assert init_file.mode == 0o500


def test_service(Service):
    """
    Test statsd service
    """

    service = Service('statsd')

    assert service.is_enabled
    assert service.is_running


def test_process(Process):
    """
    Test statsd process
    """

    assert len(Process.filter(user='statsd', comm='statsd')) == 1


def test_sockets(Socket):
    """
    Test all statsd sockets
    """

    sockets = [
        'tcp://127.0.0.1:8126',
        'udp://127.0.0.1:8125',
    ]

    for socket in sockets:
        assert Socket(socket).is_listening
