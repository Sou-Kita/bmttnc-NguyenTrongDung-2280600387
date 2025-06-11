# server.py
import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        WebSocketServer.clients.add(self)
        print(f"New client connected. Total clients: {len(self.clients)}")

    def on_close(self):
        WebSocketServer.clients.remove(self)
        print(f"Client disconnected. Remaining clients: {len(self.clients)}")

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message '{message}' to {len(cls.clients)} client(s).")
        for client in cls.clients:
            client.write_message(message)

class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list
    
    def sample(self):
        return random.choice(self.word_list)

def main():
    app = tornado.web.Application(
        [("/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)

    io_loop = tornado.ioloop.IOLoop.current()

    word_selector = RandomWordSelector(['apple', 'banana', 'orange', 'grape', 'melon'])

    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()),
        2000  # Send message every 2000ms (2 seconds)
    )
    periodic_callback.start()

    print("WebSocket server started on port 8888")
    io_loop.start()

if __name__ == "__main__":
    main()