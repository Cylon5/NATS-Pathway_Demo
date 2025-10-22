import pathway as pw

# Define the telemetry schema
class TelemetrySchema(pw.Schema):
   turbine_id: str
   timestamp: str
   blade_length: float
   blade_width: float
   vibration: int
   temperature: int
   

# Ingest telemetry data from NATS
telemetry_table = pw.io.nats.read(
   uri="nats://host.docker.internal:4222",
   topic="turbine.telemetry",
   format="json",
   schema=TelemetrySchema
)

# Define a UDF for detecting alerts with if conditions
@pw.udf
def detect_alerts(vibration, temperature):
   alerts = []
   if vibration > 80:
       alerts.append("High Vibration Detected")
   if temperature > 100:
       alerts.append("High Temperature Detected")
   return alerts

# Apply the UDF and generate multiple alerts
alerts = telemetry_table.select(
   turbine_id=pw.this.turbine_id,
   timestamp=pw.this.timestamp,
   alert_type=detect_alerts(
       pw.this.vibration,
       pw.this.temperature,
   )
)

# Filter rows with no alerts
alerts = alerts.flatten(pw.this.alert_type).filter(pw.this.alert_type.is_not_none())

# Output alerts to another NATS subject
pw.io.nats.write(
   alerts.select(
       turbine_id=pw.this.turbine_id,
       timestamp=pw.this.timestamp,
       alert_type=pw.this.alert_type
   ),
   uri="nats://host.docker.internal:4222",
   topic="turbine.alerts",
   format="json"
)

# Run the Pathway pipeline
pw.run()