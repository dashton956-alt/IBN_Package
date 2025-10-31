# IBNaaS - Intent-Based Networking as a Service

An AI-powered infrastructure automation platform combining network automation, IPAM, and ChatOps capabilities.

## 🎯 Overview

IBNaaS integrates multiple tools to provide intelligent network infrastructure management:
- **NetBox** - DCIM/IPAM for network documentation
- **n8n** - Workflow automation and AI agent orchestration
- **StackStorm** - Event-driven automation
- **Kong** - API Gateway for service integration
- **AI Agents** - Natural language interface for infrastructure operations

## 📁 Project Structure

```
ibnaas/
├── docs/                    # 📚 All documentation
│   ├── chatops/            # ChatOps guides
│   ├── netbox/             # NetBox integration docs
│   ├── workflows/          # n8n workflow documentation
│   ├── architecture/       # Architecture diagrams
│   └── setup-guides/       # Installation & configuration
│
├── n8n/                    # n8n workflow engine
│   ├── workflows/          # Workflow JSON files
│   │   ├── netbox/        # NetBox workflows
│   │   ├── chatops/       # ChatOps workflows
│   │   ├── proxmox/       # Proxmox workflows
│   │   └── archived/      # Older workflow versions
│   ├── data/              # n8n data directory
│   └── Gluware/           # Gluware integration
│
├── scripts/                # Utility scripts
├── Kong/                   # Kong API Gateway config
├── netbox-docker/         # NetBox deployment
├── stackstorm/            # StackStorm automation
├── vault/                 # HashiCorp Vault
└── [other services]/      # Additional integrations

```

## 🚀 Quick Start

1. **Review Documentation**
   ```bash
   cd docs/
   cat README.md
   ```

2. **Start Core Services**
   ```bash
   # NetBox
   cd netbox-docker && docker-compose up -d
   
   # n8n
   cd n8n && docker-compose up -d
   ```

3. **Import Workflows**
   - Navigate to n8n UI: http://localhost:5678
   - Import workflows from `n8n/workflows/`

4. **Configure AI Agent**
   - See: `docs/netbox/NetBox_AI_Agent_Quick_Start.md`

## 📖 Documentation

All documentation is organized in the `/docs` directory:

- **[Getting Started](docs/setup-guides/POC_CHECKLIST.md)** - Implementation checklist
- **[Architecture](docs/architecture/POC_ARCHITECTURE.md)** - System design and topology
- **[ChatOps Setup](docs/chatops/CHATOPS_README.md)** - ChatOps configuration
- **[NetBox Workflows](docs/netbox/README.md)** - NetBox AI agent and workflows
- **[Troubleshooting](docs/setup-guides/TROUBLESHOOTING_TOOLS.md)** - Common issues and solutions

## 🔧 Key Components

### NetBox (DCIM/IPAM)
- **URL**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Workflows**: `n8n/workflows/netbox/`

### n8n (Workflow Automation)
- **URL**: http://localhost:5678
- **Workflows**: `n8n/workflows/`
- **Documentation**: `docs/workflows/`

### StackStorm (Event Automation)
- **URL**: http://localhost:443
- **Config**: `stackstorm/`

### Kong (API Gateway)
- **URL**: http://localhost:8000
- **Config**: `Kong/`

## 🤖 AI Agents

The project includes AI-powered agents for:
- **NetBox Operations** - Natural language DCIM/IPAM commands
- **ChatOps Interface** - Conversational infrastructure management
- **Proxmox Integration** - VM lifecycle automation

See: `docs/workflows/AI_AGENT_SETUP.md`

## 🛠️ Development

### Workflow Development
```bash
cd n8n/workflows/
# Edit JSON files or use n8n UI
```

### Script Development
```bash
cd scripts/
# Add utility scripts here
```

### Documentation
```bash
cd docs/
# Add/update markdown files
```

## 📊 Network Topology

Network diagrams and architecture documentation:
- `docs/architecture/NETWORK_DIAGRAM.md`
- `docs/architecture/*.png` - Visual diagrams
- `docs/architecture/*.puml` - PlantUML source files

## 🔐 Security

- Credentials managed via HashiCorp Vault
- See: `docs/setup-guides/VAULT_INTEGRATION.md`
- Environment variables in `.env` (not committed)

## 📝 TODOs & Roadmap

- See: `docs/chatops/CHATOPS_ROADMAP.md`
- See: `docs/setup-guides/INFRA_GAPS.md`

## 🐛 Troubleshooting

Common issues and solutions:
- [Troubleshooting Guide](docs/setup-guides/TROUBLESHOOTING_TOOLS.md)
- [Integration Issues](docs/setup-guides/INTEGRATIONS.md)

## 🤝 Contributing

1. Document changes in appropriate `docs/` subdirectory
2. Update relevant README files
3. Test workflows before committing
4. Follow existing naming conventions

## 📄 License

[Add license information]

## 📞 Support

- Documentation: `docs/`
- Issues: [Add issue tracker]
- Contact: [Add contact info]

---

**Last Updated**: October 31, 2025
