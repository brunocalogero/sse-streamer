import './App.css';

// import React from 'react';
// import EventStreamComponent from './EventStreamComponent';

import React, { useEffect, useState } from 'react';

interface EventData {
  message: string;
  // Add other fields as needed based on your actual event structure
}


const App = () => {

  const [events, setEvents] = useState<EventData[]>([]);

  useEffect(() => {
    // Create a new EventSource pointing to your server's /events endpoint
    const eventSource = new EventSource('http://localhost:9745/events');


    function handleStream(event: MessageEvent) {
        console.log(event);
        const eventData: EventData = JSON.parse(event.data);
        setEvents((prevEvents) => [...prevEvents, eventData]);
    }

    eventSource.onmessage = e => (handleStream(e));

    eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        // Close the EventSource and attempt to reconnect if needed
        eventSource.close();
    };

    // Cleanup when the component is unmounted
    return () => {
      eventSource.close();
    };
  }, []); // Empty dependency array ensures the effect runs only once

  return (
    <div>
      <h2>Event Stream</h2>
      <ul>
        {events.map((event, index) => (
          <li key={index}>{JSON.stringify(event)}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;

