"""
This script checks for the presence of a security.txt file in a list of domains. The results are printed in .csv format and visualized with pie charts.
Author: http://github.com/schmuckware
"""

import os
import csv
from datetime import datetime

import click
import requests
import matplotlib.pyplot as plt


# List of paths to check for security.txt
SECURITY_TXT_PATHS = ["/.well-known/", "/"]


@click.command()
@click.option('-f', '--file', default="domains.csv", help='File with domains to check. Available formats: .csv, .txt')
@click.option('-v', '--verbose', is_flag=True, help='Print to console aswell')
@click.option('-d', '--directory', required=True, help='Directory to save the output file in. Could be the top level domain like a country code DE, CO.UK or COM. Refer to the GitHub README for more information.')
def check_for_security_txt(file, verbose, directory):

    # Read domains from the provided .txt or .csv file
    domains = read_domains_from_file(file)

    # Initialize counters
    total_domains = len(domains)
    found_counter = 0
    not_found_counter = 0

    # Initialize a dictionary to count in which path security.txt was found
    path_counter = {path: 0 for path in SECURITY_TXT_PATHS}

    results = []
    # Check for security.txt with the provided paths
    for domain in domains:
        found_or_errored = False
        for path in SECURITY_TXT_PATHS:
            url = f'https://www.{domain}{path}security.txt'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # Print if verbose is enabled in script options
                    print(f'Found at {url}') if verbose else None
                    results.append((domain, 'Found', url)
                                   ) if not found_or_errored else None
                    found_or_errored = True
                    found_counter += 1
                    # Increment the count for this path
                    path_counter[path] += 1
                else:
                    print(f'Nothing found at {url}') if verbose else None
            # Catch any exceptions that might occur when checking the URL
            except requests.exceptions.RequestException as e:
                print(f'Error checking {url}: {e}') if verbose else None
                found_or_errored = True
                break

        # If not found in any of the paths, add to the results
        if not found_or_errored:
            results.append((domain, 'Not found'))
            not_found_counter += 1

    # Calculate the error counter
    error_counter = total_domains - found_counter - not_found_counter

    # Print all counters
    print(f'\nTotal domains checked for security.txt: {total_domains}')
    print(f'Found: {found_counter}')
    print(f'Not found: {not_found_counter}')
    print(f'Error checking domain: {error_counter}')
    # Print the counts for each path
    for path, count in path_counter.items():
        print(f'Number of times security.txt found in {path}: {count}')

    # Get the current date to later include in the filenames
    date = datetime.now().strftime('%Y-%m-%d')

    # Create the output directory
    directory = os.path.normpath(os.path.join('data', directory))

    # Write results to the output file
    write_results_to_output_file(results, date, directory)
    # Create two pie charts to visualize the results and save them in the output directory
    visualize_results(found_counter, not_found_counter,
                      path_counter, date, directory)


def read_domains_from_file(file):
    domains = []
    file_extension = os.path.splitext(file)[1]

    # Handle both .csv and .txt files
    try:
        with open(file, 'r') as f:
            if file_extension == '.csv':
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        domains.append(row[0])
            elif file_extension == '.txt':
                domains = [line.strip() for line in f]
            # Quit if the file extension is not supported
            else:
                print('File extension not supported. Please provide a .csv or .txt file')
                exit(1)
        return domains
    except FileNotFoundError as e:
        print(f'File not found: {e}')
        exit(1)
    except Exception as e:
        print(f'Error reading file: {e}')
        exit(1)


def write_results_to_output_file(results, date, directory):
    try:
        # Create the country code directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        file = f'{date}_result.csv'
        # Write output into a .csv file in the country code directory
        file_path = os.path.join(directory, file)
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(results)
        print(f'\nResults saved to {file_path}')
    except IOError as e:
        print(f'Error writing to file: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')


def visualize_results(found_counter, not_found_counter, path_counter, date, directory):
    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2)

    # Pie chart for the domain counters
    labels = [f'Found: {found_counter}',
              f'Not found: {not_found_counter}']
    sizes = [found_counter, not_found_counter]
    axs[0].pie(sizes, labels=labels, explode=[0.04, 0.04],
               shadow=True, autopct='%1.1f%%')
    axs[0].set_title('Domains with a security.txt')
    fig.suptitle(f'Number of domains checked without errors: {
                 found_counter + not_found_counter}')

    # Pie chart for the path counters
    labels = [f'Found {count} at\n{path}' for path,
              count in path_counter.items()]
    sizes = path_counter.values()
    axs[1].pie(sizes, labels=labels, explode=[0.04, 0.04],
               shadow=True, autopct='%1.1f%%')
    axs[1].set_title('Paths with security.txt')

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    # Save the visualisation
    path = os.path.join('data', directory)
    os.makedirs(directory, exist_ok=True)
    file = f'{date}_visualisation.png'
    file_path = os.path.join(directory, file)
    fig.savefig(file_path)
    print(f'Visualisation saved to {file_path}')


if __name__ == '__main__':
    check_for_security_txt()
