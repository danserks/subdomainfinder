import requests
import pyfiglet
import json
from colorama import Fore, Style  # Import libraries for color output

def find_sub_domains(domain):
  found_sub_domains = []
  animation_frames = ["[■]", "[□]", "[■]"]  # Define animation frames

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

            # Print subdomain with color and animation
            print(f"{Fore.GREEN}{animation_frames.pop(0)} Found: {full_domain} (Status: {status_code}){Style.RESET_ALL}")
            animation_frames.append("[■]")  # Reset animation frame order

            # Write found subdomain to log file
            with open("log.txt", "a") as logfile:
              logfile.write(f"{full_domain} (Status: {status_code})\n")

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
  print("Github:: https://github.com/TwanstCodess/subdomainfinder.git")

if __name__ == "__main__":
  print_banner()
  domain = input("Enter Domain (e.g., example.com): ")
  found_sub_domains = find_sub_domains(domain)

  if found_sub_domains:
    print("\nDiscovered Subdomains:")
    with open("log.txt", "r") as logfile:  # Read and print subdomains from log
      log_contents = logfile.read()
      print(log_contents)
  else:
    print("No subdomains found.")

  # Clear log file for next run (optional)
  # with open("log.txt", "w") as logfile:
  #   logfile.write("")
