import socket
from datetime import datetime
import csv

def resolve_ip(url):
    try:
        # Remove any whitespace and strip http/https if present
        url = url.strip().lower()
        if url.startswith(('http://', 'https://')):
            url = url.split('://')[1]
        
        # Resolve IP address
        ip = socket.gethostbyname(url)
        return ip
    except socket.gaierror:
        return "Could not resolve"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Get current timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d")
    output_file = f"results_{timestamp}.txt"
    
    # Read URLs from input file
    try:
        with open('input.txt', 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: input.txt file not found!")
        return
    
    # Remove duplicates while preserving order
    urls = list(dict.fromkeys(urls))
    
    # Process URLs and write results
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['URL', 'IP Address'])  # Header
        
        for url in urls:
            ip = resolve_ip(url)
            writer.writerow([url, ip])
            print(f"Processed: {url} -> {ip}")
    
    print(f"\nResults have been saved to {output_file}")

if __name__ == "__main__":
    main() 