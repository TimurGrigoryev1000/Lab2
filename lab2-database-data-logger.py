#!/usr/bin/env python3
"""
SYSC3010 Lab 2 - Exercise 3
Reads SenseHAT temperature/humidity/pressure once per second and logs to SQLite.

DB: sensorDB.db
Table: sensordata(id, datetime, temperature, humidity, pressure)
"""

import sqlite3
import time
from datetime import datetime

DB_PATH = "sensorDB.db"

# 
try:
    from sense_hat import SenseHat  
    sense = SenseHat()
    USE_SENSEHAT = True
except Exception:
    USE_SENSEHAT = False

def create_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sensordata (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          datetime TEXT NOT NULL,
          temperature REAL NOT NULL,
          humidity REAL NOT NULL,
          pressure REAL NOT NULL
        );
        """
    )
    conn.commit()

def read_sensors():
    if USE_SENSEHAT:
        # SenseHAT values are floats
        temp = float(sense.get_temperature())
        hum = float(sense.get_humidity())
        pres = float(sense.get_pressure())
        return temp, hum, pres

    t = time.time()
    temp = 20.0 + 2.0 * (0.5 - ((t % 10) / 10.0))
    hum = 40.0 + 5.0 * (0.5 - ((t % 20) / 20.0))
    pres = 1013.0 + 1.0 * (0.5 - ((t % 30) / 30.0))
    return temp, hum, pres

def insert_row(conn: sqlite3.Connection, dt_str: str, temp: float, hum: float, pres: float) -> None:
    conn.execute(
        "INSERT INTO sensordata(datetime, temperature, humidity, pressure) VALUES (?, ?, ?, ?);",
        (dt_str, temp, hum, pres),
    )
    conn.commit()

def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        create_table(conn)

        print("Logging sensor data to sensorDB.db (Ctrl+C to stop)...")
        if not USE_SENSEHAT:
            print("WARNING: SenseHAT not detected; using simulated values.")

        try:
            while True:
                dt_str = datetime.now().isoformat(timespec="seconds")
                temp, hum, pres = read_sensors()
                insert_row(conn, dt_str, temp, hum, pres)
                print(f"{dt_str}  T={temp:.2f}C  H={hum:.2f}%  P={pres:.2f}hPa")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped.")

if __name__ == "__main__":
    main()

