import yaml
import io

customSections = {
	"Base": {
		"spec": {"greeting": "string(default='')"},
		"isBaseOnly": True,
	},
}

# Simulate saveCustomSections
buf = io.StringIO()
yaml.safe_dump(customSections, buf, allow_unicode=True)
written = buf.getvalue()
print("=== WRITTEN TO FILE ===")
print(repr(written))
print()
print(written)

# Simulate loadCustomSections
loaded = yaml.safe_load(written)
print("=== LOADED FROM FILE ===")
print(loaded)
print()

# Check what addSection receives
for name, entry in loaded.items():
	spec = entry.get("spec")
	isBaseOnly = entry.get("isBaseOnly", False)
	print(f"name={name!r}")
	print(f"  spec={spec!r}  (type: {type(spec).__name__})")
	print(f"  isBaseOnly={isBaseOnly!r}")
	print(
		f"  spec value type: {type(next(iter(spec.values()))).__name__}" if spec else "  spec is empty/None"
	)
