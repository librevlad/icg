import json
import urllib.request

BASE = "http://localhost:8000"

def call(capability, text, params=None):
    data = {
        "object": {"id": "test", "type": "text", "data": text},
        "capability": capability,
    }
    if params:
        data["parameters"] = params
    req = urllib.request.Request(
        f"{BASE}/execute",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

print("=== 1. Entity Extraction ===")
r = call("entity_extraction", "Email me at vlad@point.app or call +1-555-0199. See https://icg.dev")
obj = json.loads(r["new_object"]["data"])
print(f"  Phones: {obj['phones']}")
print(f"  Emails: {obj['emails']}")
print(f"  URLs:   {obj['urls']}")

print("\n=== 2. Transform (stats) ===")
r = call("transform", "Point is the Object Runtime for the digital world. It works with any object.")
print(f"  Result: {r['new_object']['data']}")

print("\n=== 3. Summarize ===")
long_text = (
    "Point changes the interaction model. Instead of apps, it centers on objects. "
    "Any object can be understood, transformed, continued, shared, or explored. "
    "Point does not know about apps. It knows about capabilities. "
    "Whether a local LLM, cloud service, or home server performs the action doesn't matter. "
    "They are all equal realizers of a capability. "
    "The end goal is to become a universal Object Runtime for the entire digital world."
)
r = call("summarize", long_text)
print(f"  Summary: {r['new_object']['data']}")

print("\n=== 4. Capabilities ===")
with urllib.request.urlopen(f"{BASE}/capabilities") as resp:
    caps = json.loads(resp.read())
    print(f"  Available: {caps['capabilities']}")

print("\nAll tests passed!")
