__author__ = 'mattesnider'

__version__ = (0, 1, 5)

registered_networks = {}


def register_backend(backend):
    """
    Registers a backend with the django social user system.
    """
    if not backend.network:
        raise Exception('network must be defined on custom backend')
    registered_networks[backend.network] = backend()
