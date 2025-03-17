import socket
import datetime
import re
import platform
from http import cookies
from langdetect import detect
from geolite2 import geolite2

# Function to parse HTTP headers and extract cookies
def parse_http_headers(data):
    headers = {}
    lines = data.splitlines()
    for line in lines:
        parts = line.split(b': ')
        if len(parts) == 2:
            headers[parts[0].decode('utf-8')] = parts[1].decode('utf-8')

    # Extract cookies if present
    cookie_header = headers.get('Cookie', '')
    if cookie_header:
        cookie_dict = cookies.SimpleCookie(cookie_header)
        cookies_list = [morsel.OutputString() for morsel in cookie_dict.values()]
        return "; ".join(cookies_list)
    else:
        return "No cookies"

# Function to parse user agent string
def parse_user_agent(user_agent_string):
    # Example regex for parsing user agent
    pattern = r'\((.*?)\)'
    match = re.search(pattern, user_agent_string)
    if match:
        return match.group(1)
    return "Unknown"

# Function to get system information
def get_system_info():
    return platform.platform()

# Function to get geolocation based on IP address
def get_geolocation(ip_address):
    reader = geolite2.reader()
    location = reader.get(ip_address)
    if location and 'country' in location:
        return f"{location['country']['names']['en']}, {location['city']['names']['en'] if 'city' in location else 'Unknown'}"
    return "Unknown"

# Function to detect language from text
def detect_language(text):
    try:
        return detect(text)
    except:
        return "Unknown"

# Function to print connection details in a formatted table-like manner
def print_connection_details(connection_info):
    header = "[+] Connection details:"
    print(header)
    print("=" * len(header))
    print("{:<20} {:<20} {:<20} {:<20} {:<40} {:<40} {:<40} {:<20}".format("Time", "IP Address", "User Agent", "System Info", "Location", "Language", "Cookies", "Received Data"))
    print("-" * 200)
    for info in connection_info:
        location = info.get('location', 'Unknown')
        print("{:<20} {:<20} {:<20} {:<20} {:<40} {:<40} {:<40} {:<20}".format(info['time'], info['ip'], info['user_agent'], info['system'], location, info['language'], info['cookies'], info['data']))
    print("\n")

# Define the server address and port
server_address = ('localhost', 12345)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
sock.bind(server_address)

# Listen for incoming connections (backlog of 5)
sock.listen(5)

# List to store connection details
connection_info = []

print("[+] Listener started.\n")

while True:
    # Wait for a connection
    connection, client_address = sock.accept()

    try:
        # Get current timestamp
        connection_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract IP address
        ip_address = client_address[0]

        # Receive data from the client
        data = connection.recv(1024)
        if data:
            # Parse user agent string (assuming it's part of the received data)
            user_agent = parse_user_agent(data.decode())

            # Get system information
            system_info = get_system_info()

            # Parse HTTP headers (if applicable)
            headers = parse_http_headers(data)

            # Get geolocation based on IP address
            location = get_geolocation(ip_address)

            # Detect language of received data
            language = detect_language(data.decode())

            # Log the received data along with connection details
            log_message = f"Connection at {connection_time} from IP {ip_address}\n"
            log_message += f"User Agent: {user_agent}\n"
            log_message += f"System Info: {system_info}\n"
            log_message += f"Location: {location}\n"
            log_message += f"Language: {language}\n"
            log_message += f"Cookies: {headers}\n"
            log_message += f"Received Data: {data.decode()}\n"

            # Append connection details to list
            connection_info.append({
                'time': connection_time,
                'ip': ip_address,
                'user_agent': user_agent,
                'system': system_info,
                'location': location,
                'language': language,
                'cookies': headers,
                'data': data.decode()
            })

            # Print formatted connection details
            print_connection_details(connection_info)

    finally:
        # Clean up the connection
        connection.close()