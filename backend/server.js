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

// ── 301 Permanent Redirects for legacy .html URLs ──────────────
app.get(['/index.html', '/frontend.html'], (req, res) => res.redirect(301, '/'));
app.get('/about.html', (req, res) => res.redirect(301, '/about'));
app.get('/services.html', (req, res) => res.redirect(301, '/services'));
app.get('/service.html', (req, res) => {
  const query = req.url.includes('?') ? req.url.substring(req.url.indexOf('?')) : '';
  res.redirect(301, '/service' + query);
});
app.get(['/products.html', '/product.html'], (req, res) => res.redirect(301, '/products'));
app.get('/contact.html', (req, res) => res.redirect(301, '/contact'));
app.get('/newsletter.html', (req, res) => res.redirect(301, '/about#newsletter-section'));
app.get('/quote.html', (req, res) => res.redirect(301, '/contact'));

// ── Clean Page Routes ─────────────────────────────────────────
app.get('/', (req, res) => res.sendFile(path.join(__dirname, '..', 'index.html')));
app.get('/about', (req, res) => res.sendFile(path.join(__dirname, '..', 'about.html')));
app.get('/services', (req, res) => res.sendFile(path.join(__dirname, '..', 'services.html')));
app.get('/service', (req, res) => res.sendFile(path.join(__dirname, '..', 'service.html')));
app.get('/products', (req, res) => res.sendFile(path.join(__dirname, '..', 'products.html')));
app.get('/contact', (req, res) => res.sendFile(path.join(__dirname, '..', 'contact.html')));

// ── API Routes ─────────────────────────────────────────────────
app.use('/api/login',      require('./routes/auth'));
app.use('/api/contacts',   require('./routes/contacts'));
app.use('/api/quotes',     require('./routes/quotes'));
app.use('/api/newsletter', require('./routes/newsletter'));
app.use('/api/products',   require('./routes/products'));
app.use('/api/services',   require('./routes/services'));

// ── Health Check ───────────────────────────────────────────────
app.get('/api/health', (req, res) => res.json({ status: 'ok', time: new Date().toISOString() }));

// ── Static Files ──────────────────────────────────────────────
app.use('/admin', express.static(path.join(__dirname, '..', 'admin')));
app.use(express.static(path.join(__dirname, '..')));

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
