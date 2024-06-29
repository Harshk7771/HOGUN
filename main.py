import requests
from bs4 import BeautifulSoup
import time
import cfscrape
import socket
import whois
from tqdm import tqdm
import re
import json
from urllib.parse import urlparse
import builtins
from datetime import datetime

def print_banner():
    banner = """
    ██╗░░██╗░█████╗░░██████╗░██╗░░░░░██╗███╗░░██╗
    ██║░░██║██╔══██╗██╔════╝░██║░░░░░██║████╗░██║
    ███████║██║░░██║██║░░██╗░██║░░░░░██║██╔██╗██║
    ██╔══██║██║░░██║██║░░╚██╗██║░░░░░██║██║╚████║
    ██║░░██║╚█████╔╝░╚██████╔╝╚██████╔╝██║░╚███║
    ╚═╝░░╚═╝░╚════╝░░░╚═════╝░░╚═════╝░╚═╝░░╚══╝

    Web$cr@@per by hk23
    """
    print(banner)

def save_results(task, results):
    filename = f"{task}_results.json"
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4, default=json_serial)
    print(f"Results saved to {filename}")

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def custom_input(prompt):
    try:
        return builtins.input(prompt)
    except KeyboardInterrupt:
        print("Scan interrupted. Returning to main menu.")
        return None

def web_scraping(target_url):
    try:
        scraper = cfscrape.create_scraper()
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }

        if not target_url.startswith('http://') and not target_url.startswith('https://'):
            target_url = 'https://' + target_url

        print("Web Scraping in progress...")
        response = scraper.get(target_url, headers=headers)
        time.sleep(2)  # Add a delay of 2 seconds
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting information
        title = soup.title.string if soup.title else "No title found"
        meta_description = soup.find('meta', {'name': 'description'})
        description = meta_description['content'] if meta_description else "No meta description found"

        # Extracting links
        links = [link.get('href') for link in tqdm(soup.find_all('a', href=True), desc="Links")]

        # Extracting images
        images = [img.get('src') for img in tqdm(soup.find_all('img', src=True), desc="Images")]

        # Extracting paragraphs
        paragraphs = [p.text.strip() for p in tqdm(soup.find_all('p'), desc="Paragraphs")]

        # Extracting scripts
        scripts = [script['src'] for script in tqdm(soup.find_all('script', src=True), desc="Scripts")]

        # Extracting stylesheets
        stylesheets = [link['href'] for link in tqdm(soup.find_all('link', rel='stylesheet', href=True), desc="Stylesheets")]

        # Extracting emails using a simple regex (you may need to improve this)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)

        print(f"\nWebsite Title: {title}")
        print(f"Meta Description: {description}")

        # Display extracted information
        print("\nLinks:")
        for idx, link in enumerate(links, start=1):
            print(f"{idx}. {link}")

        print("\nImages:")
        for idx, img in enumerate(images, start=1):
            print(f"{idx}. {img}")

        print("\nParagraphs:")
        for idx, para in enumerate(paragraphs, start=1):
            print(f"{idx}. {para}")

        print("\nScripts:")
        for idx, script in enumerate(scripts, start=1):
            print(f"{idx}. {script}")

        print("\nStylesheets:")
        for idx, stylesheet in enumerate(stylesheets, start=1):
            print(f"{idx}. {stylesheet}")

        print("\nEmails:")
        for idx, email in enumerate(emails, start=1):
            print(f"{idx}. {email}")

        results = {
            "Website Title": title,
            "Meta Description": description,
            "Links": links,
            "Images": images,
            "Paragraphs": paragraphs,
            "Scripts": scripts,
            "Stylesheets": stylesheets,
            "Emails": emails
        }

        save_option = custom_input("Do you want to save this information? (yes/no): ")
        if save_option.lower() == 'yes':
            save_results("web_scraping", results)

        return title, description, links, images, paragraphs, scripts, stylesheets, emails

    except KeyboardInterrupt:
        print("Scan interrupted. Returning to main menu.")
        return None, None, None, None, None, None, None, None

