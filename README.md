# veryFunListener

A lightweight Python-based listener that captures and logs incoming TCP connections, extracting details such as user agent, system information, geolocation, language detection, and cookies from received data.

## Features
- Captures incoming TCP connections
- Extracts and logs:
  - IP Address
  - User Agent
  - System Information
  - Geolocation (Country & City)
  - Detected Language
  - Cookies (if applicable)
  - Received Data
- Displays connection details in a formatted table-like output

## Installation

Ensure you have Python installed along with the required dependencies. You can install them using:

```sh
pip install socket langdetect maxminddb geolite2
```

## Usage

1. Clone this repository:
   ```sh
   git clone https://github.com/naviNBRuas/veryFunListener.git
   cd veryFunListener
   ```

2. Run the listener:
   ```sh
   python main.py
   ```

3. The listener will start on `localhost:12345` and wait for incoming connections.

## Dependencies
- Python 3.x
- `socket` (Built-in)
- `platform` (Built-in)
- `datetime` (Built-in)
- `re` (Built-in)
- `http.cookies` (Built-in)
- `langdetect` (Language detection)
- `geolite2` (Geolocation based on IP address)

## Notes
- This tool is for **educational and research purposes only**. Use it responsibly.
- Ensure you have the required MaxMind GeoLite2 database for IP geolocation.

## License
This project is licensed under the MIT License.

