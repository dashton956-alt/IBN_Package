# GitHub ↔ n8n Automation - Quick Reference

## 🚀 Quick Setup (5 minutes)

### 1. Import n8n Workflows
```bash
# In n8n UI:
# 1. Import n8n-github-sync-workflow.json
# 2. Import n8n-ai-pr-review-workflow.json
# 3. Activate both workflows
# 4. Copy webhook URLs
```

### 2. Add GitHub Secrets
```bash
# Settings → Secrets → Actions → New secret
N8N_WEBHOOK_URL=https://your-n8n.com
N8N_API_KEY=n8n_api_xxxxx
N8N_BASE_URL=https://your-n8n.com
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 3. Add GitHub Actions
```bash
mkdir -p .github/workflows
cp sync-n8n-workflows.yml .github/workflows/
cp ai-pr-review.yml .github/workflows/
git add .github/workflows/ && git commit -m "Add automation" && git push
```

### 4. Test
```bash
# Create test workflow
cat > workflows/test.json <<JSON
{"name":"Test","nodes":[{"type":"n8n-nodes-base.start","position":[250,300]}],"connections":{}}
JSON

git add workflows/test.json
git commit -m "Test workflow sync"
git push origin master

# Check: GitHub Actions → n8n workflows
```

---

## 📋 Workflow Files

### Required Structure
```
your-repo/
├── .github/workflows/
│   ├── sync-n8n-workflows.yml    ← Triggers on push to master
│   └── ai-pr-review.yml          ← Triggers on PR
└── workflows/                     ← Your n8n workflows
    ├── automation/
    │   └── *.json
    ├── integrations/
    │   └── *.json
    └── *.json
```

### Example Workflow File
```json
{
  "name": "My Workflow",
  "nodes": [
    {
      "parameters": {},
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "position": [250, 300]
    }
  ],
  "connections": {},
  "settings": {},
  "tags": [{"name": "automation"}]
}
```

---

## 🔄 Workflow 1: GitHub → n8n Sync

**Trigger:** Push to master/main with `.json` files

**Webhook:** `/webhook/github-workflow-sync`

**What it does:**
1. ✓ Fetches workflows from GitHub
2. ✓ Validates JSON structure
3. ✓ Creates or updates in n8n
4. ✓ Preserves folder structure as tags
5. ✓ Posts sync report to commit

**Payload Example:**
```json
{
  "repository": "owner/repo",
  "ref": "refs/heads/master",
  "sha": "abc123",
  "n8n_api_key": "***",
  "github_token": "***",
  "n8n_base_url": "https://n8n.example.com",
  "workflow_path": "workflows"
}
```

---

## 🤖 Workflow 2: AI PR Review

**Trigger:** PR opened/updated with `.json` changes

**Webhook:** `/webhook/ai-pr-review`

**What it does:**
1. ✓ Fetches PR file changes
2. ✓ Sends to Claude AI for analysis
3. ✓ Posts detailed review comment
4. ✓ Submits formal PR review
5. ✓ Adds risk/quality labels

**Payload Example:**
```json
{
  "repository": "owner/repo",
  "pull_request": {
    "number": 123,
    "title": "Update workflow",
    "url": "..."
  },
  "github_token": "***",
  "anthropic_api_key": "***",
  "auto_comment": true,
  "review_depth": "standard"
}
```

---

## 🔑 Required Secrets

| Secret | Where to Get It | Used By |
|--------|----------------|---------|
| `N8N_WEBHOOK_URL` | Your n8n instance URL | Both |
| `N8N_API_KEY` | n8n Settings → API → Create | Sync |
| `N8N_BASE_URL` | Your n8n instance URL | Sync |
| `ANTHROPIC_API_KEY` | console.anthropic.com | Review |
| `GITHUB_TOKEN` | Auto-provided by GitHub | Both |

---

## 🎯 Manual Triggers

### Sync Workflow
```bash
# GitHub UI: Actions → Sync Workflows → Run workflow

Options:
- dry_run: true/false
- workflow_path: "workflows"
```

### AI Review
```bash
# GitHub UI: Actions → AI PR Review → Run workflow

Options:
- pr_number: 123
- auto_comment: true/false
```

---

## 🔍 Testing

### Test Sync
```bash
echo '{"name":"Test","nodes":[]}' > workflows/test.json
git add workflows/test.json
git commit -m "Test sync"
git push origin master
# Check: Actions tab + n8n
```

### Test Review
```bash
git checkout -b test-pr
echo '{"name":"Updated"}' > workflows/test.json
git commit -am "Update workflow"
git push origin test-pr
# Create PR in GitHub
# AI review auto-triggers
```

### Test Webhooks Locally
```bash
# Sync
curl -X POST http://localhost:5678/webhook/github-workflow-sync \
  -H "Content-Type: application/json" \
  -d '{"repository":"test/repo","ref":"refs/heads/master","sha":"abc123"}'

# Review
curl -X POST http://localhost:5678/webhook/ai-pr-review \
  -H "Content-Type: application/json" \
  -d '{"repository":"test/repo","pull_request":{"number":1}}'
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | Check API keys in secrets |
| Webhook timeout | Verify n8n URL is accessible |
| No workflows synced | Check file paths match `workflows/**/*.json` |
| AI review not posting | Ensure `auto_comment: true` and valid API keys |
| Invalid JSON | Validate with `python -m json.tool file.json` |

### Debug Mode
```yaml
# Add to GitHub Actions:
env:
  ACTIONS_STEP_DEBUG: true
```

---

## 📊 Monitoring

### Check Sync Status
```bash
# GitHub: Actions → Sync Workflows → Latest run
# n8n: Workflows → Check for new/updated workflows
```

### Check Review Status
```bash
# GitHub: PR → Conversation → Look for AI comment
# n8n: Executions → Filter by ai-pr-review
```

### View Logs
```bash
# GitHub Actions: Click on failed step → View logs
# n8n: Executions → Click execution → View node outputs
```

---

## 🎨 Customization

### Change Workflow Path
```yaml
# In sync-n8n-workflows.yml:
workflow_path: 'custom/path'
```

### Change Review Depth
```yaml
# In ai-pr-review.yml payload:
review_depth: 'deep'  # minimal/standard/deep
```

### Add Custom Tags
```javascript
// In n8n sync workflow, "Validate & Enrich" node:
workflowData.tags.push({ name: 'custom-tag' });
```

---

## 📈 Metrics to Track

- ✅ Sync success rate
- ⏱️ Average sync time
- 📊 Workflows synced per run
- 🎯 AI review accuracy
- 🚨 Failed syncs/reviews

---

## 🔒 Security Checklist

- [ ] Rotate API keys every 90 days
- [ ] Use separate keys for prod/dev
- [ ] Enable webhook signature verification
- [ ] Audit sync logs regularly
- [ ] Restrict GitHub token permissions
- [ ] Use secrets, never hardcode

---

## 📞 Support

**Issues:** Open GitHub issue
**Docs:** See GITHUB_N8N_AUTOMATION_GUIDE.md
**n8n:** docs.n8n.io
**Claude:** docs.anthropic.com

---

## ✨ Quick Tips

1. **Folder structure = tags** - Organize workflows in folders, they become tags in n8n
2. **Dry run first** - Test sync with `dry_run: true` before real import
3. **Manual review** - Set `auto_comment: false` to review AI output before posting
4. **Validate locally** - Check JSON before pushing: `python -m json.tool workflow.json`
5. **Monitor executions** - Check n8n Executions tab regularly for issues

---

**Last Updated:** 2025-01-01
**Version:** 1.0.0
