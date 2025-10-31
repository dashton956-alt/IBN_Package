"""
title: StackStorm Workflow Tool
author: ChatOps
version: 1.0.0
description: Trigger and monitor StackStorm workflows for network automation
requirements: requests
"""

import os
import requests
import json
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class Tools:
    def __init__(self):
        self.st2_url = os.getenv("ST2_API_URL", "http://st2-docker-st2api-1:9101")
        self.st2_api_key = os.getenv("ST2_API_KEY", "")
        self.headers = {
            "St2-Api-Key": self.st2_api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make API request to StackStorm"""
        url = f"{self.st2_url}/v1/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=data, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=30)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            response.raise_for_status()
            return response.json() if response.content else {"success": True}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def list_actions(
        self,
        pack: Optional[str] = None,
        limit: int = 50
    ) -> str:
        """
        List available StackStorm actions/workflows.
        
        :param pack: Filter by pack name (e.g., 'core', 'chatops', 'network')
        :param limit: Maximum number of results to return (default 50)
        :return: Formatted string with action information
        """
        params = {"limit": limit}
        if pack:
            params["pack"] = pack
        
        result = self._make_request("actions", data=params)
        
        if "error" in result:
            return f"Error listing actions: {result['error']}"
        
        if isinstance(result, list):
            actions = result
        else:
            actions = result if isinstance(result, list) else []
        
        if not actions:
            return "No actions found."
        
        # Format output
        output = f"Found {len(actions)} action(s):\n\n"
        for action in actions:
            output += f"- **{action.get('ref')}**\n"
            output += f"  - Pack: {action.get('pack')}\n"
            output += f"  - Description: {action.get('description', 'N/A')}\n"
            if action.get('parameters'):
                params_list = ', '.join(action.get('parameters', {}).keys())
                output += f"  - Parameters: {params_list}\n"
            output += "\n"
        
        return output
    
    def execute_action(
        self,
        action: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Execute a StackStorm action/workflow.
        
        :param action: Action reference (e.g., 'core.local', 'chatops.deploy_config')
        :param parameters: Dictionary of parameters for the action
        :return: Execution ID and status
        """
        if parameters is None:
            parameters = {}
        
        data = {
            "action": action,
            "parameters": parameters
        }
        
        result = self._make_request("executions", method="POST", data=data)
        
        if "error" in result:
            return f"Error executing action: {result['error']}"
        
        execution_id = result.get('id', 'unknown')
        status = result.get('status', 'unknown')
        
        output = f"**Action Executed**\n\n"
        output += f"- Execution ID: `{execution_id}`\n"
        output += f"- Action: {action}\n"
        output += f"- Status: {status}\n"
        output += f"- Started: {result.get('start_timestamp', 'N/A')}\n"
        
        if parameters:
            output += f"- Parameters: {json.dumps(parameters, indent=2)}\n"
        
        output += f"\nUse `get_execution_status('{execution_id}')` to check progress.\n"
        
        return output
    
    def get_execution_status(
        self,
        execution_id: str
    ) -> str:
        """
        Get the status of a StackStorm execution.
        
        :param execution_id: The execution ID to check
        :return: Execution status and details
        """
        result = self._make_request(f"executions/{execution_id}")
        
        if "error" in result:
            return f"Error getting execution status: {result['error']}"
        
        status = result.get('status', 'unknown')
        action = result.get('action', {}).get('ref', 'unknown')
        
        output = f"**Execution Status**\n\n"
        output += f"- Execution ID: `{execution_id}`\n"
        output += f"- Action: {action}\n"
        output += f"- Status: **{status}**\n"
        output += f"- Started: {result.get('start_timestamp', 'N/A')}\n"
        
        if result.get('end_timestamp'):
            output += f"- Ended: {result.get('end_timestamp')}\n"
        
        # Show result if completed
        if status in ['succeeded', 'failed']:
            if result.get('result'):
                output += f"\n**Result:**\n```json\n{json.dumps(result.get('result'), indent=2)}\n```\n"
        
        # Show parameters used
        if result.get('parameters'):
            output += f"\n**Parameters:**\n```json\n{json.dumps(result.get('parameters'), indent=2)}\n```\n"
        
        return output
    
    def list_executions(
        self,
        action: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """
        List recent StackStorm executions.
        
        :param action: Filter by action name
        :param status: Filter by status (succeeded, failed, running, etc.)
        :param limit: Maximum number of results (default 10)
        :return: Formatted string with execution history
        """
        params = {"limit": limit}
        if action:
            params["action"] = action
        if status:
            params["status"] = status
        
        result = self._make_request("executions", data=params)
        
        if "error" in result:
            return f"Error listing executions: {result['error']}"
        
        if isinstance(result, list):
            executions = result
        else:
            executions = result if isinstance(result, list) else []
        
        if not executions:
            return "No executions found."
        
        # Format output
        output = f"Found {len(executions)} execution(s):\n\n"
        for execution in executions:
            exec_id = execution.get('id', 'unknown')
            exec_action = execution.get('action', {}).get('ref', 'unknown')
            exec_status = execution.get('status', 'unknown')
            exec_start = execution.get('start_timestamp', 'N/A')
            
            # Status emoji
            status_emoji = {
                'succeeded': '✅',
                'failed': '❌',
                'running': '🔄',
                'pending': '⏳',
                'canceled': '🚫'
            }.get(exec_status, '❓')
            
            output += f"{status_emoji} **{exec_action}**\n"
            output += f"  - ID: `{exec_id}`\n"
            output += f"  - Status: {exec_status}\n"
            output += f"  - Started: {exec_start}\n\n"
        
        return output
    
    def cancel_execution(
        self,
        execution_id: str
    ) -> str:
        """
        Cancel a running StackStorm execution.
        
        :param execution_id: The execution ID to cancel
        :return: Cancellation confirmation
        """
        # First check if execution exists and is running
        result = self._make_request(f"executions/{execution_id}")
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        status = result.get('status', 'unknown')
        
        if status not in ['running', 'pending']:
            return f"Cannot cancel execution {execution_id}. Current status: {status}"
        
        # Cancel the execution
        cancel_result = self._make_request(
            f"executions/{execution_id}",
            method="DELETE"
        )
        
        if "error" in cancel_result:
            return f"Error canceling execution: {cancel_result['error']}"
        
        return f"✅ Execution `{execution_id}` has been canceled."
    
    def get_execution_logs(
        self,
        execution_id: str
    ) -> str:
        """
        Get the output/logs of a StackStorm execution.
        
        :param execution_id: The execution ID
        :return: Execution logs
        """
        result = self._make_request(f"executions/{execution_id}")
        
        if "error" in result:
            return f"Error getting execution logs: {result['error']}"
        
        output = f"**Execution Logs for `{execution_id}`**\n\n"
        output += f"- Action: {result.get('action', {}).get('ref', 'unknown')}\n"
        output += f"- Status: {result.get('status', 'unknown')}\n\n"
        
        # Get stdout/stderr if available
        result_data = result.get('result', {})
        
        if result_data.get('stdout'):
            output += f"**Standard Output:**\n```\n{result_data['stdout']}\n```\n\n"
        
        if result_data.get('stderr'):
            output += f"**Standard Error:**\n```\n{result_data['stderr']}\n```\n\n"
        
        if result_data.get('return_code') is not None:
            output += f"Return Code: {result_data['return_code']}\n"
        
        # If no stdout/stderr, show full result
        if not result_data.get('stdout') and not result_data.get('stderr'):
            output += f"**Result:**\n```json\n{json.dumps(result_data, indent=2)}\n```\n"
        
        return output
    
    def list_workflows(
        self,
        limit: int = 20
    ) -> str:
        """
        List available StackStorm workflows (action aliases and chains).
        
        :param limit: Maximum number of results (default 20)
        :return: Formatted list of workflows
        """
        # Get action-chains (workflows)
        result = self._make_request("actions", data={"limit": limit, "runner_type": "action-chain"})
        
        if "error" in result:
            return f"Error listing workflows: {result['error']}"
        
        workflows = result if isinstance(result, list) else []
        
        if not workflows:
            return "No workflows found."
        
        output = f"Found {len(workflows)} workflow(s):\n\n"
        for workflow in workflows:
            output += f"- **{workflow.get('ref')}**\n"
            output += f"  - Pack: {workflow.get('pack')}\n"
            output += f"  - Description: {workflow.get('description', 'N/A')}\n"
            output += f"  - Enabled: {workflow.get('enabled', False)}\n\n"
        
        return output
