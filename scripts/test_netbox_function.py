#!/usr/bin/env python3
"""
Test script to verify netbox_function.py works correctly
"""

import os
import sys

# Set environment variables
os.environ["NETBOX_URL"] = "http://netbox-docker-netbox-1:8000"
os.environ["NETBOX_TOKEN"] = "b6ec5fa9fb961fe932dc7a396058f93afbafad9e"

# Import the function
sys.path.insert(0, '/home/dan/ibnaas')
from netbox_function import Tools

# Test the function
print("="*60)
print("Testing NetBox Function")
print("="*60)

tools = Tools()
print("\n1. Testing query_devices()...")
print("-"*60)
result = tools.query_devices()
print(result)

print("\n2. Testing query_devices with name filter...")
print("-"*60)
result = tools.query_devices(name="Fox")
print(result)

print("\n3. Testing query_vlans()...")
print("-"*60)
result = tools.query_vlans()
print(result)

print("\n="*60)
print("Test Complete!")
print("="*60)
