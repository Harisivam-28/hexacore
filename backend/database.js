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
      ['Precision Measurement Equipment', 'Technology', 'Advanced metrology equipment for reliable performance diagnostics.', 'High Precision'],
      ['Laser Measurement Technology', 'Technology', 'Laser interferometer systems for positioning accuracy verification.', 'Sub-micron'],
      ['Machine Calibration Technology', 'Technology', 'Calibration tools to align and restore original machine tolerances.', 'ISO/VDI Standard'],
      ['CNC Measurement Solutions', 'Technology', 'Integrated measurement systems for automated CNC quality control.', 'Dynamic'],
      ['Machine Diagnostic Technology', 'Technology', 'Diagnostic systems identifying kinematic and geometric machine errors.', 'Advanced'],
      ['Precision Engineering Solutions', 'Solutions', 'Custom engineering and technical support for complex machining challenges.', 'Custom Spec']
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
      ['SVC / 01', 'Linear Laser Calibration', 'Precision measurement of machine-axis positioning accuracy using laser interferometer technology.'],
      ['SVC / 02', 'Machine Health Diagnosis / Ballbar Testing', 'Assessment of CNC machine performance through circular interpolation testing and analysis.'],
      ['SVC / 03', 'Rotary Axis Calibration', 'Measurement and calibration of rotary-axis positioning and indexing accuracy.'],
      ['SVC / 04', 'Off-Axis Rotary Calibration', 'Evaluation of rotary-axis errors when operating away from the rotational centre line.'],
      ['SVC / 05', 'Axis Straightness Testing', 'Measurement of linear deviations along the machine travel to identify geometric inaccuracies.'],
      ['SVC / 06', 'Squareness Testing', 'Verification of perpendicularity between machine axes to maintain geometric accuracy.'],
      ['SVC / 07', 'Machine Leveling & Relocation', 'Machine leveling, alignment and relocation support to help maintain geometric performance.'],
      ['SVC / 08', 'Axis Servo Tuning', 'Technical assessment and tuning support for servo-related machine performance issues.'],
      ['SVC / 09', 'LM Guideway Parallelism Checking', 'Inspection of guideway alignment and parallelism to identify potential geometric errors.'],
      ['SVC / 10', 'Software Troubleshooting', 'Technical support for machine-control and software-related issues affecting machine performance.'],
      ['SVC / 11', 'Ballscrew Replacement Support', 'Technical support for ballscrew replacement, alignment and related machine accuracy requirements.'],
      ['SVC / 12', 'Preventive Maintenance', 'Planned maintenance and periodic calibration support designed to reduce unexpected machine problems and downtime.']
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
