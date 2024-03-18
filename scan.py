import click
import csv
import requests

# Click options
# -f file
# -v verbose
# -o output 

@click.command()
@click.option('-f', '--file', help='File with domains to check. Available formats: .csv, .txt')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose mode')
@click.option('-o', '--output', help='Output file to save results. Available formats: .csv, .txt')
def check_for_security_txt(file, verbose, output):

    # Read domains from the CSV file
    domains = []
    with open('domains.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Verify that the row is not empty
            if row:
                domains.append(row[0])

    for domain in domains:
        url = f'https://www.{domain}/.well-known/security.txt'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f'{domain} has a security.txt file')
            else:
                print(f'{domain} does not have a security.txt file')
        except requests.exceptions.RequestException as e:
            print(f'Error checking domain: {e}')
