import os
import time

import log
from influxdb_client import InfluxDBClient

logger = log.get_module_logger("Main")

bucket = "scadadata"
names = ["/home/wp/state[T-Boiler]",
         "/home/wp/state[T-Sauggas]",
         "/home/wp/state[T-Puffer]",
         "/home/wp/state[T-Heissgas]",
         "/home/wp/state[T-Abtauung]",
         "/home/wp/state[T-Vorlauf]",
         "/home/wp/state[T-Raum]",
         "/home/wp/state[T-Aussen]",
        ]


client = InfluxDBClient(url=os.getenv("INFLUXDB_URL"), port=8086, token=os.getenv("INFLUXDB_TOKEN"), org=os.getenv("INFLUXDB_ORG"))
query_api = client.query_api()
delete_api = client.delete_api()

logger.info("Connected to InfluxDB.")
logger.info("Starting to search for weird Datapoints.")


while True:
    found = False
    for name in names:

        query = f"""
        from(bucket: "{bucket}")
        |> range(start: -3h)
        |> filter(fn: (r) => r["name"] == "{name}")
        |> derivative(unit: 1s, nonNegative: false, columns: ["_value"], timeColumn: "_time")
        |> filter(fn: (r) => r._value < -0.5)
        """

        result = query_api.query(query)

        if len(result) > 0:
            found = True
            records = result[0].records

            logger.info(f"Remove {len(records)} weird values from {name}.")

            for entry in records:
                measurement = entry.get_measurement()
                start = entry.get_time()
                stop = entry.get_time()
                delete_api.delete(start, stop, f'_measurement="{measurement}"', bucket=bucket, org='scada')
                #write_api.write(bucket, 'scada', [{"measurement": measurement, "fields": {"value": 1}, "time": 1}])
        
        query = f"""
        from(bucket: "{bucket}")
        |> range(start: -3h)
        |> filter(fn: (r) => r["name"] == "{name}")
        |> derivative(unit: 1s, nonNegative: true, columns: ["_value"], timeColumn: "_time")
        |> filter(fn: (r) => r._value > 0.5)
        """
        result = query_api.query(query)

        if len(result) > 0:
            found = True
            records = result[0].records

            logger.info(f"Remove {len(records)} weird values from {name}.")

            for entry in records:
                measurement = entry.get_measurement()
                start = entry.get_time()
                stop = entry.get_time()
                delete_api.delete(start, stop, f'_measurement="{measurement}"', bucket=bucket, org='scada')

    if not found:
        logger.info("No weird values found.")           
    time.sleep(60)