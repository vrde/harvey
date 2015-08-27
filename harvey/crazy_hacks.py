"""This module loads the monkeypatch from gevent and applies it.

Nothing fancy, but it's useful and more readable to put this in a separate
module and give and explicit name to it.
"""


import gevent.monkey

gevent.monkey.patch_all()

# Re-add sslwrap to Python 2.7.9
# https://github.com/gevent/gevent/issues/477

import inspect
__ssl__ = __import__('ssl')

try:
    _ssl = __ssl__._ssl
except AttributeError:
    _ssl = __ssl__._ssl2


OldSSLSocket = __ssl__.SSLSocket

import pkgutil
import os
_boto_cacerts_package = pkgutil.get_loader('boto.cacerts')
CA_CERTS = os.path.join(_boto_cacerts_package.filename, 'cacerts.txt')


class NewSSLSocket(OldSSLSocket):
    """Fix SSLSocket constructor."""
    def __init__(
        self, sock, keyfile=None, certfile=None, server_side=False,
        cert_reqs=__ssl__.CERT_REQUIRED, ssl_version=2, ca_certs=None,
        do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None,
        server_hostname=None, _context=None
    ):
        OldSSLSocket.__init__(
            self, sock, keyfile=keyfile, certfile=certfile,
            server_side=server_side, cert_reqs=cert_reqs,
            ssl_version=ssl_version, ca_certs=ca_certs,
            do_handshake_on_connect=do_handshake_on_connect,
            suppress_ragged_eofs=suppress_ragged_eofs, ciphers=ciphers
        )


def new_sslwrap(sock, server_side=False, keyfile=None, certfile=None,
                cert_reqs=__ssl__.CERT_NONE,
                ssl_version=__ssl__.PROTOCOL_SSLv23,
                ca_certs=None, ciphers=None):
    context = __ssl__.SSLContext(ssl_version)
    context.verify_mode = cert_reqs or __ssl__.CERT_NONE
    ca_certs = CA_CERTS
    if ca_certs:
        context.load_verify_locations(ca_certs)
    if certfile:
        context.load_cert_chain(certfile, keyfile)
    if ciphers:
        context.set_ciphers(ciphers)

    caller_self = inspect.currentframe().f_back.f_locals['self']
    return context._wrap_socket(sock, server_side=server_side,
                                ssl_sock=caller_self)

if not hasattr(_ssl, 'sslwrap'):
    _ssl.sslwrap = new_sslwrap
    __ssl__.SSLSocket = NewSSLSocket

import socket
__getaddrinfo = socket.getaddrinfo

# kudos to http://stackoverflow.com/a/13214222/597097
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo
