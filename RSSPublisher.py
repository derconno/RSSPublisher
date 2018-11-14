import time

import RSSServer

server = RSSServer.RSSServer()

print('Server started on default port')
server.start_server()

print('sleeping for 120 sec')
time.sleep(120)

print('stopping server')
server.stop_server()
