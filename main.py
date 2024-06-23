import requests
import pyfiglet
import json 

def find_sub_domains(domain):
    found_sub_domains = []

    # Query crt.sh to find subdomains
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sub_domains = set(item['name_value'] for item in data)

            for sub_domain in sub_domains:
                full_domain = sub_domain.strip()
                if not full_domain.startswith('*'):
                    try:
                        # Verify if the subdomain is active and get the status code
                        sub_response = requests.get(f"http://{full_domain}", timeout=5)
                        status_code = sub_response.status_code
                        found_sub_domains.append((full_domain, status_code))
                        print(f"Found: {full_domain} (Status: {status_code})")
                    except requests.ConnectionError:
                        pass
                    except requests.RequestException as e:
                        print(f"Error connecting to {full_domain}: {e}")
        else:
            print(f"Error fetching subdomains from crt.sh: HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching subdomains from crt.sh: {e}")

    return found_sub_domains

def print_banner():
   ascii_banner = pyfiglet.figlet_format("KURD", font="slant")
   print(ascii_banner)
   print("Create By Twanst Codes ")
   print("Github::  https://github.com/TwanstCodess/subdomainfinder.git")

if __name__ == "__main__":
    print_banner()
    domain = input("Enter Domain (e.g., example.com): ")
    found_sub_domains = find_sub_domains(domain)

    if found_sub_domains:
        print("\nDiscovered Subdomains:")
        for sub_domain, status in found_sub_domains:
            print(f"Subdomain: {sub_domain}, Status: {status}")
    else:
        print("No subdomains found.")
