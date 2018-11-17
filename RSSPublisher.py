import RSSServer

server = RSSServer.RSSServer()

try:
    print('Server started on default port')
    server.start_server()
except KeyboardInterrupt:
    print('stopping server')
    server.stop_server()
