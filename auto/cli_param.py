from optparse import OptionParser


def parse_options():
    parser = OptionParser('Auto')
    parser.add_option(
        '-C', '--case',
        dest='case',
        default=None,
        # action="store_false",
        help='Run a list of test cases, separated by ",", read from the configuration file by default'
    )
    parser.add_option(
        '-H', '--host',
        dest='host',
        default=None,
        help='Run the test host, read from the configuration file by default'
    )
    parser.add_option(
        '-P', '--case-path',
        dest='case_dir',
        default=None,
        help='Test case folder absolute path, default case folder under the execution folder'
    )
    parser.add_option(
        '-G', '--config-file',
        dest='config_file',
        default=None,
        help='The absolute path of the configuration file, the config/base_info.yaml file under the default execution folder'
    )
    parser.add_option(
        '-T', '--create-template',
        dest='create_template',
        default=None,
        help='Create test cases and configuration file templates, stored in the api folder under the execution folder'
    )
    opts, _ = parser.parse_args()
    return opts
