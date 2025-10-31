"""
title: NetBox Network Query Tool
author: ChatOps
version: 1.0.0
description: Query and interact with NetBox network inventory API
requirements: requests
"""

import os
import requests
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class Tools:
    def __init__(self):
        self.netbox_url = os.getenv("NETBOX_URL", "http://netbox-docker-netbox-1:8000")
        self.netbox_token = os.getenv("NETBOX_TOKEN", "")
        self.headers = {
            "Authorization": f"Token {self.netbox_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make API request to NetBox"""
        url = f"{self.netbox_url}/api/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=10)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def query_devices(
        self,
        name: Optional[str] = None,
        site: Optional[str] = None,
        device_type: Optional[str] = None,
        role: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        Query NetBox devices with optional filters.
        
        :param name: Filter by device name (partial match)
        :param site: Filter by site name
        :param device_type: Filter by device type
        :param role: Filter by device role
        :param limit: Maximum number of results to return (default 50)
        :return: JSON string with device information
        """
        params = {"limit": limit}
        if name:
            params["name__ic"] = name
        if site:
            params["site"] = site
        if device_type:
            params["device_type"] = device_type
        if role:
            params["role"] = role
        
        result = self._make_request("dcim/devices/", data=params)
        
        if "error" in result:
            return f"Error querying devices: {result['error']}"
        
        devices = result.get("results", [])
        if not devices:
            return "No devices found matching the criteria."
        
        # Format output
        output = f"Found {len(devices)} device(s):\n\n"
        for device in devices:
            output += f"- **{device.get('name')}**\n"
            output += f"  - Type: {device.get('device_type', {}).get('display', 'N/A')}\n"
            output += f"  - Role: {device.get('device_role', {}).get('display', 'N/A')}\n"
            output += f"  - Site: {device.get('site', {}).get('name', 'N/A')}\n"
            output += f"  - Status: {device.get('status', {}).get('label', 'N/A')}\n"
            output += f"  - Primary IP: {device.get('primary_ip', {}).get('address', 'N/A') if device.get('primary_ip') else 'N/A'}\n\n"
        
        return output
    
    def query_interfaces(
        self,
        device: Optional[str] = None,
        name: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        Query NetBox interfaces with optional filters.
        
        :param device: Filter by device name
        :param name: Filter by interface name
        :param limit: Maximum number of results to return (default 50)
        :return: JSON string with interface information
        """
        params = {"limit": limit}
        if device:
            params["device"] = device
        if name:
            params["name__ic"] = name
        
        result = self._make_request("dcim/interfaces/", data=params)
        
        if "error" in result:
            return f"Error querying interfaces: {result['error']}"
        
        interfaces = result.get("results", [])
        if not interfaces:
            return "No interfaces found matching the criteria."
        
        # Format output
        output = f"Found {len(interfaces)} interface(s):\n\n"
        for iface in interfaces:
            output += f"- **{iface.get('name')}** on {iface.get('device', {}).get('name', 'N/A')}\n"
            output += f"  - Type: {iface.get('type', {}).get('label', 'N/A')}\n"
            output += f"  - Enabled: {iface.get('enabled', False)}\n"
            output += f"  - MTU: {iface.get('mtu', 'N/A')}\n"
            output += f"  - Description: {iface.get('description', 'N/A')}\n\n"
        
        return output
    
    def query_vlans(
        self,
        vid: Optional[int] = None,
        name: Optional[str] = None,
        site: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        Query NetBox VLANs with optional filters.
        
        :param vid: Filter by VLAN ID
        :param name: Filter by VLAN name
        :param site: Filter by site name
        :param limit: Maximum number of results to return (default 50)
        :return: JSON string with VLAN information
        """
        params = {"limit": limit}
        if vid:
            params["vid"] = vid
        if name:
            params["name__ic"] = name
        if site:
            params["site"] = site
        
        result = self._make_request("ipam/vlans/", data=params)
        
        if "error" in result:
            return f"Error querying VLANs: {result['error']}"
        
        vlans = result.get("results", [])
        if not vlans:
            return "No VLANs found matching the criteria."
        
        # Format output
        output = f"Found {len(vlans)} VLAN(s):\n\n"
        for vlan in vlans:
            output += f"- **VLAN {vlan.get('vid')}** - {vlan.get('name')}\n"
            output += f"  - Site: {vlan.get('site', {}).get('name', 'N/A') if vlan.get('site') else 'Global'}\n"
            output += f"  - Status: {vlan.get('status', {}).get('label', 'N/A')}\n"
            output += f"  - Description: {vlan.get('description', 'N/A')}\n\n"
        
        return output
    
    def query_ip_addresses(
        self,
        address: Optional[str] = None,
        device: Optional[str] = None,
        interface: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        Query NetBox IP addresses with optional filters.
        
        :param address: Filter by IP address (partial match)
        :param device: Filter by device name
        :param interface: Filter by interface name
        :param limit: Maximum number of results to return (default 50)
        :return: JSON string with IP address information
        """
        params = {"limit": limit}
        if address:
            params["address__ic"] = address
        if device:
            params["device"] = device
        if interface:
            params["interface"] = interface
        
        result = self._make_request("ipam/ip-addresses/", data=params)
        
        if "error" in result:
            return f"Error querying IP addresses: {result['error']}"
        
        ips = result.get("results", [])
        if not ips:
            return "No IP addresses found matching the criteria."
        
        # Format output
        output = f"Found {len(ips)} IP address(es):\n\n"
        for ip in ips:
            output += f"- **{ip.get('address')}**\n"
            output += f"  - Status: {ip.get('status', {}).get('label', 'N/A')}\n"
            output += f"  - DNS Name: {ip.get('dns_name', 'N/A')}\n"
            if ip.get('assigned_object'):
                output += f"  - Assigned to: {ip.get('assigned_object', {}).get('display', 'N/A')}\n"
            output += f"  - Description: {ip.get('description', 'N/A')}\n\n"
        
        return output
    
    def query_prefixes(
        self,
        prefix: Optional[str] = None,
        site: Optional[str] = None,
        vlan: Optional[int] = None,
        limit: int = 50
    ) -> str:
        """
        Query NetBox IP prefixes with optional filters.
        
        :param prefix: Filter by IP prefix (CIDR notation)
        :param site: Filter by site name
        :param vlan: Filter by VLAN ID
        :param limit: Maximum number of results to return (default 50)
        :return: JSON string with prefix information
        """
        params = {"limit": limit}
        if prefix:
            params["prefix"] = prefix
        if site:
            params["site"] = site
        if vlan:
            params["vlan_id"] = vlan
        
        result = self._make_request("ipam/prefixes/", data=params)
        
        if "error" in result:
            return f"Error querying prefixes: {result['error']}"
        
        prefixes = result.get("results", [])
        if not prefixes:
            return "No prefixes found matching the criteria."
        
        # Format output
        output = f"Found {len(prefixes)} prefix(es):\n\n"
        for pfx in prefixes:
            output += f"- **{pfx.get('prefix')}**\n"
            output += f"  - Site: {pfx.get('site', {}).get('name', 'N/A') if pfx.get('site') else 'Global'}\n"
            output += f"  - Status: {pfx.get('status', {}).get('label', 'N/A')}\n"
            output += f"  - VLAN: {pfx.get('vlan', {}).get('display', 'N/A') if pfx.get('vlan') else 'N/A'}\n"
            output += f"  - Description: {pfx.get('description', 'N/A')}\n\n"
        
        return output
