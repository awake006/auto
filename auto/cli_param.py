from optparse import OptionParser


def parse_options():
    parser = OptionParser('Auto')
    parser.add_option(
        '-H', '--host',
        dest='host',
        default=None,
        help='Run the test host, read from the configuration file by default'
    )
    parser.add_option(
        '-T', '--create-template',
        dest='create_template',
        default=None,
        help='Create test cases and configuration file templates, stored in the api folder under the execution folder'
    )
    opts, _ = parser.parse_args()
    return opts
