const express = require('express');
const router  = express.Router();
const { getDb } = require('../database');
const { requireAuth } = require('../middleware');
const {
  sendQuoteNotification,
  sendQuoteConfirmation,
} = require('../mailer');

// POST /api/quotes — Public: submit quote request
router.post('/', async (req, res) => {
  const { name, company, email, phone, subject, message } = req.body;
  if (!name || !email) return res.status(400).json({ error: 'Name and email are required' });

  // 1. Save to database
  const db = getDb();
  const result = db.exec2(
    'INSERT INTO quotes (name, company, email, phone, subject, message) VALUES (?, ?, ?, ?, ?, ?)',
    [name, company || '', email, phone || '', subject || '', message || '']
  );

  // 2. Send emails (non-blocking)
  const payload = { name, company, email, phone, subject, message };

  Promise.allSettled([
    sendQuoteNotification(payload),
    sendQuoteConfirmation(payload),
  ]).then(results => {
    results.forEach((r, i) => {
      if (r.status === 'rejected') {
        console.error(`⚠️  Quote email ${i === 0 ? 'notification' : 'auto-reply'} failed:`, r.reason?.message);
      }
    });
  });

  res.status(201).json({
    success: true,
    id: result.lastInsertRowid,
    message: 'Your quote request has been received. We will respond within 2 business days.',
  });
});

// GET /api/quotes — Admin: list all quotes
router.get('/', requireAuth, (req, res) => {
  res.json(getDb().query('SELECT * FROM quotes ORDER BY created_at DESC'));
});

// PATCH /api/quotes/:id/status — Admin
router.patch('/:id/status', requireAuth, (req, res) => {
  getDb().exec2('UPDATE quotes SET status = ? WHERE id = ?', [req.body.status, req.params.id]);
  res.json({ success: true });
});

// DELETE /api/quotes/:id — Admin
router.delete('/:id', requireAuth, (req, res) => {
  getDb().exec2('DELETE FROM quotes WHERE id = ?', [req.params.id]);
  res.json({ success: true });
});

module.exports = router;
