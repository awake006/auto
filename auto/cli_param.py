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
        '-C', '--create-template',
        dest='create_template',
        default=None,
        help='Create test cases and configuration file templates, stored in the api folder under the execution folder'
    )
    parser.add_option(
        '-T', '--token',
        dest='token',
        default=None,
        help='token,default configuration'
    )
    parser.add_option(
        '-R', '--report',
        dest='report_format',
        default=None,
        help='xml or html'
    )
    opts, _ = parser.parse_args()
    return opts
