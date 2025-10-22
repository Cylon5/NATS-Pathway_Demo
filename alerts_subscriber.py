import asyncio
import nats
import json 

async def receive_alerts():
    nc = await nats.connect("nats://localhost:4222") 

    async def alert_handler(msg):
        alert = json.loads(msg.data.decode())
        print(f"ALERT: Turbine {alert['turbine_id']} - {alert['alert_type']} at {alert['timestamp']}")

    await nc.subscribe("turbine.alerts", cb=alert_handler)
    print("Subscribed to 'turbine.alerts' subject.")

    while True:
        await asyncio.sleep(1)
		
asyncio.run(receive_alerts())