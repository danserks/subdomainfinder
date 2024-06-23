import requests

def find_sub_domains(domain, sub_domain_list):
    found_sub_domains = []
    for sub_domain in sub_domain_list:
        full_domain = f"{sub_domain}.{domain}"
        url = f"http://{full_domain}"
      
        try:
            response = requests.get(url)
  
            if response.status_code == 200:
                found_sub_domains.append(full_domain)
                print(f"Found: {full_domain}")
        except requests.ConnectionError:
            pass
        except requests.RequestException as e:
            print(f"Error connecting to {full_domain}: {e}")
    return found_sub_domains

def load_sub_domain(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

sub_domain_path = "subdomain.txt"
domain = input("Enter Domain/ Example.com: ")

sub_domain_list = load_sub_domain(sub_domain_path)
found_sub_domains = find_sub_domains(domain, sub_domain_list)

print(found_sub_domains)
