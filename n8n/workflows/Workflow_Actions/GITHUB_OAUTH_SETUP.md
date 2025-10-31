# GitHub OAuth2 Setup Guide for n8n

This guide will help you set up GitHub OAuth2 authentication in n8n to access private repositories.

## Step 1: Create a GitHub OAuth App

1. **Go to GitHub Settings**:
   - Navigate to: https://github.com/settings/developers
   - Or: Click your profile picture → Settings → Developer settings → OAuth Apps

2. **Click "New OAuth App"** (or "Register a new application")

3. **Fill in the Application Details**:
   ```
   Application name: n8n Workflow Automation
   Homepage URL: http://localhost:5678
   Authorization callback URL: http://localhost:5678/rest/oauth2-credential/callback
   ```
   
   **Important**: If your n8n is on a different URL, replace `http://localhost:5678` with your actual n8n URL.

4. **Click "Register application"**

5. **Save your credentials**:
   - Copy the **Client ID** (you'll need this)
   - Click **"Generate a new client secret"**
   - Copy the **Client Secret** immediately (you won't be able to see it again!)

## Step 2: Configure OAuth2 in n8n

1. **Open n8n** (http://localhost:5678)

2. **Go to Credentials**:
   - Click your profile icon (bottom left)
   - Select **"Credentials"**

3. **Create New Credential**:
   - Click **"+ Add Credential"**
   - Search for **"GitHub OAuth2 API"**
   - Select it

4. **Fill in the OAuth2 Configuration**:
   ```
   Credential Name: GitHub OAuth2 (Private Repos)
   Client ID: [paste your Client ID from GitHub]
   Client Secret: [paste your Client Secret from GitHub]
   ```

5. **Click "Connect my account"**:
   - You'll be redirected to GitHub
   - GitHub will ask for permissions
   - **IMPORTANT**: Make sure to grant access to the repositories you need

6. **Authorize the application**:
   - You'll see a list of permissions the app is requesting
   - Click **"Authorize [your-username]"**

7. **Back in n8n**:
   - You should see "Connection successful" or similar
   - Click **"Save"**

## Step 3: Configure Required Scopes (If Needed)

If you need to update scopes later:

1. Go back to your GitHub OAuth App settings: https://github.com/settings/developers
2. Click on your app name
3. Under "Repository access", ensure you have the right permissions
4. For these workflows, you need:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **read:user** (Read user profile)
   - ✅ **workflow** (Update GitHub Actions workflows)

## Step 4: Use the Credential in Workflows

1. **Import the workflow** (if not already done)

2. **Update each GitHub node**:
   - Open the workflow
   - Click on each GitHub node (trigger or action)
   - Under "Credentials", select your **"GitHub OAuth2 (Private Repos)"** credential
   - Save the workflow

3. **Test the workflow**:
   - Try selecting a repository in a GitHub node
   - You should now see both public AND private repositories!

## Troubleshooting

### Can't see private repos?
- Make sure you selected the **"GitHub OAuth2 API"** credential type (not "GitHub API")
- Check that you authorized the app for the organization/repos you need
- Go to: https://github.com/settings/applications → "Authorized OAuth Apps" → Check your app's access

### "Invalid credentials" error?
- The Client Secret might be wrong - generate a new one in GitHub
- Make sure the callback URL matches exactly (including http/https and port)

### Webhook not triggering?
- After setting up OAuth2, you need to activate the workflow
- GitHub will automatically create a webhook in your repository
- Check repository Settings → Webhooks to verify it was created

### Need to revoke and re-authorize?
1. Go to: https://github.com/settings/applications
2. Find your app under "Authorized OAuth Apps"
3. Click "Revoke"
4. In n8n, reconnect the credential (it will ask you to authorize again)

## Security Notes

- **Never share your Client Secret** - treat it like a password
- **Use HTTPS** in production (don't use http:// for public-facing instances)
- **Rotate secrets periodically** if this is for production use
- **Limit scope** to only what you need (though 'repo' is required for private repos)

## Testing Your Setup

To verify everything works:

1. **Test with GitHub Trigger**:
   - Create a test workflow with just a GitHub Trigger node
   - Select a private repository
   - Make a test commit
   - Check if the workflow executes

2. **Test with GitHub Node**:
   - Add a Manual Trigger + GitHub node (Get File operation)
   - Select a private repository
   - Try to fetch a file
   - If it succeeds, your OAuth is working!

---

## Quick Reference

**GitHub OAuth App Settings**: https://github.com/settings/developers
**Your Authorized Apps**: https://github.com/settings/applications
**n8n Callback URL Format**: `http://YOUR_N8N_URL:PORT/rest/oauth2-credential/callback`

Need help? Check the [n8n community forum](https://community.n8n.io/) or [GitHub OAuth docs](https://docs.github.com/en/developers/apps/building-oauth-apps).
