'''
Module      : Main
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 2016
License     : MIT
Maintainer  : bjpope@unimelb.edu.au
Portability : POSIX

'''

from argparse import ArgumentParser
import sys
import logging
import csv
import feedparser
import urllib
import pkg_resources


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
EXIT_FASTA_FILE_ERROR = 3
PROGRAM_NAME = "insighter"

insight_url_base = "https://www.insight-database.org/api/rest.php/"
insight_genes_url = insight_url_base + "genes" 
insight_variants_url = insight_url_base + "variants/" 
insight_search_variant_query = "{gene}?search_Variant/DNA={variant}"


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Annotate variants using data from the InSiGHT database'
    parser = ArgumentParser(description=description)
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log',
                        metavar='LOG_FILE',
                        type=str,
                        help='record program progress in LOG_FILE')
    parser.add_argument('--column',
                        metavar='COLUMN',
                        type=str,
                        help='name of column containing variant in HGVSC format')
    parser.add_argument('variants',
                        metavar='VARIANTS_FILE',
                        type=str,
                        help='Input TSV file containing variant information')
    return parser.parse_args()



def init_logging(log_filename):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
                            level=logging.DEBUG,
                            filemode='w',
                            format='%(asctime)s %(levelname)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: %s', ' '.join(sys.argv))


def process_variants(column_title, variants_filepath, insight_genes):
    insight_genes = set(insight_genes)
    with open(variants_filepath) as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            variant = row[column_title]
            gene = row['gene']
            if variant and gene and gene in insight_genes:
                print(variant)
                if variant.startswith('NM'):
                    nm, variant = variant.split(':')
                quote_gene = urllib.parse.quote_plus(gene)
                quote_variant = urllib.parse.quote_plus(variant)
                search_query = insight_search_variant_query.format(gene=quote_gene, variant=quote_variant)
                search_url = insight_variants_url + search_query
                print(search_url)


def get_insight_genes():
    document = feedparser.parse(insight_genes_url)
    return [entry.title for entry in document.entries]


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.log)
    insight_genes = get_insight_genes()
    process_variants(options.column, options.variants, insight_genes)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
