const express = require('express');
const router  = express.Router();
const { getDb } = require('../database');
const { requireAuth } = require('../middleware');
const { sendNewsletterBroadcast } = require('../mailer');

// ── Subscribers ──────────────────────────────────────────────

// POST /api/newsletter — Public / Admin: Add Subscriber
router.post('/', (req, res) => {
  const { email } = req.body;
  if (!email) return res.status(400).json({ error: 'Email is required' });
  const db = getDb();
  const existing = db.queryOne('SELECT id FROM newsletter WHERE email = ?', [email]);
  if (existing) return res.status(409).json({ error: 'This email is already subscribed.' });
  db.exec2('INSERT INTO newsletter (email) VALUES (?)', [email]);
  res.status(201).json({ success: true, message: 'Subscribed successfully!' });
});

// GET /api/newsletter — Admin: List Subscribers
router.get('/', requireAuth, (req, res) => {
  res.json(getDb().query('SELECT * FROM newsletter ORDER BY subscribed_at DESC'));
});

// PUT /api/newsletter/:id — Admin: Edit Subscriber Email
router.put('/:id', requireAuth, (req, res) => {
  const { email } = req.body;
  if (!email) return res.status(400).json({ error: 'Email is required' });
  const db = getDb();
  const existing = db.queryOne('SELECT id FROM newsletter WHERE email = ? AND id != ?', [email, req.params.id]);
  if (existing) return res.status(409).json({ error: 'This email is already subscribed.' });
  
  db.exec2('UPDATE newsletter SET email = ? WHERE id = ?', [email, req.params.id]);
  res.json({ success: true });
});

// DELETE /api/newsletter/:id — Admin: Delete Subscriber
router.delete('/:id', requireAuth, (req, res) => {
  getDb().exec2('DELETE FROM newsletter WHERE id = ?', [req.params.id]);
  res.json({ success: true });
});

// GET /api/newsletter/public — Public: List newsletters for website display
router.get('/public', (req, res) => {
  const db = getDb();
  res.json(db.query('SELECT * FROM newsletters ORDER BY created_at DESC'));
});

// GET /api/newsletter/campaigns — Admin: List Newsletters
router.get('/campaigns', requireAuth, (req, res) => {
  res.json(getDb().query('SELECT * FROM newsletters ORDER BY created_at DESC'));
});

// POST /api/newsletter/campaigns — Admin: Add / Create Newsletter
router.post('/campaigns', requireAuth, (req, res) => {
  const { title, subject, content } = req.body;
  if (!title || !subject || !content) {
    return res.status(400).json({ error: 'Title, Subject, and Content are required.' });
  }
  const db = getDb();
  const result = db.exec2(
    'INSERT INTO newsletters (title, subject, content, status) VALUES (?, ?, ?, ?)',
    [title, subject, content, 'draft']
  );
  res.status(201).json({ success: true, id: result.lastInsertRowid, message: 'Newsletter created as draft.' });
});

// PUT /api/newsletter/campaigns/:id — Admin: Edit Newsletter
router.put('/campaigns/:id', requireAuth, (req, res) => {
  const { title, subject, content } = req.body;
  if (!title || !subject || !content) {
    return res.status(400).json({ error: 'Title, Subject, and Content are required.' });
  }
  const db = getDb();
  db.exec2(
    'UPDATE newsletters SET title = ?, subject = ?, content = ? WHERE id = ?',
    [title, subject, content, req.params.id]
  );
  res.json({ success: true, message: 'Newsletter updated.' });
});

// DELETE /api/newsletter/campaigns/:id — Admin: Delete Newsletter
router.delete('/campaigns/:id', requireAuth, (req, res) => {
  getDb().exec2('DELETE FROM newsletters WHERE id = ?', [req.params.id]);
  res.json({ success: true });
});

// POST /api/newsletter/campaigns/:id/send — Admin: Send / Broadcast Newsletter
router.post('/campaigns/:id/send', requireAuth, async (req, res) => {
  const db = getDb();
  const campaign = db.queryOne('SELECT * FROM newsletters WHERE id = ?', [req.params.id]);
  if (!campaign) return res.status(404).json({ error: 'Newsletter not found.' });

  const subscribers = db.query('SELECT email FROM newsletter');
  const recipientEmails = subscribers.map(s => s.email);

  if (!recipientEmails.length) {
    return res.status(400).json({ error: 'No active subscribers found to receive this newsletter.' });
  }

  const { sentCount } = await sendNewsletterBroadcast({
    title: campaign.title,
    subject: campaign.subject,
    content: campaign.content,
    recipients: recipientEmails,
  });

  const now = new Date().toISOString();
  db.exec2("UPDATE newsletters SET status = 'sent', sent_at = ? WHERE id = ?", [now, req.params.id]);

  res.json({ success: true, message: `Newsletter broadcast complete. Sent to ${sentCount} subscriber(s).`, sentCount });
});

module.exports = router;
