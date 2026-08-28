const express = require('express');
const router  = express.Router();
const { getDb } = require('../database');
const { requireAuth } = require('../middleware');

// POST /api/newsletter — Public
router.post('/', (req, res) => {
  const { email } = req.body;
  if (!email) return res.status(400).json({ error: 'Email is required' });
  const db = getDb();
  const existing = db.queryOne('SELECT id FROM newsletter WHERE email = ?', [email]);
  if (existing) return res.status(409).json({ error: 'This email is already subscribed.' });
  db.exec2('INSERT INTO newsletter (email) VALUES (?)', [email]);
  res.status(201).json({ success: true, message: 'Subscribed successfully!' });
});

// GET /api/newsletter — Admin
router.get('/', requireAuth, (req, res) => {
  res.json(getDb().query('SELECT * FROM newsletter ORDER BY subscribed_at DESC'));
});

// DELETE /api/newsletter/:id — Admin
router.delete('/:id', requireAuth, (req, res) => {
  getDb().exec2('DELETE FROM newsletter WHERE id = ?', [req.params.id]);
  res.json({ success: true });
});

module.exports = router;
