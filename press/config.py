import os.path

from pyramid.config import Configurator


def discover_set(settings, setting_name, env_var, default=None):
    """Discover a setting from environment variables and add it
    to the settings dictionary. A ``default`` value can be supplied
    and used when the environment variable can not be found.

    """
    if env_var in os.environ:
        settings[setting_name] = os.environ[env_var]
    elif default is not None:
        settings.setdefault(setting_name, default)


def configure(settings=None):
    """Configure the Configurator object"""
    if settings is None:
        settings = {}

    # Discover & check settings
    discover_set(settings, 'shared_directory', 'SHARED_DIR')
    assert os.path.exists(settings['shared_directory'])  # required
    # TODO check permissions for write access

    # Create the configuration object
    config = Configurator(settings=settings)
    config.include('.views')

    config.scan()
    return config


__all__ = ('configure',)
