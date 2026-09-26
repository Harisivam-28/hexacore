import os, re, glob

# New compact WhatsApp CSS rules
COMPACT_WA_CSS = '''
        /* ── WhatsApp Floating Widget & Popup ── */
        #wa-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 10px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        #whatsapp-float {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: linear-gradient(135deg, #25D366, #128C7E);
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 18px rgba(37,211,102,0.45), 0 2px 6px rgba(0,0,0,0.18);
            transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), box-shadow 0.25s;
            animation: wa-bounce 3s ease-in-out infinite;
            position: relative;
        }

        #whatsapp-float:hover {
            transform: scale(1.08);
            box-shadow: 0 8px 28px rgba(37,211,102,0.6), 0 3px 10px rgba(0,0,0,0.22);
            animation: none;
        }

        #wa-badge {
            position: absolute;
            top: -2px;
            right: -2px;
            background: #FF4444;
            color: #fff;
            font-size: 10px;
            font-weight: 700;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #fff;
            animation: wa-ping 1.5s ease-in-out infinite;
        }

        #wa-badge.hidden { display: none; }

        /* ── Compact Popup Card ── */
        #wa-popup {
            width: 260px;
            max-width: calc(100vw - 32px);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 12px 36px rgba(0,0,0,0.22), 0 3px 10px rgba(0,0,0,0.12);
            transform: scale(0.85) translateY(15px);
            transform-origin: bottom right;
            opacity: 0;
            pointer-events: none;
            transition: transform 0.3s cubic-bezier(.34,1.4,.64,1), opacity 0.25s ease;
        }

        #wa-popup.open {
            transform: scale(1) translateY(0);
            opacity: 1;
            pointer-events: all;
        }

        /* ── Compact Header ── */
        #wa-popup-header {
            background: linear-gradient(135deg, #075E54, #128C7E);
            padding: 10px 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        #wa-popup-avatar {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            border: 1.5px solid rgba(255,255,255,0.4);
        }

        #wa-popup-info { flex: 1; min-width: 0; }

        #wa-popup-name {
            color: #fff;
            font-size: 12.5px;
            font-weight: 700;
            line-height: 1.25;
            letter-spacing: 0.01em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        #wa-popup-status {
            color: rgba(255,255,255,0.85);
            font-size: 10.5px;
            display: flex;
            align-items: center;
            gap: 4px;
            margin-top: 2px;
        }

        #wa-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #4AFF82;
            display: inline-block;
            animation: wa-pulse 2s ease-in-out infinite;
            flex-shrink: 0;
        }

        #wa-close-btn {
            background: rgba(255,255,255,0.18);
            border: none;
            color: #fff;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            font-size: 15px;
            line-height: 1;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
            flex-shrink: 0;
        }

        #wa-close-btn:hover { background: rgba(255,255,255,0.35); }

        /* ── Compact Body ── */
        #wa-popup-body {
            background: #ECE5DD;
            padding: 10px;
            background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c8b9a8' fill-opacity='0.18'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }

        #wa-bubble {
            background: #fff;
            border-radius: 0 10px 10px 10px;
            padding: 10px 12px;
            font-size: 12px;
            line-height: 1.45;
            color: #2c3e50;
            box-shadow: 0 1px 5px rgba(0,0,0,0.08);
            position: relative;
        }

        #wa-bubble::before {
            content: '';
            position: absolute;
            left: -6px;
            top: 0;
            border: 6px solid transparent;
            border-right-color: #fff;
            border-top-color: #fff;
            border-left: none;
            border-bottom: none;
        }

        #wa-bubble p { margin: 0 0 5px; }
        #wa-bubble p:last-child { margin-bottom: 0; }
        #wa-bubble strong { color: #075E54; }
        #wa-bubble em { font-style: normal; font-size: 11px; color: #666; }

        /* ── Compact Footer ── */
        #wa-popup-footer {
            background: #F0F0F0;
            padding: 9px 10px;
        }

        #wa-start-chat {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: linear-gradient(135deg, #25D366, #128C7E);
            color: #fff;
            text-decoration: none;
            border-radius: 40px;
            padding: 8px 14px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.01em;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 3px 12px rgba(37,211,102,0.35);
        }

        #wa-start-chat:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(37,211,102,0.5);
        }

        @keyframes wa-bounce {
            0%, 100% { transform: translateY(0); }
            40%       { transform: translateY(-6px); }
            60%       { transform: translateY(-3px); }
        }
        @keyframes wa-ping {
            0%, 100% { transform: scale(1); opacity: 1; }
            50%       { transform: scale(1.15); opacity: 0.75; }
        }
        @keyframes wa-pulse {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.4; }
        }

        @media (max-width: 600px) {
            #wa-widget { bottom: 14px; right: 14px; }
            #whatsapp-float { width: 48px; height: 48px; }
            #wa-popup { width: calc(100vw - 28px); }
        }
'''

