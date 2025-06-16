#!/usr/bin/env python3
"""
Basic test script to verify ART infrastructure works.
Run this from the NVDA root directory.
"""

import sys
import time
import os
import subprocess
from pathlib import Path

def activate_venv():
	"""Activate the NVDA virtual environment."""
	venv_path = Path(__file__).parent / "venv"
	if not venv_path.exists():
		print("Virtual environment not found. Please run 'scons source' first.")
		sys.exit(1)
	
	# Add venv site-packages to Python path
	import site
	site_packages = venv_path / "Lib" / "site-packages"
	if site_packages.exists():
		site.addsitedir(str(site_packages))
		print(f"✓ Activated virtual environment: {venv_path}")
	else:
		print(f"✗ Virtual environment site-packages not found: {site_packages}")
		sys.exit(1)

# Activate venv before importing anything else
activate_venv()

# Add NVDA source to path
nvda_source = Path(__file__).parent / "source"
sys.path.insert(0, str(nvda_source))

# Set up minimal globalVars for testing
class MockAppArgs:
	secure = False
	logFileName = None
	logLevel = 20  # INFO
	debugLogging = False
	noLogging = False

# Import and set up basic NVDA modules
import globalVars
globalVars.appArgs = MockAppArgs()
globalVars.appDir = str(nvda_source.parent)

# Initialize basic logging
from logHandler import log
import logHandler
logHandler.initialize()

from art.manager import ARTManager

def test_basic_art():
	"""Test basic ART functionality."""
	print("=" * 50)
	print("Starting ART Basic Test")
	print("=" * 50)
	
	# Start ART manager
	print("1. Starting ARTManager...")
	manager = ARTManager()
	
	try:
		manager.start()
		print("   ✓ ARTManager started")
		
		# Wait for services to connect
		print("2. Waiting for service connections...")
		max_wait = 10  # seconds
		start_time = time.time()
		
		while time.time() - start_time < max_wait:
			if len(manager.artServices) >= 3:
				break
			time.sleep(0.5)
			print(f"   Services connected: {len(manager.artServices)}/3")
		
		if len(manager.artServices) >= 3:
			print("   ✓ All services connected")
			
			# List connected services
			for service_name in manager.artServices:
				print(f"     - {service_name}")
		else:
			print(f"   ✗ Only {len(manager.artServices)}/3 services connected")
			return False
		
		# Test addon service
		print("3. Testing AddOnLifecycleService...")
		addon_service = manager.getService("addon_lifecycle")
		if addon_service:
			print("   ✓ Connected to addon service")
			
			# Test getting loaded addons (should be empty initially)
			try:
				loaded_addons = addon_service.getLoadedAddons()
				print(f"   ✓ Current loaded addons: {loaded_addons}")
			except Exception as e:
				print(f"   ✗ Error getting loaded addons: {e}")
				return False
			
			# Try to load test addon
			test_addon_path = Path(__file__).parent / "test_addon"
			if test_addon_path.exists():
				print(f"4. Loading test addon from: {test_addon_path}")
				try:
					result = addon_service.loadAddon(str(test_addon_path))
					if result:
						print("   ✓ Test addon loaded successfully")
						
						# Check loaded addons again
						loaded_addons = addon_service.getLoadedAddons()
						print(f"   ✓ Loaded addons after test: {loaded_addons}")
					else:
						print("   ✗ Test addon failed to load")
						return False
				except Exception as e:
					print(f"   ✗ Error loading test addon: {e}")
					return False
			else:
				print("4. Skipping addon loading test (test_addon directory not found)")
		else:
			print("   ✗ Failed to connect to addon service")
			return False
		
		# Test extension point service
		print("5. Testing ExtensionPointService...")
		ext_service = manager.getService("extension_points")
		if ext_service:
			print("   ✓ Connected to extension point service")
		else:
			print("   ✗ Failed to connect to extension point service")
			return False
		
		# Test handler service
		print("6. Testing ExtensionPointHandlerService...")
		handler_service = manager.getService("handlers")
		if handler_service:
			print("   ✓ Connected to handler service")
		else:
			print("   ✗ Failed to connect to handler service")
			return False
		
		print("=" * 50)
		print("✓ ALL TESTS PASSED!")
		print("ART infrastructure is working correctly.")
		print("=" * 50)
		return True
		
	except Exception as e:
		print(f"✗ Test failed with exception: {e}")
		import traceback
		traceback.print_exc()
		return False
	
	finally:
		print("7. Shutting down ARTManager...")
		try:
			manager.stop()
			print("   ✓ ARTManager stopped cleanly")
		except Exception as e:
			print(f"   ✗ Error stopping ARTManager: {e}")

def create_test_addon():
	"""Create a minimal test addon if it doesn't exist."""
	test_addon_dir = Path(__file__).parent / "test_addon"
	test_addon_init = test_addon_dir / "__init__.py"
	
	if not test_addon_init.exists():
		print("Creating test addon...")
		test_addon_dir.mkdir(exist_ok=True)
		
		addon_code = '''"""
Minimal test addon for ART testing.
"""

# Test imports that should work in ART
try:
	import config
	print("✓ config module imported successfully in ART")
	
	# Test config access
	if hasattr(config, 'conf'):
		print("✓ config.conf is available")
	else:
		print("✗ config.conf not available")
		
except ImportError as e:
	print(f"✗ Failed to import config: {e}")

try:
	from logHandler import log
	print("✓ logHandler imported successfully in ART")
	
	# Test logging
	log.info("Test log message from ART addon")
	print("✓ Logging works in ART")
	
except ImportError as e:
	print(f"✗ Failed to import logHandler: {e}")

print("Test addon initialization complete!")
'''
		
		test_addon_init.write_text(addon_code, encoding='utf-8')
		print(f"   ✓ Created test addon at: {test_addon_init}")

if __name__ == "__main__":
	# Create test addon if needed
	create_test_addon()
	
	# Run the test
	success = test_basic_art()
	
	if success:
		print("\nTo run this test:")
		print("  python test_art_basic.py")
		print("\nNext steps:")
		print("  1. Integrate ARTManager into NVDA core startup")
		print("  2. Register extension points with names")
		print("  3. Create additional proxy modules")
	else:
		print("\nTest failed. Check the output above for details.")
		sys.exit(1)
