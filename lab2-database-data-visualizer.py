import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "sensorDB.db"


conn = sqlite3.connect(DB_NAME)

#  load SQL query result into a pandas 
df = pd.read_sql_query(
    "SELECT datetime, temperature, humidity, pressure FROM sensordata ORDER BY datetime ASC;",
    conn
)

conn.close()

#  check that data exists
if df.empty:
    print("No data found. Run the logger first to insert rows.")
    raise SystemExit

#  FIX: parse ISO-8601 datetime strings correctly
df["datetime"] = pd.to_datetime(df["datetime"], format="ISO8601")

print("Rows loaded:", len(df))
print(df.head(25))

#  plot
plt.figure()

plt.plot(
    df["datetime"],
    df["temperature"],
    marker="o",
    linestyle="-",
    label="Temperature (C)"
)

plt.plot(
    df["datetime"],
    df["humidity"],
    marker="o",
    linestyle="-",
    label="Humidity (%)"
)

plt.plot(
    df["datetime"],
    df["pressure"],
    marker="o",
    linestyle="-",
    label="Pressure (mbar)"
)

plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Sensor data over time")
plt.legend()
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

# save the plot image 
plt.savefig("lab2-database-plot.png", dpi=200)

# show the plot window
plt.show()

print("Saved plot to lab2-database-plot.png")
