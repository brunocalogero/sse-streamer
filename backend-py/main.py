from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pyee import EventEmitter
from loguru import logger
import json
import asyncio
import queue

app = FastAPI()

origins = [
    "http://localhost:9746",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an EventEmitter instance
event_emitter = EventEmitter()

event_queue = queue.Queue()

@event_emitter.on("event")
def add_event(data):
    logger.info(f"Received event: {data}")
    try:
        event_queue.put(data)
    except Exception as e:
        logger.error(f"Error adding event to queue: {e}")


@app.get("/")
async def root():
    logger.info("GET /")
    return "Everything is working - you're ready for the interview!"

# Dummy event stream endpoint
@app.get("/datastream")
async def get_data_stream(response: Response):
    # Set headers to enable server-sent events
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    # Function to generate and send data to the client
    async def data_stream():
        count = 0
        while True:
            # Construct a simple message with a counter
            data = f"Data {count}"

            # Convert the dictionary to a JSON string
            json_data = json.dumps(data)

            # Yield the data as a Server-Sent Event
            yield f"data: {json_data}\n\n"

            # Increment the counter
            count += 1

            # Introduce a delay (simulating real-time data)
            await asyncio.sleep(1)

    # Return StreamingResponse with the generator function
    return StreamingResponse(data_stream(), media_type="text/event-stream")

# Queue event based streamer
@app.get("/events")
async def get_events(request: Request, response: Response):
    # Set headers to enable server-sent events
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    # Generator to send events to the client
    async def event_streamer():
        while True:
            try:
                # If client closed the connection
                if await request.is_disconnected():
                    break

                # Yield the next event from the queue if there are any
                if not event_queue.empty():
                    event_data = event_queue.get()
                    logger.info(f"Sending event: {event_data}")
                    yield f"data: {json.dumps(event_data)}\n\n"
            except Exception as e:
                logger.error(f"Error in event stream: {e}")

    return StreamingResponse(event_streamer(), media_type="text/event-stream")


@app.post("/send_event")
async def send_event(data: dict):
    try:
        # Emit the "event" with the provided data
        event_emitter.emit("event", data)
        return {"status": "Event sent"}
    except Exception as e:
        logger.error(f"Error sending event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
