/**
 * mailer.js — Hexacore Precision Technologies
 * Nodemailer transporter using Gmail SMTP.
 * Credentials are loaded from .env — never hard-coded.
 */

const nodemailer = require('nodemailer');

// ── Transporter ─────────────────────────────────────────────────
let transporter;

const cleanPass = (process.env.MAIL_PASS || '').replace(/\s+/g, '');
const isAppPassword = /^[a-z]{16}$/.test(cleanPass);

if (process.env.MAIL_USER && isAppPassword) {
  transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,           // SSL — required for port 465
    auth: {
      user: process.env.MAIL_USER,
      pass: process.env.MAIL_PASS,      // Gmail App Password (16 chars, no spaces)
    },
  });

  transporter.verify(err => {
    if (err) {
      console.warn('⚠️  Gmail SMTP authentication failed. Falling back to Mock Mailer.');
      setupMockTransporter();
    } else {
      console.log('✅ Email service ready —', process.env.MAIL_USER);
    }
  });
} else {
  console.log('ℹ️  No valid 16-character Gmail App Password configured in .env. Running in Mock Mailer mode.');
  setupMockTransporter();
}

function setupMockTransporter() {
  transporter = {
    sendMail: async (options) => {
      console.log('✉️  [MOCK MAIL] Simulated sending of email:');
      console.log('   From:   ', options.from);
      console.log('   To:     ', options.to);
      console.log('   Subject:', options.subject);
      console.log('   HTML length:', options.html ? options.html.length : 0);
      return { messageId: 'mock-id-' + Date.now() };
    }
  };
}

// ── Internal helpers ────────────────────────────────────────────

/**
 * Shared HTML shell used by all outgoing emails.
 * @param {string} title   — Email subject line (used in header)
 * @param {string} body    — Inner HTML content
 */
