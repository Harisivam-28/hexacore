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
      image       TEXT,
      active      INTEGER DEFAULT 1,
      created_at  TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS services (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      number      TEXT,
      title       TEXT NOT NULL,
      description TEXT,
      specs       TEXT,
      image       TEXT,
      active      INTEGER DEFAULT 1,
      created_at  TEXT DEFAULT (datetime('now'))
    );
  `);

  // Ensure image column exists in products
  try {
    db.exec('ALTER TABLE products ADD COLUMN image TEXT;');
  } catch (e) {
    // Column already exists
  }

  // Ensure specs & image columns exist in services
  try { db.exec('ALTER TABLE services ADD COLUMN specs TEXT;'); } catch (e) {}
  try { db.exec('ALTER TABLE services ADD COLUMN image TEXT;'); } catch (e) {}

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
  const adminUser = process.env.ADMIN_USER || 'admin';
  const adminPass = process.env.ADMIN_PASS || 'hexacore2026';
  const hash = bcrypt.hashSync(adminPass, 10);

  const adminCount = db.queryOne('SELECT COUNT(*) AS c FROM admins').c;
  if (adminCount === 0) {
    db.exec2('INSERT INTO admins (username, password) VALUES (?, ?)', [adminUser, hash]);
    console.log(`✅ Default admin created — username: ${adminUser} | password: ${adminPass}`);
  } else {
    const firstAdminId = db.queryOne('SELECT id FROM admins LIMIT 1').id;
    db.exec2('UPDATE admins SET username = ?, password = ? WHERE id = ?', [adminUser, hash, firstAdminId]);
    console.log(`✅ Admin credentials synchronized — username: ${adminUser}`);
  }

  // ── Seed Products ──────────────────────────────────────────────
  const pdfProducts = [
    // PDF 1: Gauges & Fixtures
    ['Plain Plug Gauge', 'Plain & Setting Gauges', 'Plain Plug Gauges to relevant I.S., B.S. and DIN standards based on customer requests from 5-100mm diameter. Specialized non-standard designs such as extra lengths, multiple diameters, air grooves, pilots, depth steps and relieved NO-GO ends.', 'IS:3455 (5-100mm)', 'images/products/plain_plug_gauge.png'],
    ['OD Master', 'Plain & Setting Gauges', 'OD Master supplied as per Standard and Customer Design. Used in comparison measurement methods to set zero value on measuring instruments.', 'Custom / Standard', 'images/products/od_master.png'],
    ['Master Setting Ring / Go-NoGo Ring Gauges', 'Plain & Setting Gauges', 'Setting Rings and plain Go/NoGo Rings according to I.S.3455-1971 gauging practice. Made of high grade En31 steel for high durability.', 'En31 (10-200mm)', 'images/products/master_setting_ring.png'],
    ['Thread Gauges', 'Thread Gauges', 'Wide variety of precision thread plug and ring gauges suitable for popularly used thread forms including Metric and Unified pitch standards.', 'Metric / Unified', 'images/products/thread_gauges.png'],
    ['Width Gauge', 'Special Gauges', 'KeyWay Width Gauges widely used in automobile industry for checking groove width according to IS design or custom drawings.', 'Range: 3.00-100.0mm', 'images/products/width_gauge.png'],
    ['Fixed Snap Gauge', 'Snap Gauges', 'Used for checking outer diameters, flange widths, and groove diameters. Made of subzero treated steel with 60±2HRC hardness.', 'IS:3455 (60±2HRC)', 'images/products/fixed_snap_gauge.png'],
    ['Knurling Height Master', 'Height Masters', 'Cylindrical height master (Dia 30.000mm Knurled & Black oxidized) used to set height gauges and dial gauges to exact dimensions with close tolerances.', 'Range: 10-150mm', 'images/products/knurling_height_master.png'],
    ['Plate / Paddle Gauge', 'Plain & Setting Gauges', 'Lightweight plate/paddle gauge designed to check internal diameters from 80mm to 500mm, reducing weight and cost over complete disc gauges.', 'Range: 80-500mm ID', 'images/products/plate_paddle_gauge.png'],
    ['Air Snap Gauge', 'Air Gauges', 'Precision air snap gauge with hardened rectangular steel body and carbide resting pads on V-surface. Two-jetted design for shaft size, taper & ovality measurement.', 'Range: 25-100mm', 'images/products/air_snap_gauge.png'],
    ['Air Plug Gauge', 'Air Gauges', 'Self-cleaning air plug gauge for internal bore measurement. Two-jetted design for checking size, taper and ovality in through or blind bores.', 'Range: 5-100mm', 'images/products/air_plug_gauge.png'],
    ['Flush Pin Gauge', 'Depth Gauges', 'Flush Pin / Step Pin Gauge for GO/NOGO depth evaluation of holes, counterbores, and step depths with ground precision tolerance steps.', 'GO/NOGO Step Depth', 'images/products/flush_pin_gauge.png'],
    ['PCD Gauge', 'Fixtures & Gauges', 'Pitch Circle Diameter checking gauge for accurate measurement of bolt circle diameters in flanges, wheels, and gears for automotive and aerospace components.', 'High Precision PCD', 'images/products/pcd_gauge.png'],
    ['Receiving / Relation Gauge', 'Fixtures & Gauges', 'Custom relation/receiving gauge used for contour and size inspection of male parts without requiring a coordinate measuring system (CMM).', 'Custom Inspection Fixture', 'images/products/receiving_relation_gauge.png'],
    
    // PDF 2: Air Units & Precision Equipment
    ['Single Channel Air Electronic Unit', 'Air Electronic Units', 'Single Channel Air Electronic Unit with 1/2" Auto Drain Filters, Digital Piezo Transducer, 6-character tri-color LED display, program storage for 10-16 programs, USB & online SPC.', 'Res: 0.0001mm / 0.1 thou', 'images/products/air_electronic_unit_single.png'],
    ['Multi-Channel Air Electronic Unit', 'Air Electronic Units', 'Two to Eight Channel Air Electronic Unit for static or dynamic measurements (Max, Min, Avg, TIR) with ovality key, auto-correction, USB data logging and SPC connectivity.', '2 to 8 Channel (0.0001mm)', 'images/products/air_electronic_unit_multi.png'],
    ['Air Electronic Column Unit', 'Air Electronic Units', 'Air Electronic Column Unit featuring a high-visibility Tri-Color LED Bar Indicator and 6-character display, operating 0.80 to 2.0mm air jets with wrong master calibration alerts.', 'Tri-Color Bar Display', 'images/products/air_electronic_column_unit.png'],
    ['Special Filter (SS Air Dryer)', 'Air Accessories', 'Stainless Steel Air Dryer with Auto Drain Filter. Protects pneumatic metrology units from moisture and nano-particles to increase durability in harsh environments.', 'SS Auto Drain Filter', 'images/products/special_filter.png'],
    ['SPC Air Unit (S-Touch)', 'Air Electronic Units', 'Touchscreen SPC Air Unit with 7" TFT display (800x480 resolution), Piezo sensors, 2/4/8 outputs, real-time clock, SD RAM, and USB data logging.', '7" Touchscreen (800x480)', 'images/products/spc_air_unit.png'],
    ['2D & CMM Probes', 'Probes & Styli', 'High precision 2D and CMM styli, star probes, and pencil probes engineered for high repeatability in dimensional inspection and scanning.', 'Sub-micron Repeatability', 'images/products/cmm_probes.png'],
    ['Vision Measuring System', 'Metrology Equipment', 'Optical 2D Vision Measuring System (ATQ METRO STD 3020) for high-accuracy non-contact measurement of micro-components, circuit boards, and precision parts.', 'STD 3020 Optical', 'images/products/vision_measuring_system.png'],
    ['2D Height Gauges', 'Metrology Equipment', 'Precision 1D/2D vertical height gauges (Trimos V Series - V3, V4, V5, V6) with motorized displacement, air cushion support, and high accuracy linear encoders.', 'Trimos V Series', 'images/products/height_gauge_2d.png'],
    ['Coordinate Measuring Machine (CMM)', 'Metrology Equipment', 'High accuracy 3D Coordinate Measuring Machine (Global S / Bridge CMM) with multisensor probing for complex 3D surface and geometric dimensioning & tolerancing (GD&T).', '3D GD&T Inspection', 'images/products/cmm_machine.png']
  ];

  // Remove old generic seed products if present
  db.exec2("DELETE FROM products WHERE name IN ('Precision Measurement Equipment', 'Laser Measurement Technology', 'Machine Calibration Technology', 'CNC Measurement Solutions', 'Machine Diagnostic Technology', 'Precision Engineering Solutions')");

  // Sync products: insert missing products or update existing ones
  pdfProducts.forEach(([name, category, description, tolerance, image]) => {
    const existing = db.queryOne('SELECT id FROM products WHERE name = ?', [name]);
    if (existing) {
      db.exec2('UPDATE products SET category=?, description=?, tolerance=?, image=?, active=1 WHERE id=?', [category, description, tolerance, image, existing.id]);
    } else {
      db.exec2('INSERT INTO products (name, category, description, tolerance, image, active) VALUES (?, ?, ?, ?, ?, 1)', [name, category, description, tolerance, image]);
    }
  });
  console.log('✅ PDF Products synchronized with database');

  // ── Seed Services (Brochure Services) ─────────────────────────
  const brochureServices = [
    ['SVC / 01', 'Linear Laser Calibration', 'Ensures precise positioning accuracy of machine axes using laser interferometer systems.', 'Accuracy up to 0.005 ppm, positioning & repeatability analysis, pitch error compensation, ISO 230-2 compliant.', 'images/services/linear_laser_calibration.png'],
    ['SVC / 02', 'Machine Health Diagnose (Ballbar Test)', 'Evaluates overall CNC performance by analyzing circular interpolation errors.', 'Detects backlash, servo mismatch, cyclic errors; 360° and 220° tests; quick diagnostic within minutes; ISO 230-4 standard.', 'images/services/machine_health_diagnose.png'],
    ['SVC / 03', 'Rotary Axis Calibration', 'Calibrates rotary axes for accurate angular positioning and indexing.', 'Angular accuracy up to +1 arc-sec, indexing error mapping, encoder verification, improves 4th/5th axis performance.', 'images/services/rotary_axis_calibration.png'],
    ['SVC / 04', 'Off-Axis Rotary Calibration', 'Measures rotary axis errors when positioned away from the center line.', 'Eccentricity and tilt error analysis, volumetric compensation support, critical for multi-axis machining accuracy.', 'images/services/off_axis_rotary_calibration.png'],
    ['SVC / 05', 'Axis Straightness Testing', 'Checks linear deviations in axis movement along travel length.', 'Measurement in horizontal & vertical planes, micron-level accuracy, laser-based or electronic levels, ISO 230-1.', 'images/services/axis_straightness_testing.png'],
    ['SVC / 06', 'Squareness Testing', 'Verifies perpendicularity between machine axes for geometric precision.', 'Laser or granite square methods, angular error measurement in microns/meter, improves part geometry accuracy.', 'images/services/squareness_testing.png'],
    ['SVC / 07', 'Preventive Maintenance Contract', 'Scheduled maintenance to ensure consistent machine performance and reliability.', 'Periodic calibration check, lubrication inspection, alignment verification, customized service intervals, downtime reduction.', 'images/services/preventive_maintenance_contract.png']
  ];

  // Clean up any old services that don't match the 7 brochure service titles
  const validTitles = brochureServices.map(s => s[1]);
  const existingServices = db.query('SELECT id, title FROM services');
  existingServices.forEach(s => {
    if (!validTitles.includes(s.title)) {
      db.exec2('DELETE FROM services WHERE id = ?', [s.id]);
    }
  });

  // Sync services: insert or update
  brochureServices.forEach(([number, title, description, specs, image]) => {
    const existing = db.queryOne('SELECT id FROM services WHERE title = ?', [title]);
    if (existing) {
      db.exec2('UPDATE services SET number=?, description=?, specs=?, image=?, active=1 WHERE id=?', [number, description, specs, image, existing.id]);
    } else {
      db.exec2('INSERT INTO services (number, title, description, specs, image, active) VALUES (?, ?, ?, ?, ?, 1)', [number, title, description, specs, image]);
    }
  });
  console.log('✅ Brochure Services synchronized with database');

  console.log('✅ Database ready');
  return db;
}

module.exports = { init, getDb: () => db };
