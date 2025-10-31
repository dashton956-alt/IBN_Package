# GitHub Workflows Setup Guide (Fixed Version)

## 🎯 Overview

Two production-ready workflows with **valid JSON** and proper GitHub node configurations:

1. **github-n8n-sync-v2-fixed.json** - Auto-sync workflows from GitHub to n8n
2. **github-ai-pr-review-gemini.json** - AI code review using Google Gemini

---

## 🔧 Prerequisites

### Required n8n Credentials

#### 1. GitHub OAuth2 (for Triggers)
- Node: `n8n-nodes-base.githubTrigger`
- Type: OAuth2
- Steps:
  1. Go to GitHub → Settings → Developer settings → OAuth Apps
  2. Create new OAuth App
  3. Authorization URL: `https://github.com/login/oauth/authorize`
  4. Access Token URL: `https://github.com/login/oauth/access_token`
  5. Scopes: `repo`, `read:org`, `workflow`
  6. Add to n8n credentials

#### 2. GitHub API (for Actions)
- Node: `n8n-nodes-base.github`
- Type: Personal Access Token
- Steps:
  1. GitHub → Settings → Developer settings → Personal access tokens
  2. Generate new token (classic)
  3. Scopes: `repo`, `read:org`, `workflow`, `write:discussion`
  4. Save token to n8n credentials

#### 3. Google Gemini OAuth2 (for AI Review)
- Node: `n8n-nodes-base.googleGemini`
- Type: OAuth2
- Steps:
  1. Go to Google Cloud Console
  2. Enable Gemini API
  3. Create OAuth 2.0 credentials
  4. Add to n8n credentials

---

## 📥 Import Instructions

### Step 1: Import Workflows

```bash
# Import GitHub Sync Workflow
curl -X POST http://localhost:5678/api/v1/workflows/import \
  -H "Content-Type: application/json" \
  -d @github-n8n-sync-v2-fixed.json

# Import AI PR Review Workflow
curl -X POST http://localhost:5678/api/v1/workflows/import \
  -H "Content-Type: application/json" \
  -d @github-ai-pr-review-gemini.json
```

Or import via n8n UI:
1. Open n8n
2. Click "+" → Import from File
3. Select workflow JSON file
4. Click "Import"

### Step 2: Configure Credentials

For **each workflow**, update these credential IDs:

#### GitHub Sync Workflow
- `YOUR_GITHUB_OAUTH_ID` → Your GitHub OAuth2 credential ID
- `YOUR_GITHUB_API_ID` → Your GitHub API credential ID

#### AI PR Review Workflow
- `YOUR_GITHUB_OAUTH_ID` → Your GitHub OAuth2 credential ID
- `YOUR_GITHUB_API_ID` → Your GitHub API credential ID
- `YOUR_GEMINI_OAUTH_ID` → Your Google Gemini OAuth2 credential ID

**How to find credential IDs:**
1. Go to n8n → Credentials
2. Click on your credential
3. ID is in the URL: `/credentials/{ID}`

### Step 3: Configure Webhook URLs

The workflows use these webhook IDs:
- **Sync Workflow**: `github-workflow-sync-v2`
- **AI Review**: `github-ai-pr-review-gemini`

Webhook URLs will be:
- `https://your-n8n-domain.com/webhook/github-workflow-sync-v2`
- `https://your-n8n-domain.com/webhook/github-ai-pr-review-gemini`

### Step 4: GitHub Repository Setup

1. Go to your GitHub repository → Settings → Webhooks
2. Click "Add webhook"

**For Workflow Sync:**
- Payload URL: `https://your-n8n-domain.com/webhook/github-workflow-sync-v2`
- Content type: `application/json`
- Events: Select "Pushes"
- Active: ✅

**For AI PR Review:**
- Payload URL: `https://your-n8n-domain.com/webhook/github-ai-pr-review-gemini`
- Content type: `application/json`
- Events: Select "Pull requests"
- Active: ✅

---

## 🔍 GitHub Node Configuration Issues - FIXED

### Common Problems (Now Resolved)

#### ❌ Problem 1: "Not pulling any GitHub users or repos"
**Cause:** Missing or incorrect credential configuration

**Fix Applied:**
- All GitHub nodes now use proper credential references
- OAuth2 for triggers (webhooks)
- API token for actions (creating comments, getting files)

