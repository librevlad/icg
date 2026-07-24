from providers.registry import CapabilityRegistry
from discovery.discovery import LocalDiscoveryService

def setup_parser(subparsers):
    p = subparsers.add_parser("discover", help="Scan and discover providers")
    p.add_argument("--path", default="./providers", help="Path to scan")

def execute(args) -> int:
    registry = CapabilityRegistry()
    discovery = LocalDiscoveryService(registry, search_path=args.path)
    providers = discovery.discover()
    print(f"Discovered {len(providers)} providers.")
    for p in providers:
        print(f" - {p.manifest.id}: {p.capabilities()}")
    return 0
