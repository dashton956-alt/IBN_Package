# GitHub Integration Workflows v2

## 🎉 What's New in v2

The v2 workflows replace HTTP Request nodes with **native GitHub nodes** and use **GitHub Triggers** for automatic webhook setup.

### Key Improvements

✅ **Native GitHub Integration**
- Uses `n8n-nodes-base.githubTrigger` for automatic webhook registration
- Uses `n8n-nodes-base.github` nodes for all GitHub API operations
- No manual webhook configuration needed

✅ **Simplified Authentication**
- Single GitHub API credential configuration
- Environment variables for sensitive keys
- No more Bearer token headers in every HTTP node

✅ **Better Error Handling**
- Native node error responses
- Automatic retry logic
- Better status reporting

✅ **Enhanced Features**
- Automatic commit status updates
- PR label management
- Better event filtering

---

## 📦 Available Workflows

### 1. GitHub → n8n Workflow Sync (v2)
**File:** `github-n8n-sync-v2.json`

**Purpose:** Automatically syncs workflow JSON files from GitHub to n8n when you push to the repository.

**Trigger:** GitHub Push Event (any branch)

**What It Does:**
1. Listens for push events via GitHub webhook
2. Filters commits that modified `.json` workflow files
3. Fetches workflow content from GitHub
4. Validates and enriches workflows with tags
5. Creates new workflows or updates existing ones in n8n
6. Updates GitHub commit status with sync results

**Key Nodes:**
- **GitHub Push Trigger** - Webhook receives push events
- **Get Repository Files** - Uses GitHub node to fetch file list
- **Fetch Workflow Content** - Uses GitHub node to download files
- **Update Commit Status** - Reports sync status back to GitHub

**Environment Variables Required:**
```bash
N8N_API_KEY=your_n8n_api_key
N8N_HOST=http://localhost:5678  # Optional, defaults to localhost
```

**GitHub Credentials:**
- Create GitHub API credential in n8n
- Requires repo permissions: `repo:status`, `repo:contents`

---

### 2. GitHub AI Pull Request Review (v2)
**File:** `github-ai-pr-review-v2.json`

**Purpose:** Automatically reviews pull requests containing workflow changes using Claude AI and posts feedback.

**Trigger:** GitHub Pull Request Events (opened, synchronize, reopened)

**What It Does:**
1. Listens for PR opened/updated events
2. Fetches changed files from the PR
3. Filters for workflow JSON files
4. Sends comprehensive context to Claude AI
5. Parses AI review for risk level, approval status, quality score
6. Posts review as PR comment
7. Submits formal PR review (Approve/Request Changes/Comment)
8. Adds labels: `ai-reviewed`, `risk:low/medium/high`, `approved`/`needs-review`

**Key Nodes:**
- **GitHub PR Trigger** - Webhook receives PR events
- **Get PR Files** - Uses GitHub node to list changed files
- **Post PR Comment** - Uses GitHub node to comment
- **Submit PR Review** - Uses GitHub node to submit formal review
- **Add PR Labels** - Uses GitHub node to tag PR

