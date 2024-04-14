
import argparse
from .cmds.cmd_gen_sv import CmdGenSv

def getparser():
    parser = argparse.ArgumentParser()
    subparsrers = parser.add_subparsers(required=True)

    gen_sv = subparsrers.add_parser("gen-sv")
    gen_sv.add_argument("-m", "--module", action="append",
        help="Specifies a Python module to load")
    gen_sv.add_argument("-o", "--output", 
        help="Specifies the output file")
    gen_sv.add_argument("ifc",
        help="Specifies the interface to generate")

    gen_sv.set_defaults(func=CmdGenSv())



    return parser


def main():
    parser = getparser()
    args = parser.parse_args()

    args.func(args)
    pass

if __name__ == "__main__":
    main()

