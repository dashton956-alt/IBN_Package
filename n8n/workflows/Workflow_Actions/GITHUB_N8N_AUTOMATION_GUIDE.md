# GitHub ↔ n8n Workflow Automation - Complete Guide

## 📋 Overview

This automation solution provides:
1. **Automatic workflow sync** from GitHub to n8n on merge
2. **AI-powered PR reviews** using Claude for workflow quality analysis
3. **Modular n8n workflows** that can be triggered from GitHub Actions
4. **Comprehensive error handling** and reporting

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
│                  (workflows/*.json files)                │
└────────────┬───────────────────────────┬─────────────────┘
             │                           │
    Push to master                  Pull Request Created
             │                           │
             ↓                           ↓
    ┌────────────────┐          ┌──────────────────┐
    │ GitHub Actions │          │  GitHub Actions  │
    │  Workflow Sync │          │   AI PR Review   │
    └────────┬───────┘          └────────┬─────────┘
             │                           │
             │ Webhook POST              │ Webhook POST
             ↓                           ↓
    ┌────────────────┐          ┌──────────────────┐
    │      n8n       │          │       n8n        │
    │  Sync Workflow │          │  Review Workflow │
    └────────┬───────┘          └────────┬─────────┘
             │                           │
             │                           ↓
             │                  ┌──────────────────┐
             │                  │  Claude AI API   │
             │                  └────────┬─────────┘
             │                           │
             ↓                           ↓
    ┌─────────────────────────────────────────┐
    │         n8n Instance (Updated)           │
    │      + GitHub PR Comment Posted          │
    └─────────────────────────────────────────┘
```

## 🚀 Setup Instructions

### Step 1: Import n8n Workflows

1. **Import Workflow 1** (GitHub Sync):
   ```bash
   # In n8n UI:
   # - Click "Workflows" → "Import from File"
   # - Select n8n-github-sync-workflow.json
   # - Activate the workflow
   ```

2. **Import Workflow 2** (AI PR Review):
   ```bash
   # In n8n UI:
   # - Click "Workflows" → "Import from File"
   # - Select n8n-ai-pr-review-workflow.json
   # - Activate the workflow
   ```

3. **Get Webhook URLs**:
   - Open each workflow in n8n
   - Click on the "Webhook Trigger" node
   - Copy the "Production URL"
   - URLs will look like:
     - `https://your-n8n.com/webhook/github-workflow-sync`
     - `https://your-n8n.com/webhook/ai-pr-review`

### Step 2: Configure GitHub Repository

1. **Create GitHub Secrets**:
   ```bash
   # In your GitHub repo: Settings → Secrets and variables → Actions
   # Add the following secrets:
   ```

   | Secret Name | Description | Example |
   |-------------|-------------|---------|
   | `N8N_WEBHOOK_URL` | Base n8n webhook URL | `https://n8n.example.com` |
   | `N8N_API_KEY` | n8n API key | `n8n_api_xxxxx...` |
   | `N8N_BASE_URL` | n8n instance URL | `https://n8n.example.com` |
   | `ANTHROPIC_API_KEY` | Claude API key | `sk-ant-xxxxx...` |

   **How to get n8n API Key:**
   ```
   1. In n8n, go to Settings → API
   2. Click "Create API Key"
   3. Copy the generated key
   ```

   **How to get Anthropic API Key:**
   ```
   1. Go to https://console.anthropic.com
   2. Sign up or log in
   3. Go to API Keys
   4. Create a new key
   ```

2. **Add GitHub Actions Workflows**:
   ```bash
   # In your repo, create .github/workflows/ directory
   mkdir -p .github/workflows
   
   # Copy the workflow files:
   cp sync-n8n-workflows.yml .github/workflows/
   cp ai-pr-review.yml .github/workflows/
   
   # Commit and push
   git add .github/workflows/
   git commit -m "Add n8n workflow automation"
   git push
   ```

### Step 3: Organize Your Workflow Files

Create a folder structure for your n8n workflows:

```
your-repo/
├── .github/
│   └── workflows/
│       ├── sync-n8n-workflows.yml
│       └── ai-pr-review.yml
├── workflows/
│   ├── automation/
│   │   ├── email-automation.json
│   │   └── slack-notifications.json
│   ├── integrations/
│   │   ├── github-integration.json
│   │   └── jira-sync.json
│   └── data-processing/
│       ├── csv-processor.json
│       └── api-aggregator.json
└── README.md
```

### Step 4: Test the Setup

1. **Test Workflow Sync**:
   ```bash
   # Create a test workflow file
   cat > workflows/test-workflow.json <<EOF
   {
     "name": "Test Workflow",
     "nodes": [
       {
         "parameters": {},
         "name": "Start",
         "type": "n8n-nodes-base.start",
         "typeVersion": 1,
         "position": [250, 300]
       }
     ],
     "connections": {},
     "settings": {},
     "tags": [{"name": "test"}]
   }
   EOF
   
   # Commit and push to master
   git add workflows/test-workflow.json
   git commit -m "Add test workflow"
   git push origin master
   
   # Check GitHub Actions tab for sync status
   # Check n8n for the imported workflow
   ```

2. **Test AI PR Review**:
   ```bash
   # Create a new branch
   git checkout -b test-pr
   
   # Modify a workflow
   echo '  "description": "Updated workflow"' >> workflows/test-workflow.json
   
   # Create PR
   git add workflows/test-workflow.json
   git commit -m "Update test workflow"
   git push origin test-pr
   
   # Create PR in GitHub UI
   # AI review should trigger automatically
   ```

## 📖 Usage Guide

### Automatic Workflow Sync

**Trigger:** Push to `master` or `main` branch

**Process:**
1. GitHub Actions detects `.json` files in `workflows/` directory
2. Sends webhook to n8n sync workflow
3. n8n fetches repository tree from GitHub
4. Filters for workflow files
5. Validates JSON structure
6. Checks if workflow exists in n8n (by name)
7. Creates new or updates existing workflows
8. Preserves folder structure using tags
9. Returns sync report to GitHub Actions
10. Posts comment on commit with results

**Example Commit Comment:**
```markdown
## 🔄 n8n Workflow Sync Complete

**Status:** ✅ All workflows synced successfully

**Summary:**
- Total: 3
- Successful: 3
- Failed: 0

### ✅ Successfully Synced
- `workflows/automation/email-automation.json` → **automation/Email Automation** (update)
- `workflows/integrations/github-integration.json` → **integrations/GitHub Integration** (create)
- `workflows/data-processing/csv-processor.json` → **data-processing/CSV Processor** (update)

**Statistics:**
- Total nodes: 47
- Created: 1
- Updated: 2
- Tags: automation, integrations, data-processing, github-sync
```

### AI PR Review

**Trigger:** Pull request opened/updated with workflow changes

**Process:**
1. GitHub Actions detects `.json` changes in PR
2. Posts "Review in progress" comment
3. Sends PR data to n8n AI review workflow
4. n8n fetches PR files and diffs from GitHub
5. Builds comprehensive context with file changes
6. Sends analysis prompt to Claude AI
7. Claude analyzes:
   - Code quality and structure
   - Risk assessment
   - Security considerations
   - Performance implications
   - Best practices compliance
8. Posts detailed review comment on PR
9. Submits formal review (APPROVE/REQUEST_CHANGES/COMMENT)
10. Adds labels based on risk and quality

**Example AI Review Comment:**
```markdown
## 🤖 AI Workflow Review

### 1. Summary
This PR introduces a new Slack notification workflow that triggers on error events from other workflows. The implementation follows n8n best practices with proper error handling and conditional logic.

### 2. Risk Analysis
**Risk Level:** Low

- No breaking changes to existing workflows
- Isolated functionality with clear boundaries
- Proper error handling implemented
- No security concerns identified

### 3. Code Quality Assessment
**Score:** 8/10

**Strengths:**
- Well-structured node organization
- Descriptive node names and annotations
- Proper use of expressions for dynamic data
- Includes error handling nodes

**Areas for Improvement:**
- Consider adding retry logic for Slack API calls
- Some expressions could be simplified
- Missing workflow description field

### 4. Specific Observations
✅ **Good patterns:**
- Use of IF node for conditional routing
- Centralized error handling
- Environment variable usage for sensitive data

⚠️ **Potential issues:**
- Hardcoded channel ID in line 47 (consider using variable)
- No timeout configured for HTTP request node
- Missing rate limit handling

### 5. Recommendations
1. Add workflow-level description
2. Replace hardcoded values with variables
3. Add timeout to HTTP Request nodes (suggest 30s)
4. Consider adding exponential backoff for retries
5. Add logging for debugging

### 6. Testing Checklist
- [ ] Test with various error message formats
- [ ] Verify Slack message formatting
- [ ] Test error handling paths
- [ ] Verify rate limit behavior
- [ ] Test with missing/invalid data

### 7. Overall Assessment
**Approval Status:** APPROVE

This is a solid implementation that follows best practices. The suggested improvements are minor and don't block approval. The workflow is production-ready with the current implementation.

**Key Action Items:**
1. Address hardcoded values (optional)
2. Add timeout configurations (recommended)
3. Test thoroughly before production deployment

---
*Reviewed by Claude AI | 2025-01-01T12:00:00Z*
*Review ID: exec_abc123*
```

## 🔧 Configuration Options

### Workflow Sync Configuration

**In GitHub Actions** (`sync-n8n-workflows.yml`):

```yaml
env:
  N8N_WEBHOOK_URL: ${{ secrets.N8N_WEBHOOK_URL }}
  N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
  N8N_BASE_URL: ${{ secrets.N8N_BASE_URL }}

workflow_dispatch:
  inputs:
    dry_run:
      description: 'Dry run mode (no actual import)'
      type: boolean
      default: false
    workflow_path:
      description: 'Path to workflow files'
      type: string
      default: 'workflows'
```

**Manual Trigger:**
```bash
# In GitHub UI: Actions → Sync Workflows to n8n → Run workflow
# Set inputs:
# - dry_run: true (to test without importing)
# - workflow_path: "custom/path" (for different directory)
```

### AI Review Configuration

**In GitHub Actions** (`ai-pr-review.yml`):

```yaml
workflow_dispatch:
  inputs:
    pr_number:
      description: 'PR number to review'
      type: number
    auto_comment:
      description: 'Automatically post review comment'
      type: boolean
      default: true
```

**In n8n Workflow Payload:**

```json
{
  "auto_comment": true,        // Post review automatically
  "review_depth": "standard"   // Options: minimal, standard, deep
}
```

**Review Depth Levels:**
- `minimal`: Quick summary and risk assessment
- `standard`: Comprehensive review (default)
- `deep`: Detailed analysis including security audit

## 🎨 Customization

### Custom Folder Structure Mapping

The sync workflow uses folder paths as tags. To customize:

```javascript
// In "Validate & Enrich Workflow" node
// Modify this section:
const tags = pathParts
  .filter(part => part !== workflowPath && part !== fileName)
  .map(part => part.replace(/[_-]/g, ' '));

// Example custom mapping:
const tagMapping = {
  'automation': 'automation',
  'integrations': 'integration',
  'data': 'data-processing'
};
const tags = pathParts.map(part => tagMapping[part] || part);
```

### Custom AI Prompts

To customize the AI review prompt:

```javascript
// In "Build Analysis Context" node
// Modify the analysisPrompt variable
const analysisPrompt = `
Your custom prompt here...

Focus areas:
- Security assessment
- Performance optimization
- Error handling
- Best practices

Output format:
...
`;
```

### Adding Custom Notifications

**Slack Integration:**

```yaml
# In sync-n8n-workflows.yml, add:
- name: Notify Slack
  if: always()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK_URL }} \
      -H 'Content-Type: application/json' \
      -d '{
        "text": "Workflow sync ${{ job.status }}",
        "blocks": [{
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "Synced ${{ steps.results.outputs.successful }} workflows"
          }
        }]
      }'
```

**Email Notification:**

```yaml
- name: Send Email
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Workflow Sync Failed
    body: Check ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
    to: devops@example.com
    from: GitHub Actions
```

## 🔍 Troubleshooting

### Common Issues

**1. Sync fails with 401 Unauthorized**
```
Problem: Invalid n8n API key
Solution: 
- Verify N8N_API_KEY in GitHub secrets
- Regenerate API key in n8n Settings → API
- Ensure key has proper permissions
```

**2. Workflows not appearing in n8n**
```
Problem: Webhook not accessible or incorrect URL
Solution:
- Verify N8N_WEBHOOK_URL is correct
- Check n8n instance is publicly accessible
- Test webhook manually:
  curl -X POST https://your-n8n.com/webhook/github-workflow-sync \
    -H "Content-Type: application/json" \
    -d '{"repository":"test/repo","ref":"refs/heads/master"}'
```

**3. AI review not posting comments**
```
Problem: Missing GitHub permissions or Anthropic API key
Solution:
- Verify GITHUB_TOKEN has write permissions
- Check ANTHROPIC_API_KEY is valid
- Ensure "auto_comment": true in payload
```

**4. Invalid JSON errors**
```
Problem: Workflow files have syntax errors
Solution:
- Validate JSON locally:
  python -m json.tool workflow.json
- Use JSON linter in IDE
- Check for trailing commas, missing quotes
```

### Debug Mode

**Enable verbose logging:**

```yaml
# In GitHub Actions workflow, add:
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

**View n8n execution logs:**
```
1. Open n8n UI
2. Go to Executions
3. Click on failed execution
4. Review each node's output
5. Check error messages
```

### Testing Webhooks Locally

**Using curl:**
```bash
# Test sync webhook
curl -X POST http://localhost:5678/webhook/github-workflow-sync \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "owner/repo",
    "ref": "refs/heads/master",
    "sha": "abc123",
    "github_token": "ghp_xxx",
    "n8n_api_key": "n8n_api_xxx",
    "n8n_base_url": "http://localhost:5678"
  }'

# Test AI review webhook
curl -X POST http://localhost:5678/webhook/ai-pr-review \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "owner/repo",
    "pull_request": {
      "number": 1,
      "title": "Test PR",
      "body": "Test description"
    },
    "github_token": "ghp_xxx",
    "anthropic_api_key": "sk-ant-xxx"
  }'
```

## 📊 Monitoring & Analytics

### GitHub Actions Insights

```bash
# View workflow runs
# GitHub UI: Actions tab → Select workflow → View runs

# Metrics to track:
# - Success rate
# - Average execution time
# - Most common failures
# - Workflows synced per run
```

### n8n Execution Data

```bash
# In n8n UI:
# 1. Go to Executions
# 2. Filter by workflow
# 3. View success/failure rates
# 4. Export execution data for analysis
```

### Custom Analytics

**Add to GitHub Actions:**

```yaml
- name: Log Analytics
  run: |
    curl -X POST https://your-analytics.com/api/events \
      -d '{
        "event": "workflow_sync",
        "status": "${{ job.status }}",
        "workflows": ${{ steps.results.outputs.successful }},
        "repository": "${{ github.repository }}",
        "timestamp": "${{ github.event.head_commit.timestamp }}"
      }'
```

## 🔒 Security Best Practices

1. **API Key Rotation:**
   ```bash
   # Rotate keys every 90 days
   # Update in GitHub secrets immediately
   ```

2. **Webhook Authentication:**
   ```javascript
   // Add in n8n webhook node:
   if (headers['x-github-signature']) {
     // Verify HMAC signature
     const signature = crypto
       .createHmac('sha256', secret)
       .update(JSON.stringify(body))
       .digest('hex');
     
     if (signature !== headers['x-github-signature']) {
       throw new Error('Invalid signature');
     }
   }
   ```

3. **Least Privilege:**
   ```
   - Use separate API keys for different workflows
   - Limit GitHub token scope to required permissions
   - Restrict n8n API key permissions
   ```

4. **Audit Logging:**
   ```javascript
   // Log all sync operations
   console.log({
     event: 'workflow_sync',
     user: $json.actor,
     workflows: $json.workflows,
     timestamp: new Date().toISOString()
   });
   ```

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [n8n API Reference](https://docs.n8n.io/api/)

## 🤝 Contributing

To extend this automation:

1. Fork the repository
2. Create a feature branch
3. Make changes to workflows or GitHub Actions
4. Test thoroughly
5. Submit pull request with:
   - Description of changes
   - Test results
   - Documentation updates

## 📝 License

MIT License - Use freely in your projects

---

**Support:** For issues or questions, open a GitHub issue or discussion.