def sub_domain_enumeration(target_domain, api_key):
    try:
        subdomains = []

        # Extract domain from the URL
        target_domain = target_domain.split('//')[-1] if '//' in target_domain else target_domain
        target_domain = target_domain.split('/')[0] if '/' in target_domain else target_domain

        api_url = f"https://api.certspotter.com/v1/issuances?domain={target_domain}&include_subdomains=true&expand=dns_names"
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(api_url, headers=headers)
        data = response.json()

        for entry in data:
            dns_names = entry.get('dns_names', [])
            for name in dns_names:
                if name.endswith(f'.{target_domain}'):
                    subdomains.append(name)

        results = {"Subdomains": subdomains}
        save_option = custom_input("Do you want to save this information? (yes/no): ")
        if save_option.lower() == 'yes':
            save_results("sub_domain_enumeration", results)

        return subdomains

    except KeyboardInterrupt:
        print("Scan interrupted. Returning to main menu.")
        return None

def whois_lookup(target_domain):
    try:
        # Extract domain from the URL
        parsed_url = urlparse(target_domain) if '//' in target_domain else urlparse('http://' + target_domain)
        target_domain = parsed_url.netloc or parsed_url.path

        # Check if the target_domain is an IP address
        try:
            socket.inet_pton(socket.AF_INET, target_domain)
            ipwhois = whois.whois(target_domain)
        except socket.error:
            # If it's not an IP address, proceed with domain lookup
            ipwhois = whois.whois(target_domain)

        results = {"Whois Info": ipwhois}
        save_option = custom_input("Do you want to save this information? (yes/no): ")
        if save_option.lower() == 'yes':
            save_results("whois_lookup", results)

        return ipwhois

    except whois.parser.PywhoisError as e:
        print(f"Error during WHOIS lookup: {e}")

    except KeyboardInterrupt:
        print("Scan interrupted. Returning to the main menu.")
        return None

def main():
    print_banner()

    while True:
        print("\nMain Menu:")
        print("1. Web Scraping")
        print("2. Sub Domain Enumeration")
        print("3. WHOIS Lookup")
        print("4. Exit")

        choice = custom_input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            while True:
                target_url = custom_input("Enter the target URL (e.g., https://www.example.com): ")
                website_title, website_description, links, images, paragraphs, scripts, stylesheets, emails = web_scraping(target_url)

                if website_title is not None:  # Check if the scan was not interrupted
                    print(f"\nWebsite Title: {website_title}")
                    print(f"Meta Description: {website_description}")

                    # Display other extracted information as needed
                    # For example:
                    print("\nExtracted Links:")
                    for idx, link in enumerate(links, start=1):
                        print(f"{idx}. {link}")

                    print("\nExtracted Images:")
                    for idx, img in enumerate(images, start=1):
                        print(f"{idx}. {img}")

                    # Similarly, you can display other extracted information

                scan_more = custom_input("Do you want to scan more websites? (yes/no): ")
                if scan_more.lower() != 'yes':
                    break

        elif choice == '2':
            while True:
                target_domain = custom_input("Enter the target domain: ")
                api_key = 'k52727_3MmrnGXl3P18OE68tArz'  # Add your CertSpotter API key here
                subdomains = sub_domain_enumeration(target_domain, api_key)

                if subdomains is not None:  # Check if the scan was not interrupted
                    print("\nSubdomains:", subdomains)

                # Prompt for saving information after the loop
                save_option = custom_input("Do you want to save this information? (yes/no): ")
                if save_option.lower() == 'yes':
                    # Save the information (you can add your saving logic here)
                    print("Information saved successfully.")

                scan_more = custom_input("Do you want to scan more websites? (yes/no): ")
                if scan_more.lower() != 'yes':
                    break

        elif choice == '3':
            while True:
                target_domain = custom_input("Enter the target domain or IP address: ")
                whois_info = whois_lookup(target_domain)

                if whois_info is not None:  # Check if the scan was not interrupted
                    print("\nWhois Info:", whois_info)

                    # Prompt for saving information after the loop
                    save_option = custom_input("Do you want to save this information? (yes/no): ")
                    if save_option.lower() == 'yes':
                        # Save the information (you can add your saving logic here)
                        print("Information saved successfully.")

                scan_more = custom_input("Do you want to scan more websites? (yes/no): ")
                if scan_more.lower() != 'yes':
                    break

        elif choice == '4':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
