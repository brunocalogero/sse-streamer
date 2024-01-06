# sse-streamer

## Requirements

1. Docker
2. A modern-ish version of Node

To ensure things will work, please run these two commands:

./build.sh
./start.sh

## Use

The app is configured to listen to the `/events` endpoint. This endpoint is event based. It listens to a queue, when the queue is poulated it sends an event over to the frontend, this event is then displayed.

To add events to the queue one can run the following after running the app:
`curl -X POST -H "Content-Type: application/json" -d '{"message": "your message here"}'`

## Extra

One can play with other endpoint provided to test SSE in the client.
