from optparse import OptionParser


def parse_options():
    parser = OptionParser(usage="test")
    parser.add_option(
        '-n',
        dest='number',
        type='int',
        help='input number'
    )
    opts, _ = parser.parse_args()
    return opts


def main():
    value_obj = parse_options()
    if value_obj.number:
        print(value_obj.number)
    else:
        print('please input number,use -n value')


if __name__ == "__main__":
    main()
