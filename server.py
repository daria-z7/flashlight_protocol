import json
from websocket import create_connection


ws = create_connection("ws://127.0.0.1:9999/ws")

ws.send(json.dumps({"command":"COLOR", "metadata":"red"}))
result =  ws.recv()
print("Received '%s'" % result)
ws.close()