function htmlShell(title, body) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>
    body { margin: 0; padding: 0; background: #f0f2f5; font-family: 'Inter', Arial, sans-serif; }
    .wrapper { max-width: 620px; margin: 30px auto; background: #ffffff; }
    .header  { background: #0B1F3A; padding: 28px 36px; border-bottom: 3px solid #F47B20; }
    .header .brand { display: flex; align-items: center; gap: 12px; }
    .hex { width: 36px; height: 36px; background: #F47B20;
           clip-path: polygon(25% 3%, 75% 3%, 100% 50%, 75% 97%, 25% 97%, 0% 50%);
           display: flex; align-items: center; justify-content: center;
           font-weight: 800; color: #071527; font-size: 13px; }
    .brand-name  { color: #ffffff; font-size: 18px; font-weight: 800; letter-spacing: .04em; }
    .brand-sub   { color: #93a3bc; font-size: 10px; letter-spacing: .14em; text-transform: uppercase; margin-top: 2px; }
    .body   { padding: 36px; color: #1e2d42; }
    .title  { font-size: 22px; font-weight: 700; color: #0B1F3A; margin-bottom: 20px; text-transform: uppercase; letter-spacing: .02em; border-bottom: 2px solid #F47B20; padding-bottom: 12px; }
    .field  { margin-bottom: 16px; }
    .field .label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: #8296b0; margin-bottom: 4px; }
    .field .value { font-size: 14.5px; color: #1e2d42; line-height: 1.55; background: #f6f8fb; padding: 10px 14px; border-left: 3px solid #F47B20; }
    .message-box { background: #f6f8fb; border-left: 3px solid #F47B20; padding: 16px 18px; margin-top: 8px; font-size: 14px; line-height: 1.7; color: #2e3f56; white-space: pre-wrap; }
    .footer { background: #071527; padding: 20px 36px; text-align: center; }
    .footer p { color: #4a5e7a; font-size: 11px; margin: 0; }
    .footer a { color: #F47B20; text-decoration: none; }
    .badge { display: inline-block; background: rgba(244,123,32,.12); color: #F47B20; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; padding: 4px 10px; border: 1px solid rgba(244,123,32,.3); margin-bottom: 20px; }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <div class="brand">
        <div class="hex">HX</div>
        <div>
          <div class="brand-name">HEXACORE</div>
          <div class="brand-sub">Precision Technologies</div>
        </div>
      </div>
    </div>
    <div class="body">
      ${body}
    </div>
    <div class="footer">
      <p>Hexacore Precision Technologies &nbsp;|&nbsp; <a href="mailto:${process.env.COMPANY_EMAIL}">${process.env.COMPANY_EMAIL}</a></p>
      <p style="margin-top:6px;">This is an automated notification. Do not reply to this email directly.</p>
    </div>
  </div>
</body>
</html>`;
}

// ── Exported mail functions ─────────────────────────────────────

/**
 * Send a notification to the company when a contact form is submitted.
 */
async function sendContactNotification({ name, company, email, phone, subject, message }) {
  const html = htmlShell('New Contact Form Submission', `
    <div class="badge">New Contact Submission</div>
    <div class="title">Contact Form — ${escHtml(subject || 'General Enquiry')}</div>

    <div class="field">
      <div class="label">Full Name</div>
      <div class="value">${escHtml(name)}</div>
    </div>

    <div class="field">
      <div class="label">Company</div>
      <div class="value">${escHtml(company || '—')}</div>
    </div>

    <div class="field">
      <div class="label">Email Address</div>
      <div class="value"><a href="mailto:${escHtml(email)}" style="color:#F47B20">${escHtml(email)}</a></div>
    </div>

    <div class="field">
      <div class="label">Phone</div>
      <div class="value">${escHtml(phone || '—')}</div>
    </div>

    <div class="field">
      <div class="label">Subject</div>
      <div class="value">${escHtml(subject || '—')}</div>
    </div>

    <div class="field">
      <div class="label">Message</div>
      <div class="message-box">${escHtml(message || '—')}</div>
    </div>

    <p style="margin-top:24px;font-size:13px;color:#5b6b7f;">
      Reply directly to <a href="mailto:${escHtml(email)}" style="color:#F47B20">${escHtml(email)}</a> to respond to this enquiry.
    </p>
  `);

  return transporter.sendMail({
    from: `"${process.env.COMPANY_NAME}" <${process.env.MAIL_USER}>`,
    to: process.env.COMPANY_EMAIL,
    replyTo: email,
    subject: `[Contact] ${subject || 'New Enquiry'} — ${name}`,
    html,
  });
}

/**
 * Send an auto-reply confirmation to the user who submitted the contact form.
 */
async function sendContactConfirmation({ name, email, subject, message }) {
  const html = htmlShell('We received your message', `
    <div class="badge">Message Received</div>
    <div class="title">Thank You, ${escHtml(name.split(' ')[0])}</div>

    <p style="font-size:15px;line-height:1.7;color:#2e3f56;margin-bottom:20px;">
      We've received your enquiry and one of our engineers will review it shortly.
      You can expect a response within <strong>one business day</strong>.
    </p>

    <div class="field">
      <div class="label">Your Subject</div>
      <div class="value">${escHtml(subject || 'General Enquiry')}</div>
    </div>

    <div class="field">
      <div class="label">Your Message</div>
      <div class="message-box">${escHtml(message || '—')}</div>
    </div>

    <p style="margin-top:24px;font-size:13px;color:#5b6b7f;">
      If this is urgent, you can also reach us directly at
      <a href="mailto:${process.env.COMPANY_EMAIL}" style="color:#F47B20">${process.env.COMPANY_EMAIL}</a>.
    </p>
  `);

  return transporter.sendMail({
    from: `"${process.env.COMPANY_NAME}" <${process.env.MAIL_USER}>`,
    to: email,
    subject: `We received your message — Hexacore Precision Technologies`,
    html,
  });
}

/**
 * Send a notification to the company when a quote request is submitted.
 */
async function sendQuoteNotification({ name, company, email, phone, subject, message }) {
  const html = htmlShell('New Quote Request', `
    <div class="badge">Quote Request</div>
    <div class="title">Quote Request — ${escHtml(company || name)}</div>

    <div class="field">
      <div class="label">Contact Name</div>
      <div class="value">${escHtml(name)}</div>
    </div>

    <div class="field">
      <div class="label">Company</div>
      <div class="value">${escHtml(company || '—')}</div>
    </div>

    <div class="field">
      <div class="label">Email</div>
      <div class="value"><a href="mailto:${escHtml(email)}" style="color:#F47B20">${escHtml(email)}</a></div>
    </div>

    <div class="field">
      <div class="label">Phone</div>
      <div class="value">${escHtml(phone || '—')}</div>
    </div>

    <div class="field">
      <div class="label">Type of Requirement</div>
      <div class="value">${escHtml(subject || '—')}</div>
    </div>

    <div class="field">
      <div class="label">Project Details</div>
      <div class="message-box">${escHtml(message || '—')}</div>
    </div>

    <p style="margin-top:24px;font-size:13px;color:#5b6b7f;">
      Reply to <a href="mailto:${escHtml(email)}" style="color:#F47B20">${escHtml(email)}</a> to follow up on this request.
    </p>
  `);

  return transporter.sendMail({
    from: `"${process.env.COMPANY_NAME}" <${process.env.MAIL_USER}>`,
    to: process.env.COMPANY_EMAIL,
    replyTo: email,
    subject: `[Quote] ${subject || 'New Request'} — ${company || name}`,
    html,
  });
}

/**
 * Send an auto-reply confirmation to the user who submitted a quote request.
 */
async function sendQuoteConfirmation({ name, email }) {
  const html = htmlShell('Quote request received', `
    <div class="badge">Quote Request Received</div>
    <div class="title">We'll Be In Touch, ${escHtml(name.split(' ')[0])}</div>

    <p style="font-size:15px;line-height:1.7;color:#2e3f56;margin-bottom:20px;">
      Your quote request has been logged and assigned to our engineering team.
      We will review your requirements and get back to you with a detailed proposal
      within <strong>2 business days</strong>.
    </p>

    <p style="font-size:13px;line-height:1.7;color:#5b6b7f;">
      For faster turnaround, you're welcome to send drawings or CAD files directly to
      <a href="mailto:${process.env.COMPANY_EMAIL}" style="color:#F47B20">${process.env.COMPANY_EMAIL}</a>.
    </p>
  `);

  return transporter.sendMail({
    from: `"${process.env.COMPANY_NAME}" <${process.env.MAIL_USER}>`,
    to: email,
    subject: `Your quote request — Hexacore Precision Technologies`,
    html,
  });
}

// ── Utility ─────────────────────────────────────────────────────
function escHtml(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

module.exports = {
  sendContactNotification,
  sendContactConfirmation,
  sendQuoteNotification,
  sendQuoteConfirmation,
};
