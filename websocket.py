import threading
import websockets
import asyncio

output_websocket = ''

class WebSocket:

    def __init__(self, ip, port):
        self.websocket_thread = threading.Thread(target=self.threadStartWebsocketServer, daemon=True)
        self.message = None
        self.ip = ip
        self.port = port

    def startWebSocket(self):
        self.websocket_thread.start()

    def getOutputMessage(self):
        return self.message

    async def handleWebsocketConnection(self, websocket, path):
        # Handle the WebSocket connection
        print("Client connecting from:", websocket.remote_address)
        try:
            async for message in websocket:
                self.message = message
        except Exception as e:
            print("Error:", e)
        finally:
            print("Connection closed.")

    def threadStartWebsocketServer(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(self.handleWebsocketConnection, self.ip, self.port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


web_socket = WebSocket('0.0.0.0', 5000)

web_socket.startWebSocket()

while True:
    if web_socket.getOutputMessage() is not None:
        print(web_socket.getOutputMessage())