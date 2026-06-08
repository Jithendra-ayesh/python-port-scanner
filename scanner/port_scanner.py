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
    try:
        return socket.getservbyport(port)

    except OSError:
        return "unknown"

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

    print(f"{'PORT':<10}{'STATUS':<10}{'SERVICE'}")
    print("-" * 30)

    for port in range(1, 1025):
        if scan_port(ip, port):
            open_ports.append(port)
            service = detect_service(port)
            print(f" {port:<5}{'OPEN':<12} {service}")

    print("\nScan Complete")
    print(f"Open Ports Found: {len(open_ports)}")

if __name__ == "__main__":
    main()