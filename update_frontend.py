import re

with open('frontend.html', 'r') as f:
    content = f.read()

# 1. Update Typography and Colors
content = re.sub(
    r'<title>.*?</title>',
    '<title>Hexacore Precision Technologies — Precision Engineering & Calibration</title>',
    content, flags=re.DOTALL
)

# Update CSS variables (keep them mostly as is since they are already navy/charcoal/orange, but ensure they match)
# Let's just rely on the existing palette, as it matches Deep Navy/Charcoal, White, Light Grey, Controlled Orange.
# I will change the font families to be more standard sans-serif.
content = re.sub(
    r'font-family: \'Barlow Semi Condensed\', sans-serif;',
    'font-family: \'Inter\', sans-serif;',
    content
)
content = re.sub(
    r'font-family: \'IBM Plex Mono\', monospace;',
    'font-family: \'Inter\', sans-serif;',
    content
)

# 2. Update Footer HTML in the script tag
new_footer = """
<div class="footer-grid">
  <div>
    <div class="brand" style="margin-bottom:16px;"><div class="hex-mark">HX</div><div class="brand-text"><div class="name">HEXACORE</div><div class="sub">Precision Technologies</div></div></div>
    <p>Precision Engineering. Reliable Performance.</p>
  </div>
  <div><h5>Quick Links</h5><ul>
    <li><a onclick="showPage(1)">Home</a></li><li><a onclick="showPage(2)">About Us</a></li>
    <li><a onclick="showPage(3)">Products</a></li><li><a onclick="showPage(4)">Services &amp; Support</a></li><li><a onclick="showPage(5)">Contact</a></li>
  </ul></div>
  <div><h5>Services</h5><ul>
    <li><a onclick="showPage(4)">Laser Calibration</a></li><li><a onclick="showPage(4)">Ballbar Testing</a></li><li><a onclick="showPage(4)">Rotary Axis Calibration</a></li><li><a onclick="showPage(4)">Machine Diagnostics</a></li><li><a onclick="showPage(4)">Geometric Accuracy Testing</a></li><li><a onclick="showPage(4)">Preventive Maintenance</a></li>
  </ul></div>
  <div><h5>Contact</h5><ul>
    <li>No. 1190/1, FD 211, 4th Floor, HSR Layout, Sector 3, 22nd Cross Road, Bengaluru – 560102</li><li>+91 44 4567 8900</li><li>info@hexacoreprecision.com</li>
  </ul></div>
</div>
<div class="footer-bottom">
  <div>© 2026 Hexacore Precision Technologies. All rights reserved.</div>
  <div>Precision Engineered. Reliable Performance.</div>
</div>"""

content = re.sub(
    r'const footerHTML = `.*?`;',
    f'const footerHTML = `{new_footer}`;',
    content, flags=re.DOTALL
)

with open('frontend_new.html', 'w') as f:
    f.write(content)

