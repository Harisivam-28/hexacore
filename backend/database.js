const initSqlJs = require('sql.js');
const bcrypt    = require('bcryptjs');
const fs        = require('fs');
const path      = require('path');

const DB_PATH = path.join(__dirname, 'hexacore.db');

let db;       // sql.js Database instance (sync API)

async function init() {
  const SQL = await initSqlJs();

  // Load existing DB file or create fresh
  if (fs.existsSync(DB_PATH)) {
    const filebuffer = fs.readFileSync(DB_PATH);
    db = new SQL.Database(filebuffer);
  } else {
    db = new SQL.Database();
  }

  // Persist helper: save DB to disk after every write
  db.save = function () {
    const data = db.export();
    fs.writeFileSync(DB_PATH, Buffer.from(data));
  };

  // ── Create Tables ──────────────────────────────────────────────
  db.run(`
    CREATE TABLE IF NOT EXISTS admins (
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      username   TEXT    NOT NULL UNIQUE,
      password   TEXT    NOT NULL,
      created_at TEXT    DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS contacts (
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      name       TEXT NOT NULL,
      company    TEXT,
      email      TEXT NOT NULL,
      phone      TEXT,
      subject    TEXT,
      message    TEXT,
      status     TEXT DEFAULT 'new',
      created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS quotes (
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      name       TEXT NOT NULL,
      company    TEXT,
      email      TEXT NOT NULL,
      phone      TEXT,
      subject    TEXT,
      message    TEXT,
      status     TEXT DEFAULT 'pending',
      created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS newsletter (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      email         TEXT NOT NULL UNIQUE,
      subscribed_at TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS products (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      name        TEXT NOT NULL,
      category    TEXT,
      description TEXT,
      tolerance   TEXT,
      active      INTEGER DEFAULT 1,
      created_at  TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS services (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      number      TEXT,
      title       TEXT NOT NULL,
      description TEXT,
      active      INTEGER DEFAULT 1,
      created_at  TEXT DEFAULT (datetime('now'))
    );
  `);

  // ── Helpers ────────────────────────────────────────────────────
  // Return all rows from a SELECT as array of objects
  db.query = function (sql, params = []) {
    const stmt = db.prepare(sql);
    stmt.bind(params);
    const rows = [];
    while (stmt.step()) rows.push(stmt.getAsObject());
    stmt.free();
    return rows;
  };

  // Run INSERT/UPDATE/DELETE and return { lastInsertRowid, changes }
  db.exec2 = function (sql, params = []) {
    const stmt = db.prepare(sql);
    stmt.run(params);
    stmt.free();
    const rowid   = db.exec('SELECT last_insert_rowid() AS r')[0]?.values[0][0];
    const changes = db.exec('SELECT changes() AS c')[0]?.values[0][0];
    db.save();
    return { lastInsertRowid: rowid, changes };
  };

  // Return single row
  db.queryOne = function (sql, params = []) {
    const rows = db.query(sql, params);
    return rows[0] || null;
  };

  // ── Seed Admin ─────────────────────────────────────────────────
  const existing = db.queryOne('SELECT id FROM admins WHERE username = ?', ['admin']);
  if (!existing) {
    const hash = bcrypt.hashSync('hexacore2026', 10);
    db.exec2('INSERT INTO admins (username, password) VALUES (?, ?)', ['admin', hash]);
    console.log('✅ Default admin created — username: admin | password: hexacore2026');
  }

  // ── Seed Products ──────────────────────────────────────────────
  const pc = db.queryOne('SELECT COUNT(*) AS c FROM products').c;
  if (!pc) {
    const seeds = [
      ['Precision Shaft Assembly',    'CNC Precision Component',   'Ground and turned shaft with tight concentricity for rotating equipment.',       '±0.005mm'],
      ['Flange Housing',              'Machined Component',         'Multi-bore flange housing milled from billet aluminum, anodized finish.',         'Ø18.00 H7'],
      ['Mounting Bracket Plate',      'Industrial Component',       'Structural bracket plate, waterjet blanked and CNC finished to spec.',            '±0.01mm'],
      ['Hex Drive Fastener Set',      'Custom Manufactured Part',   'Custom hex-drive fasteners machined from stainless bar stock.',                  'M12 x 1.5'],
      ['Precision Gearbox Housing',   'CNC Precision Component',   '5-axis milled housing with cross-drilled oil channels and sealed faces.',         '±0.008mm'],
      ['Precision Cam Disc',          'Machined Component',         'Hardened steel cam disc, profile-ground for automated assembly lines.',           'Ra 0.4'],
      ['Adjustable Slide Rail',       'Industrial Component',       'Precision slide rail set with hardened wear surfaces for linear motion.',         '±0.02mm'],
      ['Prototype-to-Production Kit', 'Custom Manufactured Part',   'Engineered from customer CAD through pilot run and full production.',            'Custom Spec'],
    ];
    seeds.forEach(([name, category, description, tolerance]) => {
      db.exec2('INSERT INTO products (name, category, description, tolerance) VALUES (?, ?, ?, ?)', [name, category, description, tolerance]);
    });
    console.log('✅ Products seeded');
  }

  // ── Seed Services ──────────────────────────────────────────────
  const sc = db.queryOne('SELECT COUNT(*) AS c FROM services').c;
  if (!sc) {
    const svcs = [
      ['SVC / 01', 'CNC Milling',                    '3, 4 and 5-axis milling for complex geometries, tight tolerances and superior surface finish.'],
      ['SVC / 02', 'CNC Turning',                    'High-precision turning for cylindrical components, shafts and rotational parts.'],
      ['SVC / 03', 'Precision Machining',             'Micron-level accuracy machining for critical, close-tolerance applications.'],
      ['SVC / 04', 'Custom Component Manufacturing', 'Fully custom parts engineered and produced to your exact drawings and specification.'],
      ['SVC / 05', 'Engineering Solutions',           'DFM review, CAD/CAM programming and process design support from our engineering team.'],
      ['SVC / 06', 'Quality Inspection',              'Full CMM dimensional inspection, material certification and SPC reporting.'],
    ];
    svcs.forEach(([number, title, description]) => {
      db.exec2('INSERT INTO services (number, title, description) VALUES (?, ?, ?)', [number, title, description]);
    });
    console.log('✅ Services seeded');
  }

  console.log('✅ Database ready');
  return db;
}

module.exports = { init, getDb: () => db };
