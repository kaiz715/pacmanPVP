import socket, pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(4096))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)