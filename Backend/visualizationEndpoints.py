from fastapi import APIRouter, WebSocket
import asyncio
import plotly.express as px

viz_router = APIRouter()




@viz_router.websocket("/viz_socket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await generate_visualizations(websocket)
    await websocket.close()