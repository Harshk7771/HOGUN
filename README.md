# Web$cr@@per

Web$cr@@per is a Python-based web scraping tool designed to perform various web analysis tasks including web scraping, subdomain enumeration, and WHOIS lookup. This tool is built to help in collecting and analyzing data from websites efficiently.

## Key Features

- **Web Scraping**: Extract information such as title, meta description, links, images, paragraphs, scripts, stylesheets, and emails from a target website.
- **Subdomain Enumeration**: Enumerate subdomains for a given domain using the CertSpotter API.
- **WHOIS Lookup**: Retrieve WHOIS information for a given domain or IP address.
- **Customizable and Extensible**: Easily modify and extend the tool to include more features as needed.
- **User-friendly Interface**: Simple command-line interface for ease of use.
- **Data Saving**: Option to save the extracted information in JSON format.

## Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `cfscrape`
  - `whois`
  - `tqdm`

## Installation

1. **Clone the repository:**
2. 
   git clone https://github.com/Harshk7771/Webscrapper
   cd webscraper

    Install the required packages:

    pip install requests beautifulsoup4 cfscrape python-whois tqdm

**Usage**

    Run the Web Scraper:

    python scraper.py

    Main Menu:
        1. Web Scraping: Enter a URL to scrape and extract information.
        2. Sub Domain Enumeration: Enter a domain to enumerate subdomains using CertSpotter API.
        3. WHOIS Lookup: Enter a domain or IP address to perform a WHOIS lookup.
        4. Exit: Exit the program.

    Follow the prompts to perform the desired tasks and optionally save the results.

**Code Overview**
scraper.py

This is the main file of the web scraper tool. It includes the following key functions:

    print_banner(): Displays the banner of the tool.
    save_results(task, results): Saves the extracted results to a JSON file.
    json_serial(obj): Serializes JSON objects.
    custom_input(prompt): Custom input function to handle keyboard interrupts.
    web_scraping(target_url): Performs web scraping on the given URL.
    sub_domain_enumeration(target_domain, api_key): Enumerates subdomains for the given domain using CertSpotter API.
    whois_lookup(target_domain): Performs a WHOIS lookup for the given domain or IP address.
    main(): The main function that displays the menu and handles user choices.

**Key Methods**

    print_banner(): Displays an ASCII art banner.
    save_results(task, results): Saves results to a JSON file.
    json_serial(obj): Handles serialization of datetime objects for JSON.
    custom_input(prompt): Wraps the built-in input to handle keyboard interrupts gracefully.
    web_scraping(target_url): Scrapes various elements from a given URL.
    sub_domain_enumeration(target_domain, api_key): Uses CertSpotter API to find subdomains.
    whois_lookup(target_domain): Retrieves WHOIS information for a domain or IP address.
    main(): Main loop for user interaction.

**Contributing**

If you would like to contribute to this project, please fork the repository and submit a pull request.
License

This project is open source and available under the MIT License.
Contact

For any questions or suggestions, please contact the author.
