import asyncio
import nats
import json
from datetime import datetime
import random


async def publish_telemetry():
    # Connect to the NATS server
    nc = await nats.connect("nats://localhost:4222")
    vehicle_ids = [f"TRUCK-{i}" for i in range(1, 6)]  # Simulate 5 trucks 

    while True:
        # Generate random telemetry data
        telemetry = {
            "vehicle_id": random.choice(vehicle_ids),
            "timestamp": datetime.utcnow().isoformat(),
            "lat": random.uniform(34.0, 35.0),
            "lon": random.uniform(-118.0, -117.0),
            "engine_temp": random.randint(70, 120),  # Critical if >100
            "fuel_level": random.randint(10, 100),   # Critical if <20
            "brake_health": random.randint(50, 100)  # Critical if <60
        }
        # Publish telemetry data as JSON
        await nc.publish("fleet.telemetry", json.dumps(telemetry).encode())
        await asyncio.sleep(1)

# Run the asynchronous function
asyncio.run(publish_telemetry())