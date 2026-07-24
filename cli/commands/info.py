from providers.registry import CapabilityRegistry
from discovery.discovery import LocalDiscoveryService

def setup_parser(subparsers):
    subparsers.add_parser("capabilities", help="List all available capabilities")
    subparsers.add_parser("providers", help="List all loaded providers")

def execute(args) -> int:
    registry = CapabilityRegistry()
    discovery = LocalDiscoveryService(registry)
    discovery.discover()
    
    if args.command == "capabilities":
        caps = set()
        for p in registry.get_all():
            caps.update(p.capabilities())
        print("Available Capabilities:")
        for c in sorted(caps):
            print(f" - {c}")
            
    elif args.command == "providers":
        print("Loaded Providers:")
        for p in registry.get_all():
            print(f" - {p.manifest.id} (v{p.manifest.version})")
            
    return 0
