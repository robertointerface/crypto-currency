import argparse

parser = argparse.ArgumentParser(prog='display_kraken',
                                 usage='%(prog)s [options]',
                                 allow_abbrev=False,
                                 description='Display Kraken data')

parser.add_argument('symbol',
                    metavar='symbol',
                    action='store',
                    type=str,
                    help='coin symbol to search for')
parser.add_argument('-t',
                    metavar='time',
                    dest='start_time',
                    type=str,
                    action='store',
                    default='2021-08-01', # set default begining of august
                    help='start date of data being display')
parser.add_argument('-o',
                    metavar='output',
                    dest='output_format',
                    type=str,
                    action='store',
                    choices=['stdout', 'csv'],
                    default='stdout')
parser.add_argument('-p',
                    metavar='path',
                    dest='path',
                    type=str,
                    action='store',
                    required=True)

args = parser.parse_args()


if __name__ == '__main__':
    args = parser.parse_args()
    # normalize the input data
    print(vars(args))
    # query the data by using symbols and time
    # output the data