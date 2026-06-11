export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { password } = req.body;
  const adminPassword = process.env.ADMIN_PASSWORD;

  if (!adminPassword) {
    // If user hasn't set the password in Vercel yet, we allow entry so they aren't locked out,
    // but we notify them to set it up.
    return res.status(200).json({ success: true, warning: 'ADMIN_PASSWORD not set in Vercel. Open access granted.' });
  }

  if (password === adminPassword) {
    return res.status(200).json({ success: true });
  } else {
    return res.status(401).json({ error: 'Incorrect password' });
  }
}
