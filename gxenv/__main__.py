import sys

import gxenv.cli


if __name__ == "__main__":
    parser = gxenv.cli.create_argparse_instance()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if 'run' in sys.argv[1:3]:
        parsed, unknown = parser.parse_known_args()
        parsed.run_(parsed, meta={'argv': unknown})

    parsed = parser.parse_args()
    parsed.run_(parsed)
