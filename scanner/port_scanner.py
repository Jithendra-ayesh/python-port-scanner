import socket

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
    pass

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

    open_ports = []
    for port in range(1, 1025):
        if scan_port(ip, port):
            open_ports.append(port)
            print(f"Port {port} OPEN")

    print("\nScan Complete")
    print(f"Open Ports Found: {len(open_ports)}")

if __name__ == "__main__":
    main()