**Environment Variables Required:**
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
```

**GitHub Credentials:**
- Create GitHub API credential in n8n
- Requires permissions: `pull_request`, `issues`, `contents`

**AI Model:**
- Claude Sonnet 4 (claude-sonnet-4-20250514)
- Max tokens: 4096
- Temperature: 0.3 (focused, consistent reviews)

---

## 🚀 Setup Instructions

### Step 1: Install Workflows in n8n

1. Import both JSON files into your n8n instance
2. Or use the GitHub sync workflow to automatically import them!

### Step 2: Configure GitHub Credentials

1. In n8n, go to **Credentials** → **Add Credential**
2. Select **GitHub API**
3. Enter your GitHub Personal Access Token (PAT)
4. Grant required permissions:
   - `repo` (full repository access)
   - `workflow` (if syncing GitHub Actions)

**Create GitHub PAT:**
```
GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
Generate new token (classic):
✅ repo (all)
✅ workflow
```

### Step 3: Set Environment Variables

Edit your n8n environment configuration:

```bash
# .env file or docker-compose environment
N8N_API_KEY=your_n8n_api_key_here
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
N8N_HOST=http://localhost:5678
```

**Get n8n API Key:**
```
n8n → Settings → API → Create API Key
```

**Get Anthropic API Key:**
```
https://console.anthropic.com/ → API Keys → Create Key
```

### Step 4: Activate Workflows

1. Open each workflow in n8n
2. Click **Activate** toggle (top right)
3. The GitHub triggers will automatically:
   - Register webhooks with GitHub
   - Configure webhook URL
   - Set webhook secret

### Step 5: Test the Workflows

**Test Workflow Sync:**
```bash
# Make a change to a workflow file
echo '{"name": "test"}' > workflows/test.json
git add workflows/test.json
git commit -m "Test workflow sync"
git push
```

Watch n8n executions - should see:
- ✅ Push event received
- ✅ Workflow files detected
- ✅ Files synced to n8n
- ✅ Commit status updated

**Test AI PR Review:**
```bash
# Create a branch and modify a workflow
git checkout -b test-pr
# Edit a workflow file
git commit -am "Update workflow"
git push -u origin test-pr
# Create PR on GitHub
```

Watch n8n executions - should see:
- ✅ PR event received
- ✅ Workflow files analyzed
- ✅ AI review generated
- ✅ Comment posted on PR
- ✅ Labels added

---

## 🔧 Configuration Options

### Workflow Sync Customization

**Filter by folder:**
Edit the "Filter Workflow Files" node:
```javascript
// Only sync from specific folder
file.path.startsWith('workflows/production')
```

**Add custom tags:**
Edit the "Validate & Enrich Workflow" node:
```javascript
// Add environment tag
workflowData.tags.push({ name: 'production' });
```

**Skip certain files:**
```javascript
// Skip archived workflows
!file.path.includes('/archived/')
```

### AI Review Customization

**Adjust AI model:**
Edit the "Call Claude AI API" node:
```json
{
  "model": "claude-opus-4-20250514",  // More powerful model
  "max_tokens": 8192,                  // Longer reviews
  "temperature": 0.5                   // More creative
}
```

**Custom review criteria:**
Edit the "Build Analysis Context" node to change the prompt.

**Auto-merge approved PRs:**
Add a node after "Submit PR Review" that merges PRs with APPROVE status.

---

## 📊 Comparison: v1 vs v2

| Feature | v1 (HTTP Nodes) | v2 (GitHub Nodes) |
|---------|----------------|------------------|
| **Trigger Setup** | Manual webhook config | Automatic registration |
| **Authentication** | Bearer token in each node | Single credential |
| **GitHub Operations** | HTTP Request nodes | Native GitHub nodes |
| **Error Handling** | Manual status codes | Built-in retry logic |
| **Credentials** | Stored in workflow | Centralized credential |
| **Webhook Management** | Manual URL setup | Auto-managed by n8n |
| **Code Complexity** | Higher | Lower |
| **Maintenance** | More effort | Less effort |

---

## 🛠️ Troubleshooting

### Webhook Not Receiving Events

**Check:**
1. Workflow is activated
2. GitHub credentials are valid
3. Webhook is registered: `GitHub Repo → Settings → Webhooks`
4. n8n is accessible from internet (or use ngrok for testing)

**View webhook deliveries:**
```
GitHub → Repo → Settings → Webhooks → Recent Deliveries
```

### Authentication Errors

**Issue:** 401 Unauthorized

**Fix:**
1. Regenerate GitHub PAT with correct scopes
2. Update n8n GitHub API credential
3. Reactivate workflows

### AI Review Not Posting

**Issue:** Claude API errors

**Check:**
1. `ANTHROPIC_API_KEY` is set correctly
2. API key has credits/quota remaining
3. Check n8n execution logs for error details

### Workflows Not Syncing

**Issue:** Files detected but not imported

**Check:**
1. `N8N_API_KEY` is valid
2. N8N_HOST points to correct n8n instance
3. Workflow JSON is valid (use JSON validator)
4. n8n API is accessible from workflow execution

---

## 📝 Best Practices

### Repository Structure
```
your-repo/
├── workflows/
│   ├── production/
│   │   ├── critical-workflow.json
│   │   └── backup-workflow.json
│   ├── staging/
│   │   └── test-workflow.json
│   └── archived/
│       └── old-workflow.json
```

### Workflow Naming
- Use descriptive names: `NetBox Create Site`
- Include category prefix: `NetBox/Create Site`
- Add version tags: `v2.0`

### Git Workflow
1. Create feature branch
2. Modify workflows
3. Create PR (triggers AI review)
4. Address feedback
5. Merge to main (triggers sync)
6. Workflows automatically deployed to n8n!

### Security
- ✅ Never commit API keys to repository
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Use separate keys for dev/prod
- ✅ Review webhook security settings

---

## 🎯 Next Steps

1. **Archive v1 workflows** - Move to `archived/` folder
2. **Monitor executions** - Check n8n execution history
3. **Customize prompts** - Adjust AI review criteria
4. **Add notifications** - Send Slack/email on sync complete
5. **Create templates** - Build workflow scaffolding
6. **Add tests** - Validate workflows before sync

---

## 📚 Related Documentation

- [n8n GitHub Node Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.github/)
- [n8n GitHub Trigger Documentation](https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.githubtrigger/)
- [Anthropic Claude API Documentation](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)

---

## 🆘 Support

If you encounter issues:

1. Check n8n execution logs
2. Review GitHub webhook delivery logs
3. Verify credentials and environment variables
4. Check the original workflow documentation
5. Test with minimal workflow first

**Version:** 2.0.0  
**Last Updated:** October 31, 2025  
**Author:** IBN_Package Automation Team
