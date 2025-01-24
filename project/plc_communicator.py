import snap7
import json
import time
from database import save_value  # Import the save_value function

# Load the configuration from the JSON file
def load_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config

# Main logic
if __name__ == "__main__":
    # Load configuration
    config = load_config()
    plc_config = config['plc']
    db_number = plc_config['db_number']
    ip = plc_config['ip']
    rack = plc_config['rack']
    slot = plc_config['slot']

    # Connect to PLC
    plc = snap7.client.Client()
    try:
        plc.connect(ip, rack, slot)
        print("Connected to PLC.")

        while True:
            # Read data block
            try:
                db_data = plc.db_read(db_number, 0, 8)  # Read 8 bytes for temperature and pressure
                temperature = snap7.util.get_real(db_data, 0)  # Read REAL at offset 0
                pressure = snap7.util.get_real(db_data, 4)  # Read REAL at offset 4

                # Log and save data
                print(f"Temperature: {temperature}, Pressure: {pressure}")
                save_value("temperature", temperature)
                save_value("pressure", pressure)

                time.sleep(0.5)  # 500ms polling interval
            except Exception as e:
                print(f"Error reading data from PLC: {e}")
                break

    except Exception as e:
        print(f"Error connecting to PLC: {e}")
    finally:
        plc.disconnect()
        print("Disconnected from PLC.")
