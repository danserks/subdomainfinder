import requests
import pyfiglet
import json
from colorama import Fore, Style, init  # Import libraries for color output

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

def print_colored_banner(text, language):
  colors = [Fore.RED, Fore.YELLOW, Fore.GREEN]  # Define color choices
  if language == "Kurdish Sorani":
    text = "دۆزرایەوە"  # Replace with Kurdish Sorani text for banner
    message = "ئەمانەی کە دۆزراوەتەوە لە سەبدۆمەین"  # Kurdish message for discovered subdomains

  # Combine colors for a gradient effect
  color_gradient = "".join([color for color in colors])
  ascii_banner = pyfiglet.figlet_format(text, font="slant")
  print(color_gradient + ascii_banner + Style.RESET_ALL)  # Print banner with gradient

if __name__ == "__main__":
  init(autoreset=True)  # Initialize colorama for colored output

  # Ask for language preference
  language_options = {"English (default)": "English", "Kurdish Sorani": "Kurdish Sorani"}
  default_language = "English"
  while True:
    print("Choose language:")
    for option, code in language_options.items():
      print(f"- {option}")
    selected_language = input("Enter your choice (default: English): ")
    if selected_language.lower() in language_options.keys() or not selected_language:
      language = language_options.get(selected_language, default_language)
      break
    else:
      print("Invalid selection. Please choose a valid language.")

  # Print colored banner based on language
  print_colored_banner("KURD", language)
  domain = input("Enter Domain (e.g., example.com): ")
  found_sub_domains = find_sub_domains(domain)

  if found_sub_domains:
    # Print Kurdish message for discovered subdomains only for Kurdish Sorani
    if language == "Kurdish Sorani":
      print(message)
    print("\nDiscovered Subdomains:")  # Print in English for clarity
    with open("log.txt", "r") as logfile:  # Read and print subdomains from log
      log_contents =