COMPACT_WA_HTML = '''        <!-- Popup card -->
        <div id="wa-popup" role="dialog" aria-label="WhatsApp Chat">
            <!-- Header -->
            <div id="wa-popup-header">
                <div id="wa-popup-avatar">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="20" height="20" fill="none">
                        <path fill="#fff" d="M23.5 8.5A10.94 10.94 0 0 0 16 5.5C10.2 5.5 5.5 10.2 5.5 16c0 1.86.48 3.67 1.4 5.27L5.5 26.5l5.37-1.4A10.96 10.96 0 0 0 16 26.5c5.8 0 10.5-4.7 10.5-10.5 0-2.8-1.09-5.43-3-7.5Zm-7.5 16.15a9.1 9.1 0 0 1-4.64-1.27l-.33-.2-3.18.83.85-3.1-.22-.34A9.1 9.1 0 0 1 6.9 16a9.1 9.1 0 0 1 9.1-9.1 9.1 9.1 0 0 1 9.1 9.1 9.1 9.1 0 0 1-9.1 9.15Zm5-6.8c-.28-.14-1.64-.81-1.9-.9-.26-.1-.44-.14-.63.14-.18.28-.72.9-.88 1.08-.16.18-.33.2-.6.07-.28-.14-1.17-.43-2.23-1.37-.82-.73-1.38-1.63-1.54-1.9-.16-.28-.02-.43.12-.57.12-.12.28-.32.42-.47.14-.15.18-.26.28-.44.09-.18.05-.34-.02-.47-.07-.14-.63-1.52-.87-2.08-.23-.54-.46-.47-.63-.47h-.54c-.18 0-.47.07-.72.34-.24.26-.94.92-.94 2.24 0 1.32.96 2.6 1.1 2.78.14.18 1.9 2.9 4.6 4.06.64.28 1.14.44 1.53.56.64.2 1.23.17 1.69.1.52-.08 1.6-.65 1.82-1.28.23-.63.23-1.17.16-1.28-.07-.12-.25-.19-.53-.33Z"/>
                    </svg>
                </div>
                <div id="wa-popup-info">
                    <div id="wa-popup-name">Hexacore Precision</div>
                    <div id="wa-popup-status"><span id="wa-dot"></span>Typically replies instantly</div>
                </div>
                <button id="wa-close-btn" aria-label="Close WhatsApp chat">&times;</button>
            </div>
            <!-- Body -->
            <div id="wa-popup-body">
                <div id="wa-bubble">
                    <p>👋 Hi! Welcome to <strong>Hexacore Precision</strong>.</p>
                    <p>Need CNC calibration, laser testing, or metrology support?</p>
                    <p>📍 <em>HSR Layout, Sector 3, Bengaluru</em></p>
                </div>
            </div>
            <!-- Footer -->
            <div id="wa-popup-footer">
                <a id="wa-start-chat"
                   href="https://wa.me/914445678900?text=Hello%20Hexacore%20Precision%20Technologies%2C%20I%20would%20like%20to%20enquire%20about%20your%20services."
                   target="_blank" rel="noopener noreferrer">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="16" height="16" fill="none">
                        <path fill="#fff" d="M23.5 8.5A10.94 10.94 0 0 0 16 5.5C10.2 5.5 5.5 10.2 5.5 16c0 1.86.48 3.67 1.4 5.27L5.5 26.5l5.37-1.4A10.96 10.96 0 0 0 16 26.5c5.8 0 10.5-4.7 10.5-10.5 0-2.8-1.09-5.43-3-7.5Zm-7.5 16.15a9.1 9.1 0 0 1-4.64-1.27l-.33-.2-3.18.83.85-3.1-.22-.34A9.1 9.1 0 0 1 6.9 16a9.1 9.1 0 0 1 9.1-9.1 9.1 9.1 0 0 1 9.1 9.1 9.1 9.1 0 0 1-9.1 9.15Zm5-6.8c-.28-.14-1.64-.81-1.9-.9-.26-.1-.44-.14-.63.14-.18.28-.72.9-.88 1.08-.16.18-.33.2-.6.07-.28-.14-1.17-.43-2.23-1.37-.82-.73-1.38-1.63-1.54-1.9-.16-.28-.02-.43.12-.57.12-.12.28-.32.42-.47.14-.15.18-.26.28-.44.09-.18.05-.34-.02-.47-.07-.14-.63-1.52-.87-2.08-.23-.54-.46-.47-.63-.47h-.54c-.18 0-.47.07-.72.34-.24.26-.94.92-.94 2.24 0 1.32.96 2.6 1.1 2.78.14.18 1.9 2.9 4.6 4.06.64.28 1.14.44 1.53.56.64.2 1.23.17 1.69.1.52-.08 1.6-.65 1.82-1.28.23-.63.23-1.17.16-1.28-.07-.12-.25-.19-.53-.33Z"/>
                    </svg>
                    Start Chat on WhatsApp
                </a>
            </div>
        </div>'''

for html_file in glob.glob('*.html') + ['admin/index.html']:
    if not os.path.exists(html_file): continue
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update <style> block for WA widget
    content = re.sub(
        r'/\* ── Widget Container ── \*/.*?(?=</style>)',
        COMPACT_WA_CSS,
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'#wa-widget\s*\{.*?(?=</style>)',
        COMPACT_WA_CSS,
        content,
        flags=re.DOTALL
    )

    # 2. Update popup HTML inside wa-widget
    content = re.sub(
        r'<!-- Popup card -->.*?(?=<!-- FAB trigger button -->)',
        COMPACT_WA_HTML + '\n\n        ',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<div id="wa-popup" role="dialog".*?(?=<button id="whatsapp-float")',
        COMPACT_WA_HTML + '\n\n        ',
        content,
        flags=re.DOTALL
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Made WhatsApp popup compact in {html_file}')
