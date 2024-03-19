# Domains with security.txt

This project will provide lists of domains with a security.txt file present. The data is separated into lists by top level domains.

The included python script scans a list of domains for the presence of a security.txt file. The results are printed in .csv format and visualized with pie charts.

## Table of Contents

- [Usage](#usage)
- [Skript Installation](#skript-installation)
- [Contributing](#contributing)
- [License](#license)

### Usage

Please refer to the data folder for the results of past scans.

To generate your own results install and run the `scan.py` script with the `-f` option to specify a .csv or .txt file containing the domains to check. Use the `-d` option to specify the directory to save the output file in (COM, DE, CO.UK, etc.).

Example:

```bash
python scan.py -f domains.csv -d COM
```

```bash
# --help for further information
python scan.py --help
```

## Skript Installation

```bash
git clone https://github.com/yourusername/domains-with-security-txt.git
cd domains-with-security-txt
pip install -r requirements.txt
```

## Contributing

Contributions are welcome. Please run the script with a list of domains for a specific top level domain and create a pull request with the results.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
