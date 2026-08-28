const express = require('express');
const router  = express.Router();
const { getDb } = require('../database');
const { requireAuth } = require('../middleware');

// GET /api/products — Public
router.get('/', (req, res) => {
  res.json(getDb().query('SELECT * FROM products WHERE active = 1 ORDER BY id ASC'));
});

// GET /api/products/all — Admin
router.get('/all', requireAuth, (req, res) => {
  res.json(getDb().query('SELECT * FROM products ORDER BY id ASC'));
});

// POST /api/products — Admin
router.post('/', requireAuth, (req, res) => {
  const { name, category, description, tolerance } = req.body;
  if (!name) return res.status(400).json({ error: 'Product name is required' });
  const result = getDb().exec2(
    'INSERT INTO products (name, category, description, tolerance) VALUES (?, ?, ?, ?)',
    [name, category || '', description || '', tolerance || '']
  );
  res.status(201).json({ success: true, id: result.lastInsertRowid });
});

// PUT /api/products/:id — Admin
router.put('/:id', requireAuth, (req, res) => {
  const { name, category, description, tolerance, active } = req.body;
  getDb().exec2(
    'UPDATE products SET name=?, category=?, description=?, tolerance=?, active=? WHERE id=?',
    [name, category, description, tolerance, active ?? 1, req.params.id]
  );
  res.json({ success: true });
});

// DELETE /api/products/:id — Admin
router.delete('/:id', requireAuth, (req, res) => {
  getDb().exec2('DELETE FROM products WHERE id = ?', [req.params.id]);
  res.json({ success: true });
});

module.exports = router;
