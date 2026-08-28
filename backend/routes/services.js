const express = require('express');
const router  = express.Router();
const { getDb } = require('../database');
const { requireAuth } = require('../middleware');

// GET /api/services — Public
router.get('/', (req, res) => {
  res.json(getDb().query('SELECT * FROM services WHERE active = 1 ORDER BY id ASC'));
});

// GET /api/services/all — Admin
router.get('/all', requireAuth, (req, res) => {
  res.json(getDb().query('SELECT * FROM services ORDER BY id ASC'));
});

// POST /api/services — Admin
router.post('/', requireAuth, (req, res) => {
  const { number, title, description } = req.body;
  if (!title) return res.status(400).json({ error: 'Service title is required' });
  const result = getDb().exec2(
    'INSERT INTO services (number, title, description) VALUES (?, ?, ?)',
    [number || '', title, description || '']
  );
  res.status(201).json({ success: true, id: result.lastInsertRowid });
});

// PUT /api/services/:id — Admin
router.put('/:id', requireAuth, (req, res) => {
  const { number, title, description, active } = req.body;
  getDb().exec2(
    'UPDATE services SET number=?, title=?, description=?, active=? WHERE id=?',
    [number, title, description, active ?? 1, req.params.id]
  );
  res.json({ success: true });
});

// DELETE /api/services/:id — Admin
router.delete('/:id', requireAuth, (req, res) => {
  getDb().exec2('DELETE FROM services WHERE id = ?', [req.params.id]);
  res.json({ success: true });
});

module.exports = router;
