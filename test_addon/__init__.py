"""
Minimal test addon for ART testing.
This addon tests basic functionality in the ART process.
"""

# Test imports that should work in ART
try:
	import config
	print("✓ config module imported successfully in ART")
	
	# Test config access
	if hasattr(config, 'conf'):
		print("✓ config.conf is available")
		
		# Try to access a config value
		try:
			# Test reading a config section
			general_section = config.conf.get("general", {})
			print(f"✓ Read general config section: {type(general_section)}")
			
			# Test writing a config value
			config.conf["testART"] = {"testKey": "testValue"}
			print("✓ Config write test successful")
			
		except Exception as e:
			print(f"✗ Config access error: {e}")
	else:
		print("✗ config.conf not available")
		
except ImportError as e:
	print(f"✗ Failed to import config: {e}")

try:
	from logHandler import log
	print("✓ logHandler imported successfully in ART")
	
	# Test different log levels
	log.info("Test INFO message from ART addon")
	log.debug("Test DEBUG message from ART addon")
	log.warning("Test WARNING message from ART addon")
	print("✓ Logging works in ART")
	
except ImportError as e:
	print(f"✗ Failed to import logHandler: {e}")

# Test that we're actually running in a separate process
import os
print(f"✓ Test addon running in process ID: {os.getpid()}")

print("=" * 40)
print("✓ Test addon initialization complete!")
print("=" * 40)
