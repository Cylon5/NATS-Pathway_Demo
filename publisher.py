import asyncio
import nats
import json
from datetime import datetime
import random


async def publish_telemetry():
    # Connect to the NATS server
    nc = await nats.connect("nats://localhost:4222")
    turbine_ids = [f"TURBINE-{i}" for i in range(1, 6)]  # Simulate 5 turbines

    while True:
        # Generate random telemetry data
        telemetry = {
            "turbine_id": random.choice(turbine_ids),
            "timestamp": datetime.utcnow().isoformat(),
            "blade_length": random.uniform(50.0, 80.0),
            "blade_width": random.uniform(3.0, 5.0),
            "vibration": random.randint(20, 100),  # Critical if > 80
            "temperature": random.randint(60, 120),   # Critical if > 100
        }
        # Print the telemetry data
        print(f"Publishing: {telemetry}")
        
        # Publish telemetry data as JSON
        await nc.publish("turbine.telemetry", json.dumps(telemetry).encode())
        await asyncio.sleep(1)

# Run the asynchronous function
asyncio.run(publish_telemetry())