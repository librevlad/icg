import pytest
import os
import shutil
from discovery.discovery import LocalDiscoveryService
from providers.registry import CapabilityRegistry

def test_local_discovery():
    os.makedirs("test_providers/my_prov", exist_ok=True)
    with open("test_providers/my_prov/manifest.yaml", "w") as f:
        f.write("id: my_prov\nversion: '1.0'\ncapabilities: [\"test_cap\"]")
        
    reg = CapabilityRegistry()
    disc = LocalDiscoveryService(reg, "test_providers")
    provs = disc.discover()
    
    assert len(provs) == 1
    assert "test_cap" in provs[0].capabilities()
    assert len(reg.get_all()) == 1
    
    shutil.rmtree("test_providers")
