const express = require('express');
const router  = express.Router();
const { getDb } = require('../database');
const { requireAuth } = require('../middleware');
const {
  sendContactNotification,
  sendContactConfirmation,
} = require('../mailer');

// POST /api/contacts — Public: submit contact form
router.post('/', async (req, res) => {
  const { name, company, email, phone, subject, message } = req.body;
  if (!name || !email) return res.status(400).json({ error: 'Name and email are required' });

  // 1. Save to database
  const db = getDb();
  const result = db.exec2(
    'INSERT INTO contacts (name, company, email, phone, subject, message) VALUES (?, ?, ?, ?, ?, ?)',
    [name, company || '', email, phone || '', subject || '', message || '']
  );

  // 2. Send emails (non-blocking — don't fail the response if mail fails)
  const payload = { name, company, email, phone, subject, message };

  Promise.allSettled([
    sendContactNotification(payload),
    sendContactConfirmation(payload),
  ]).then(results => {
    results.forEach((r, i) => {
      if (r.status === 'rejected') {
        console.error(`⚠️  Contact email ${i === 0 ? 'notification' : 'auto-reply'} failed:`, r.reason?.message);
      }
    });
  });

  res.status(201).json({
    success: true,
    id: result.lastInsertRowid,
    message: 'Your message has been received. We will respond within one business day.',
  });
});

// GET /api/contacts — Admin: list all contacts
router.get('/', requireAuth, (req, res) => {
  res.json(getDb().query('SELECT * FROM contacts ORDER BY created_at DESC'));
});

// PATCH /api/contacts/:id/status — Admin
router.patch('/:id/status', requireAuth, (req, res) => {
  getDb().exec2('UPDATE contacts SET status = ? WHERE id = ?', [req.body.status, req.params.id]);
  res.json({ success: true });
});

// DELETE /api/contacts/:id — Admin
router.delete('/:id', requireAuth, (req, res) => {
  getDb().exec2('DELETE FROM contacts WHERE id = ?', [req.params.id]);
  res.json({ success: true });
});

module.exports = router;
