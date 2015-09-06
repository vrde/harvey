"""This module loads the monkeypatch from gevent and applies it.

Nothing fancy, but it's useful and more readable to put this in a separate
module and give and explicit name to it.
"""




# Re-add sslwrap to Python 2.7.9
# import socket
# __getaddrinfo = socket.getaddrinfo
# 
# # kudos to http://stackoverflow.com/a/13214222/597097
# def getaddrinfo(*args):
#     return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
# 
# socket.getaddrinfo = getaddrinfo
