require('dotenv').config({ path: require('path').join(__dirname, '..', '.env') });

const express    = require('express');
const cors       = require('cors');
const path       = require('path');
const { init }   = require('./database');

const app = express();

// ── Middleware ─────────────────────────────────────────────────
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ── Static Files ──────────────────────────────────────────────
app.use(express.static(path.join(__dirname, '..')));
app.use('/admin', express.static(path.join(__dirname, '..', 'admin')));

// ── API Routes ─────────────────────────────────────────────────
app.use('/api/login',      require('./routes/auth'));
app.use('/api/contacts',   require('./routes/contacts'));
app.use('/api/quotes',     require('./routes/quotes'));
app.use('/api/newsletter', require('./routes/newsletter'));
app.use('/api/products',   require('./routes/products'));
app.use('/api/services',   require('./routes/services'));

// ── Health Check ───────────────────────────────────────────────
app.get('/api/health', (req, res) => res.json({ status: 'ok', time: new Date().toISOString() }));

// ── Root ───────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend.html'));
});

// ── Boot ───────────────────────────────────────────────────────
const PORT = process.env.PORT || 3000;

init().then(() => {
  app.listen(PORT, () => {
    console.log('');
    console.log('┌──────────────────────────────────────────────────────┐');
    console.log('│   HEXACORE PRECISION TECHNOLOGIES                    │');
    console.log('│   Dynamic Backend Server Running                     │');
    console.log('├──────────────────────────────────────────────────────┤');
    console.log(`│   Website  →  http://localhost:${PORT}/frontend.html     │`);
    console.log(`│   Admin    →  http://localhost:${PORT}/admin             │`);
    console.log(`│   API      →  http://localhost:${PORT}/api/health        │`);
    console.log('├──────────────────────────────────────────────────────┤');
    console.log('│   Admin Login:  admin / hexacore2026                 │');
    console.log('└──────────────────────────────────────────────────────┘');
    console.log('');
  });
}).catch(err => {
  console.error('❌ Failed to initialise database:', err);
  process.exit(1);
});
