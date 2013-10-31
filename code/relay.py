'''
Created on Jul 24, 2013

@author: ashah
'''
import tornado
from tornado.tcpserver import TCPServer
from tornado.netutil import bind_sockets
from tornado.ioloop import IOLoop
import paramiko


class RelayServer(TCPServer):
    def handle_stream(self,stream,address):
        EchoConnection(stream, address)

class EchoConnection(object):
 
    stream_set = set([])
    ssh_set = dict()
    def __init__(self, stream, address):
        self.stream = stream
        self.address = address
        client = paramiko.client.SSHClient()
        client.connect('localhost',sock=stream.socket)
        
        self.ssh_set[address] = client
        self.stream_set.add(self.stream)
        self.stream.set_close_callback(self._on_close)
        self.stream.read_until('\n', self._on_read_line)
 
    def _on_read_line(self, data):
        client = self.ssh_set.get(self.address)
        for stream in self.stream_set:
            stream.write(data, self._on_write_complete)
     
    def _on_write_complete(self):
        if not self.stream.reading():
            self.stream.read_until('\n', self._on_read_line)
     
    def _on_close(self):
        self.stream_set.remove(self.stream) 

if __name__ == '__main__':
    '''  server = RelayServer()
    sockets = bind_sockets(9999)
    tornado.process.fork_processes(0)
    server.add_sockets(sockets)
    IOLoop.instance().start()
    '''
    server = RelayServer()
    server.listen(8888)
    IOLoop.instance().start()