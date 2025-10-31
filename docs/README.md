# IBNaaS Documentation

This directory contains all documentation for the Intent-Based Networking as a Service (IBNaaS) project.

## Directory Structure

### 📁 `/chatops/`
ChatOps integration documentation and guides:
- `CHATOPS_README.md` - Main ChatOps overview and setup
- `CHATOPS_DIRECT_API_README.md` - Direct API integration guide
- `CHATOPS_ROADMAP.md` - Future development roadmap

### 📁 `/netbox/`
NetBox integration documentation:
- `README.md` - NetBox workflows overview
- `NetBox_AI_Agent_Quick_Start.md` - Quick start guide for AI agent
- `NetBox_AI_Agent_Conversion_Summary.md` - Conversion notes and changes
- `NetBox_AI_Agent_Prompt.txt` - AI agent prompt template
- `Proxmox_to_NetBox_Conversion_Guide.md` - Integration with Proxmox

### 📁 `/workflows/`
n8n workflow documentation:
- `README.md` - n8n workflows overview
- `AI_AGENT_SETUP.md` - AI agent configuration
- `AI_CHAT_AGENT_INTEGRATION.md` - Chat integration setup
- `API_ENDPOINTS.md` - API endpoint reference

### 📁 `/architecture/`
System architecture and diagrams:
- `POC_ARCHITECTURE.md` - Proof of concept architecture
- `NETWORK_DIAGRAM.md` - Network topology documentation
- `*.png` - Architecture and network diagrams
- `*.puml` - PlantUML diagram sources
- `Intent of IBN.jpg` - Conceptual IBN diagram

### 📁 `/setup-guides/`
Installation and configuration guides:
- `INFRA_GAPS.md` - Infrastructure gap analysis
- `INTEGRATIONS.md` - Integration documentation
- `POC_CHECKLIST.md` - Implementation checklist
- `TROUBLESHOOTING_TOOLS.md` - Debugging and troubleshooting
- `VAULT_INTEGRATION.md` - HashiCorp Vault setup
- `OPEN_WEBUI_SETUP.md` - Open WebUI configuration

## Quick Links

### Getting Started
1. Review the [POC Architecture](architecture/POC_ARCHITECTURE.md)
2. Follow the [POC Checklist](setup-guides/POC_CHECKLIST.md)
3. Set up [ChatOps](chatops/CHATOPS_README.md)
4. Configure [NetBox AI Agent](netbox/NetBox_AI_Agent_Quick_Start.md)

### Common Tasks
- **NetBox Operations**: See [netbox/README.md](netbox/README.md)
- **Workflow Management**: See [workflows/README.md](workflows/README.md)
- **Troubleshooting**: See [setup-guides/TROUBLESHOOTING_TOOLS.md](setup-guides/TROUBLESHOOTING_TOOLS.md)
- **API Reference**: See [workflows/API_ENDPOINTS.md](workflows/API_ENDPOINTS.md)

## Related Directories

- `/n8n/workflows/` - n8n workflow JSON files
- `/scripts/` - Utility scripts and automation
- `/Kong/` - Kong API Gateway configuration
- `/netbox-docker/` - NetBox Docker setup
- `/stackstorm/` - StackStorm automation

## Contributing

When adding new documentation:
1. Place it in the appropriate subdirectory
2. Update this README with a reference
3. Use clear, descriptive filenames
4. Include a table of contents for longer documents

## Support

For issues or questions, refer to:
- [Troubleshooting Guide](setup-guides/TROUBLESHOOTING_TOOLS.md)
- [Integration Documentation](setup-guides/INTEGRATIONS.md)
