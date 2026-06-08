import socket
from concurrent.futures import ThreadPoolExecutor
import time

def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip

    except socket.gaierror:
        return None

def scan_port(ip, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
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

def log_results():
    pass

def main():
    print("=" * 40)
    print(" Python Port Scanner ")
    print("=" * 40)

    host = input("\nEnter Host: ")

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
        results = executor.map(lambda port: process_port(ip, port), range(1, 1025)
        )

    for result in results:
        if result:
            port, service = result
            open_ports.append(port)

            print(f" {port:<10}{'OPEN':<10}{service}")

    end_time = time.time()
    print("\nScan Complete")
    print(f"Open Ports Found: {len(open_ports)}")
    print(f"Scan Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()