**Verify in n8n:**
1. Open workflow
2. Click on GitHub node
3. Click "Credentials" dropdown
4. Select your configured credential
5. Click "Test" button
6. Should see: "Connection successful"

#### ❌ Problem 2: "JSON errors" preventing import
**Cause:** Invalid control characters in embedded JavaScript code

**Fix Applied:**
- All JavaScript code properly escaped on single lines
- No literal newlines in JSON strings
- All code validated with `python3 -m json.tool`

#### ❌ Problem 3: GitHub trigger not firing
**Cause:** Wrong authentication type or missing webhook setup

**Fix Applied:**
- GitHub triggers use OAuth2 authentication
- Webhook IDs are unique and descriptive
- Proper event configuration (`push` or `pull_request`)

---

## 🧪 Testing

### Test Workflow Sync
1. Make a change to a `.json` workflow file
2. Commit and push to GitHub
3. Check n8n executions
4. Should see workflow imported

### Test AI PR Review
1. Create a PR with workflow changes
2. Open the PR on GitHub
3. Wait 10-30 seconds
4. Should see Gemini's review comment

### Debug Mode
Enable in each workflow:
1. Workflow → Settings
2. Enable "Save Execution Progress"
3. Set "Save Data On Error" to "All"
4. Check executions for detailed logs

---

## 📊 Node Configuration Details

### GitHub Trigger Node
```json
{
  "type": "n8n-nodes-base.githubTrigger",
  "parameters": {
    "events": ["push"],  // or ["pull_request"]
    "authentication": "oAuth2"
  },
  "credentials": {
    "githubOAuth2Api": {
      "id": "YOUR_ID"
    }
  }
}
```

### GitHub Action Node
```json
{
  "type": "n8n-nodes-base.github",
  "parameters": {
    "resource": "file",  // or "issue"
    "operation": "get",  // or "list", "createComment"
    "owner": "={{ $json.owner }}",
    "repository": "={{ $json.repo_name }}"
  },
  "credentials": {
    "githubApi": {
      "id": "YOUR_ID"
    }
  }
}
```

### Google Gemini Node
```json
{
  "type": "n8n-nodes-base.googleGemini",
  "parameters": {
    "model": "gemini-1.5-pro",
    "prompt": "={{ $json.review_prompt }}",
    "options": {
      "temperature": 0.3,
      "maxOutputTokens": 4096
    }
  },
  "credentials": {
    "googleGeminiOAuth2Api": {
      "id": "YOUR_ID"
    }
  }
}
```

---

## 🚨 Troubleshooting

### Issue: "Credentials not found"
**Solution:** Update credential IDs in workflow JSON before importing

### Issue: "GitHub trigger not activating"
**Solution:** 
1. Check webhook is configured in GitHub repo
2. Verify webhook URL matches n8n webhook
3. Check OAuth2 scopes include `repo`

### Issue: "Gemini API error"
**Solution:**
1. Verify Gemini API is enabled in Google Cloud
2. Check OAuth2 credentials are valid
3. Verify billing is enabled (Gemini requires billing)

### Issue: "Cannot read files from PR"
**Solution:**
1. Ensure GitHub API token has `repo` scope
2. Check repository is not private (or token has private access)
3. Verify PR number is valid

---

## 📝 Key Differences from v1/v2

| Feature | Old Versions | Fixed Versions |
|---------|-------------|----------------|
| JSON Validity | ❌ Invalid control chars | ✅ Fully valid JSON |
| GitHub Auth | ⚠️ Mixed/unclear | ✅ OAuth2 + API clear |
| AI Model | OpenAI | ✅ Google Gemini |
| Credential Config | ❌ Hardcoded/missing | ✅ Placeholder IDs |
| Import Ready | ❌ Errors | ✅ Imports cleanly |

---

## 🎓 Best Practices

1. **Use OAuth2 for Triggers**: More secure than webhooks with tokens
2. **Use API Tokens for Actions**: Simpler for programmatic access
3. **Test in Development**: Use a test repo first
4. **Monitor Executions**: Check n8n execution logs regularly
5. **Rate Limits**: GitHub API has rate limits (5000/hour authenticated)
6. **Gemini Costs**: Monitor Google Cloud billing for API usage

---

## 📚 Additional Resources

- [n8n GitHub Nodes Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.github/)
- [GitHub Webhook Events](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [n8n Credentials Guide](https://docs.n8n.io/credentials/)

---

**Version:** Fixed v3  
**Date:** 2025-10-31  
**Status:** ✅ Production Ready
