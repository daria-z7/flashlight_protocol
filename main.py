from fastapi import FastAPI, WebSocket,  WebSocketDisconnect
import uvicorn
from image import DrawImage


app = FastAPI(
    title="Flashligt_protocol",
    description="Protocol processing commands to flashlight",
    version="0.0.1",
    license_info={
        "name": "BSD-3",
    }
    )

COMMAND_LIST = {
    "ON": 'The flashlight is on',
    "OFF": 'The flashlight is off',
    "COLOR": 'The color is changed to ',
}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            command = data["command"]
            if command and command in COMMAND_LIST:
                if command == 'COLOR':
                    message = f'{COMMAND_LIST[command]}{data["metadata"]}'
                else:
                    message = COMMAND_LIST[command]
                print(message)
                if command == 'ON':
                    image = DrawImage.from_file("flashlight_on.png")
                    image.draw_image()
                await websocket.send_text(message)
            else:
                await websocket.send_text('Wrong command')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Server was stopped")


if __name__ == "__main__":
    uvicorn.run("main:app", port=9999, host="127.0.0.1", reload=True)
