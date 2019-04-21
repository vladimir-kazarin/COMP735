import socketserver
import http

CLRF = '\r\n'

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        try:
            self.data = self.request.recv(1024).strip()
        except:
            self.request.send(bytes('HTTP/1.1 400 Bad Request' + CLRF, 'utf-8'))
            self.request.send(bytes('Content-Type: text/html' + CLRF*2, 'utf-8'))
            self.request.send(bytes('<h1>Invalid Request: </h1>', 'utf-8'))
    
        print("Request from {}".format(self.client_address[0]))
        # just send back the same data, but upper-cased
        self.request.send(bytes(self.client_address[0] + CLRF, 'utf-8'))
        self.request.send(bytes('HTTP/1.1 200 OK Request' + CLRF, 'utf-8'))
        self.request.send(bytes('Content-Type: text/html' + CLRF*2, 'utf-8'))
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8000

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
