export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { profile, keywords } = req.body;

  if (!profile || !keywords || !Array.isArray(keywords)) {
    return res.status(400).json({ error: 'Invalid data format' });
  }

  const githubToken = process.env.GITHUB_TOKEN;
  if (!githubToken) {
    return res.status(500).json({ error: 'Server configuration error: GITHUB_TOKEN missing' });
  }

  const repo = 'manishbhandaricode/Job-tracker';
  const path = 'preferences.json';
  const apiUrl = `https://api.github.com/repos/${repo}/contents/${path}`;

  try {
    // 1. Fetch current file to get the SHA (required for updating files in GitHub API)
    const getRes = await fetch(apiUrl, {
      headers: {
        Authorization: `Bearer ${githubToken}`,
        Accept: 'application/vnd.github.v3+json'
      }
    });

    if (!getRes.ok && getRes.status !== 404) {
      throw new Error(`Failed to fetch file SHA: ${getRes.statusText}`);
    }

    let sha = undefined;
    if (getRes.ok) {
      const getData = await getRes.json();
      sha = getData.sha;
    }

    // 2. Prepare new content
    const newContent = JSON.stringify({ profile, keywords }, null, 2);
    // Base64 encode the content (Node.js Buffer)
    const encodedContent = Buffer.from(newContent).toString('base64');

    // 3. Update the file
    const updateRes = await fetch(apiUrl, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${githubToken}`,
        Accept: 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: 'Update preferences via Web Dashboard',
        content: encodedContent,
        sha: sha,
        branch: 'main'
      })
    });

    if (!updateRes.ok) {
      const errorData = await updateRes.json();
      throw new Error(`GitHub API Error: ${errorData.message}`);
    }

    res.status(200).json({ success: true, message: 'Preferences updated successfully!' });
  } catch (error) {
    console.error('Error updating preferences:', error);
    res.status(500).json({ error: error.message || 'Failed to update preferences on GitHub' });
  }
}
