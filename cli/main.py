import argparse
import sys
from cli.commands import run, info, discover

def main():
    parser = argparse.ArgumentParser(description="ICG CLI - Internet Capability Graph")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    run.setup_parser(subparsers)
    info.setup_parser(subparsers)
    discover.setup_parser(subparsers)
    
    args = parser.parse_args()
    
    if args.command == "run":
        sys.exit(run.execute(args))
    elif args.command in ("capabilities", "providers"):
        sys.exit(info.execute(args))
    elif args.command == "discover":
        sys.exit(discover.execute(args))

if __name__ == "__main__":
    main()
