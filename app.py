import pathway as pw

# Define the telemetry schema
class TelemetrySchema(pw.Schema):
   vehicle_id: str
   timestamp: str
   lat: float
   lon: float
   engine_temp: int
   fuel_level: int
   brake_health: int 

# Ingest telemetry data from NATS
telemetry_table = pw.io.nats.read(
   uri="nats://127.0.0.1:4222",
   topic="fleet.telemetry",
   format="json",
   schema=TelemetrySchema
)

# Define a UDF for detecting alerts with if conditions
@pw.udf
def detect_alerts(engine_temp, fuel_level, brake_health):
   alerts = []
   if engine_temp > 100:
       alerts.append("High Engine Temp")
   if fuel_level < 20:
       alerts.append("Low Fuel Level")
   if brake_health < 60:
       alerts.append("Poor Brake Health")
   return alerts

# Apply the UDF and generate multiple alerts

alerts = telemetry_table.select(
   vehicle_id=pw.this.vehicle_id,
   timestamp=pw.this.timestamp,
   alert_type=detect_alerts(
       pw.this.engine_temp,
       pw.this.fuel_level,
       pw.this.brake_health
   )
)

# Filter rows with no alerts
alerts = alerts.flatten(pw.this.alert_type).filter(pw.this.alert_type.is_not_none())

# Output alerts to another NATS subject
pw.io.nats.write(
   alerts.select(
       vehicle_id=pw.this.vehicle_id,
       timestamp=pw.this.timestamp,
       alert_type=pw.this.alert_type
   ),
   uri="nats://127.0.0.1:4222",
   topic="fleet.alerts",
   format="json"
)

# Run the Pathway pipeline
pw.run()