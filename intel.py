#!/usr/bin/env python


"""Extract and Validate NBIs and HBIs From Multiple Intel Sources."""

from classes.Arguments import GetArguments  # Get and validate arguments.
from classes import Data  # Format input data to a python list.
from classes.FileHashes import ExtractHashes  # Extract hashes from input data.
from classes.IPAddresses import ExtractIPs  # Extract IPs from input data.
from classes.Domains import ExtractDomains  # Extract domains from input data.
from classes.Emails import EmailAddresses  #  Extract email addresses from input data.

__program__ = "intel.py"
__author__ = "Johnny C. Wachter"
__copyright__ = "Copyright (C) 2014 Johnny C. Wachter"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Johnny C. Wachter"
__contact__ = "wachter.johnny@gmail.com"
__status__ = "Development"


def extract_indicators(input_data):
    """Extract Indicators From the Input Data."""

    results = []  # List to house all of the results.

    # All of these return a dictionary.
    hashes = ExtractHashes(input_data).get_valid_hashes()
    ips = ExtractIPs(input_data).get_ipv4_results()
    domains = ExtractDomains(input_data).get_valid_domains()
    emails = EmailAddresses(input_data).extract_email_addresses()

    # Only append non-empty lists to results.
    if hashes['md5_hashes']:

        results.extend(hashes['md5_hashes'])

    if hashes['sha256_hashes']:

        results.extend(hashes['sha256_hashes'])

    if ips['public_ips']:

        results.extend(ips['public_ips'])

    if domains['domain_list']:

        results.extend(domains['domain_list'])

    if emails:
        results.extend(emails)

    return results


def main():
    """Where the Automagic Happens."""

    args = GetArguments().valid_arguments  # Grab the arguments.

    input_data = []  # List to store all input data to be analyzed.

    for input_arg in args.input:

        input_path, path_type = input_arg  # Map tuple to variables.

        if path_type == 'file_path':

            # Append input data to the list.
            input_data.extend(Data.CleanData(input_path).to_list())

        elif path_type == 'url_path':

            # Grab the HTML from the page.
            data = Data.GetData(input_path).get_url()

            # Append input data to the list.
            input_data.extend(Data.CleanData(data).to_list())

    input_data = list(set(input_data))  # Remove duplicates.

    if args.output:

        # Open the output file in append mode.
        outfile = open(args.output, 'a+b')

    # Do, iff the 'extract' argument was passed.
    if args.extract:

        # Extracts indicators we care about and returns a dictionary.
        results = extract_indicators(input_data)

        for entry in results:

            print entry  # Always print to console.

            if args.output:

                # Write results to output file if provided.
                outfile.write(entry + "\n")


if __name__ == "__main__":
    main()
