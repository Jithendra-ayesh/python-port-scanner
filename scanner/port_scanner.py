import socket
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime
import os

def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip

    except socket.gaierror:
        return None

def scan_port(ip, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(0.8)
    result = scanner.connect_ex((ip, port))

    scanner.close()
    return result == 0

def detect_service(port):
    try:
        return socket.getservbyport(port)

    except OSError:
        return "unknown"
    
def process_port(ip, port):
    if scan_port(ip, port):
        service = detect_service(port)
        return (port, service)

    return None

def log_results(host, ip, start_port, end_port, open_ports, scan_time):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "logs",
        "scan_results.txt"
    )

    with open(log_file, "a") as file:

        file.write("\n" + "=" * 50 + "\n")
        file.write(f"Scan Date : {timestamp}\n")
        file.write(f"Host      : {host}\n")
        file.write(f"IP        : {ip}\n")
        file.write(f"Port Range: {start_port}-{end_port}\n")
        file.write("=" * 50 + "\n\n")

        file.write(f"{'PORT':<10}{'SERVICE'}\n")
        file.write("-" * 25 + "\n")

        for port, service in open_ports:
            file.write(f"{port:<10}{service}\n")

        file.write("\n")
        file.write(f"Open Ports Found : {len(open_ports)}\n")
        file.write(f"Scan Time        : {scan_time:.2f} sec\n")
        file.write("\n" + "=" * 50 + "\n")

def main():
    print("=" * 40)
    print(" Python Port Scanner ")
    print("=" * 40)

    host = input("\nEnter Host: ")
    try:
        start_port = int(input("Enter Start Port: "))
        end_port = int(input("Enter End Port: "))

    except ValueError:
        print("Invalid port number.")
        return
    
    if start_port < 1 or end_port > 65535:
        print("Ports must be between 1 and 65535.")
        return

    if start_port > end_port:
        print("Start port must be less than end port.")
        return

    ip = resolve_host(host)

    if not ip:
        print("Unable to resolve host.")
        return

    print(f"\nResolved IP: {ip}")
    print("\nScanning ports...\n")

    start_time = time.time()

    open_ports = []

    print(f"{'PORT':<10}{'STATUS':<10}{'SERVICE'}")
    print("-" * 30)

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda port: process_port(ip, port), range(start_port, end_port + 1)
        )

    for result in results:
        if result:
            port, service = result
            open_ports.append((port, service))

            print(f" {port:<10}{'OPEN':<10}{service}")

    end_time = time.time()
    scan_time = end_time - start_time
    print("\nScan Complete")
    print(f"Open Ports Found: {len(open_ports)}")
    print(f"Scan Time: {scan_time:.2f} seconds")

    log_results(host, ip, start_port, end_port, open_ports, scan_time)

    print("\nResults saved to logs/scan_results.txt")

if __name__ == "__main__":
    main()