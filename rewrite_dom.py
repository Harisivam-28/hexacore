import bs4
import re

with open('frontend_new.html', 'r', encoding='utf-8') as f:
    soup = bs4.BeautifulSoup(f, 'lxml')

# 1. Update Navigation and headers across all pages
for header in soup.select('header.site-header'):
    # Change "Request a Quote" to "GET IN TOUCH"
    cta = header.select_one('.nav-cta')
    if cta:
        cta.string = 'GET IN TOUCH'
        cta['onclick'] = "showPage(5)"

# 2. Rebuild Page 1 (Homepage)
page1 = soup.find(id='page1')
page1.clear()

# Add screen tag and header back (copy from original or create new)
page1.append(bs4.BeautifulSoup('''
<div class="screen-tag">hexacore.com / home</div>
<header class="site-header">
    <div class="brand">
        <div class="hex-mark">HX</div>
        <div class="brand-text">
            <div class="name">HEXACORE</div>
            <div class="sub">Precision Technologies</div>
        </div>
    </div>
    <nav class="main-nav">
        <a class="current" onclick="showPage(1)">Home</a>
        <a onclick="showPage(2)">About Us</a>
        <a onclick="showPage(3)">Products</a>
        <a onclick="showPage(4)">Services &amp; Support</a>
        <a onclick="showPage(5)">Contact</a>
    </nav>
    <a class="nav-cta btn btn-orange" onclick="showPage(5)">GET IN TOUCH</a>
</header>
''', 'html.parser'))

# Build Homepage Sections
homepage_content = '''
<!-- 1. HERO SECTION -->
<section class="hero" style="background: radial-gradient(circle at 82% 20%, rgba(244, 123, 32, .18), transparent 45%), linear-gradient(180deg, var(--navy-dark) 0%, var(--navy) 60%, var(--navy-mid) 100%);">
    <div class="hero-grid">
        <div>
            <h1 class="t-display" style="color: #fff; line-height: 1.1; margin-bottom: 20px;">
                Precision Engineering for <span style="color: var(--orange);">Reliable Industrial Performance</span>
            </h1>
            <p class="lead" style="color: #B9C4D6; font-size: clamp(15px, 1.6vw, 17.5px); max-width: 580px; margin-bottom: 36px; line-height: 1.75;">
                Hexacore Precision Technologies provides precision engineering, measurement, calibration and technical support solutions that help manufacturers improve machine accuracy, reliability and production performance.
            </p>
            <div class="hero-btns">
                <a class="btn btn-orange" onclick="showPage(4)">Explore Our Services</a>
                <a class="btn btn-outline" onclick="showPage(5)">Talk to Our Engineers</a>
            </div>
        </div>
        <div class="hero-art">
            <img src="images/spider_man.jpeg" style="width: 100%; border: 2px solid var(--orange); opacity: 0.8; filter: grayscale(100%); mix-blend-mode: luminosity; border-radius: 4px;" alt="Precision Measurement">
        </div>
    </div>
</section>

<!-- 2. ABOUT US -->
<section class="section grey">
    <div class="section-head">
        <div class="tag">About Hexacore Precision Technologies</div>
        <h2 class="t-h2">Experienced. Technical. Trustworthy.</h2>
        <p class="section-lead">
            Hexacore Precision Technologies is focused on helping manufacturing companies maintain the accuracy, reliability and performance of their machines and production systems.
        </p>
    </div>
    <div style="max-width: 800px; color: var(--steel); font-size: var(--t-body-lg); line-height: 1.8;">
        <p style="margin-bottom: 16px;">Our work combines engineering experience, precision measurement and practical technical support to identify machine performance issues and provide solutions that are suited to the application.</p>
        <p style="margin-bottom: 16px;">We work with a wide range of CNC machines and industrial equipment, supporting customers with calibration, machine health assessment, geometric accuracy checks and related technical services.</p>
        <p>Our approach is simple: understand the machine, measure accurately, identify the source of the problem and provide a practical solution that helps the customer maintain consistent production.</p>
    </div>
</section>

<!-- 3. PRODUCTS / CAPABILITIES -->
<section class="section">
    <div class="section-head">
        <div class="tag">Products & Technology</div>
        <h2 class="t-h2">Precision Measurement Equipment</h2>
    </div>
    <div class="product-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px;">
        <p style="color: var(--steel);">Loading capabilities...</p>
    </div>
</section>

<!-- 4. SERVICES & SUPPORT -->
<section class="section grey">
    <div class="section-head">
        <div class="tag">Services & Technical Support</div>
        <h2 class="t-h2">From machine calibration to technical troubleshooting.</h2>
        <p class="section-lead">Our services are designed to help manufacturers maintain accuracy and keep production running reliably.</p>
    </div>
    <div class="svc-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
        <p style="color: var(--steel);">Loading services...</p>
    </div>
</section>

<!-- 5. INDUSTRIES WE SERVE -->
<section class="section navy">
    <div class="section-head">
        <div class="tag">Industries</div>
        <h2 class="t-h2" style="color:#fff;">Supporting Precision Manufacturing Across Industries</h2>
        <p class="section-lead" style="color: #AAB6C9;">
            Every manufacturing environment has different requirements. We work closely with our customers to understand their machines, processes and accuracy requirements before recommending the appropriate measurement or support solution.
        </p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">Automotive</div>
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">Aerospace</div>
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">Heavy Engineering</div>
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">Precision Manufacturing</div>
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">Machine Tools</div>
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">General Engineering</div>
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">CNC Manufacturing</div>
        <div class="ind-card" style="border-left: 2px solid var(--orange); padding: 16px; background: rgba(255,255,255,0.05);">Industrial Production</div>
    </div>
</section>

<!-- 6. WHY CHOOSE HEXACORE -->
<section class="section">
    <div class="section-head">
        <div class="tag">Why Hexacore</div>
        <h2 class="t-h2">Why Companies Choose Hexacore</h2>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px;">
        <div style="padding: 24px; border: 1px solid var(--line); border-top: 3px solid var(--orange);">
            <h4 style="margin-bottom: 12px; font-size: 18px; text-transform: uppercase;">Engineering Expertise</h4>
            <p style="color: var(--steel); font-size: 15px;">Practical engineering knowledge backed by experience with CNC machines and precision measurement.</p>
        </div>
        <div style="padding: 24px; border: 1px solid var(--line); border-top: 3px solid var(--orange);">
            <h4 style="margin-bottom: 12px; font-size: 18px; text-transform: uppercase;">Precision Measurement</h4>
            <p style="color: var(--steel); font-size: 15px;">Accurate measurement helps identify problems that may not be visible during normal machine operation.</p>
        </div>
        <div style="padding: 24px; border: 1px solid var(--line); border-top: 3px solid var(--orange);">
            <h4 style="margin-bottom: 12px; font-size: 18px; text-transform: uppercase;">Practical Solutions</h4>
            <p style="color: var(--steel); font-size: 15px;">We focus on understanding the cause of an issue and recommending solutions that make sense for the machine and application.</p>
        </div>
        <div style="padding: 24px; border: 1px solid var(--line); border-top: 3px solid var(--orange);">
            <h4 style="margin-bottom: 12px; font-size: 18px; text-transform: uppercase;">Detailed Reporting</h4>
            <p style="color: var(--steel); font-size: 15px;">Clear measurement results and technical observations help customers understand machine condition and plan corrective action.</p>
        </div>
        <div style="padding: 24px; border: 1px solid var(--line); border-top: 3px solid var(--orange);">
            <h4 style="margin-bottom: 12px; font-size: 18px; text-transform: uppercase;">Multi-Platform Support</h4>
            <p style="color: var(--steel); font-size: 15px;">Experience across different machine types and CNC controller platforms.</p>
        </div>
        <div style="padding: 24px; border: 1px solid var(--line); border-top: 3px solid var(--orange);">
            <h4 style="margin-bottom: 12px; font-size: 18px; text-transform: uppercase;">Responsive Technical Support</h4>
            <p style="color: var(--steel); font-size: 15px;">We aim to respond quickly and minimise disruption to your production activities.</p>
        </div>
    </div>
</section>

<!-- 7. MACHINES WE SUPPORT & CNC CONTROLLERS -->
<section class="section grey">
    <div class="section-head">
        <div class="tag">Technology / Engineering Capabilities</div>
        <h2 class="t-h2">Machines & Controllers We Support</h2>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 60px;">
        <div>
            <h3 style="margin-bottom: 24px; padding-bottom: 8px; border-bottom: 2px solid var(--orange);">CNC Machines</h3>
            <ul style="list-style: none; padding: 0;">
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> CNC Turning Centres</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> Vertical Machining Centres (VMC)</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> Horizontal Machining Centres (HMC)</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> 5-Axis CNC Machines</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> Gantry / Plano Milling Machines</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> Double Column Machining Centres</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> CNC Grinding Machines</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> Boring Machines</li>
                <li style="margin-bottom: 8px; color: var(--steel); display: flex; align-items: center; gap: 8px;"><span style="color: var(--orange);">▸</span> EDM & Special Purpose Machines</li>
            </ul>
        </div>
        <div>
            <h3 style="margin-bottom: 24px; padding-bottom: 8px; border-bottom: 2px solid var(--orange);">CNC Controllers</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">FANUC</div>
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">SIEMENS / SINUMERIK</div>
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">HEIDENHAIN</div>
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">MITSUBISHI</div>
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">MAZATROL / MAZAK</div>
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">HAAS & FAGOR</div>
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">SYNTEC & DELTA</div>
                <div style="padding: 12px; background: #fff; border: 1px solid var(--line); font-size: 14px; font-weight: 600;">HURCO / YASKAWA / BROTHER</div>
            </div>
        </div>
    </div>
</section>

<!-- 8. QUALITY & STANDARDS -->
<section class="section">
    <div class="section-head">
        <div class="tag">Standards</div>
        <h2 class="t-h2">Quality, Accuracy & Standards</h2>
    </div>
    <div style="max-width: 800px; margin-bottom: 40px;">
        <p style="font-size: 18px; color: var(--steel); line-height: 1.6;">Our measurement and calibration work is carried out using appropriate technical methods and applicable machine-tool testing standards.</p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;">
        <div style="padding: 24px; background: var(--grey-l); border-top: 3px solid var(--navy);">
            <h4 style="margin-bottom: 12px;">ISO 230 Series</h4>
            <ul style="list-style: none; color: var(--steel);">
                <li>ISO 230-1</li><li>ISO 230-2</li><li>ISO 230-4</li>
            </ul>
        </div>
        <div style="padding: 24px; background: var(--grey-l); border-top: 3px solid var(--navy);">
            <h4 style="margin-bottom: 12px;">VDI Standards</h4>
            <ul style="list-style: none; color: var(--steel);">
                <li>VDI / VDG 3441</li><li>VDI 2617</li><li>VDI 2852</li>
            </ul>
        </div>
        <div style="padding: 24px; background: var(--grey-l); border-top: 3px solid var(--navy);">
            <h4 style="margin-bottom: 12px;">JIS Standards</h4>
            <ul style="list-style: none; color: var(--steel);">
                <li>JIS B 6201</li><li>JIS B 6330</li><li>JIS B 6190</li>
            </ul>
        </div>
    </div>
</section>

<!-- 10. CONTACT CTA -->
<section class="section navy" style="text-align: center; padding: 100px 44px;">
    <h2 class="t-display" style="margin-bottom: 24px;">Let’s Talk About Your Machine.</h2>
    <p style="font-size: 18px; color: #AAB6C9; max-width: 600px; margin: 0 auto 40px; line-height: 1.6;">
        Whether you are investigating an accuracy problem, planning preventive maintenance or looking for regular calibration support, our team can help you understand the next step.
    </p>
    <div style="display: flex; justify-content: center; gap: 16px;">
        <a class="btn btn-orange" onclick="showPage(5)">Request a Service</a>
        <a class="btn btn-outline" onclick="showPage(5)">Talk to an Engineer</a>
    </div>
</section>

<footer class="site-footer" id="footer-1"></footer>
'''
page1.append(bs4.BeautifulSoup(homepage_content, 'html.parser'))


# 3. Build Page 2 (About Us)
page2 = soup.find(id='page2')
page2.clear()
page2.append(bs4.BeautifulSoup('''
<div class="screen-tag">hexacore.com / about-us</div>
<header class="site-header">
    <div class="brand">
        <div class="hex-mark">HX</div>
        <div class="brand-text">
            <div class="name">HEXACORE</div>
            <div class="sub">Precision Technologies</div>
        </div>
    </div>
    <nav class="main-nav">
        <a onclick="showPage(1)">Home</a>
        <a class="current" onclick="showPage(2)">About Us</a>
        <a onclick="showPage(3)">Products</a>
        <a onclick="showPage(4)">Services &amp; Support</a>
        <a onclick="showPage(5)">Contact</a>
    </nav>
    <a class="nav-cta btn btn-orange" onclick="showPage(5)">GET IN TOUCH</a>
</header>
<section class="section">
    <div class="section-head">
        <div class="tag">About Hexacore Precision Technologies</div>
        <h2 class="t-h2">Experienced. Technical. Trustworthy.</h2>
    </div>
    <div class="about-grid">
        <div class="about-copy">
            <p>Hexacore Precision Technologies is focused on helping manufacturing companies maintain the accuracy, reliability and performance of their machines and production systems.</p>
            <p>Our work combines engineering experience, precision measurement and practical technical support to identify machine performance issues and provide solutions that are suited to the application.</p>
            <p>We work with a wide range of CNC machines and industrial equipment, supporting customers with calibration, machine health assessment, geometric accuracy checks and related technical services.</p>
            <p>Our approach is simple: understand the machine, measure accurately, identify the source of the problem and provide a practical solution that helps the customer maintain consistent production.</p>
        </div>
        <div class="factory-art">
            <img src="images/spider_man.jpeg" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.8; filter: grayscale(100%);">
            <div class="factory-caption">Precision Engineering Operations</div>
        </div>
    </div>
</section>

<section class="section grey">
    <div class="section-head">
        <div class="tag">How We Work</div>
        <h2 class="t-h2">Our Approach</h2>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;">
        <div style="background: #fff; padding: 30px; border: 1px solid var(--line); border-top: 3px solid var(--navy);">
            <div style="font-size: 32px; font-weight: 800; color: var(--orange); margin-bottom: 16px;">01</div>
            <h4 style="margin-bottom: 12px; font-size: 18px;">Understand</h4>
            <p style="color: var(--steel); font-size: 15px;">We first understand the machine, application and performance requirements.</p>
        </div>
        <div style="background: #fff; padding: 30px; border: 1px solid var(--line); border-top: 3px solid var(--navy);">
            <div style="font-size: 32px; font-weight: 800; color: var(--orange); margin-bottom: 16px;">02</div>
            <h4 style="margin-bottom: 12px; font-size: 18px;">Measure</h4>
            <p style="color: var(--steel); font-size: 15px;">We use appropriate measurement and diagnostic methods to assess machine accuracy and condition.</p>
        </div>
        <div style="background: #fff; padding: 30px; border: 1px solid var(--line); border-top: 3px solid var(--navy);">
            <div style="font-size: 32px; font-weight: 800; color: var(--orange); margin-bottom: 16px;">03</div>
            <h4 style="margin-bottom: 12px; font-size: 18px;">Analyse</h4>
            <p style="color: var(--steel); font-size: 15px;">We study the results to identify geometric, positioning, rotary or machine-performance errors.</p>
        </div>
        <div style="background: #fff; padding: 30px; border: 1px solid var(--line); border-top: 3px solid var(--navy);">
            <div style="font-size: 32px; font-weight: 800; color: var(--orange); margin-bottom: 16px;">04</div>
            <h4 style="margin-bottom: 12px; font-size: 18px;">Improve</h4>
            <p style="color: var(--steel); font-size: 15px;">We provide corrective recommendations and support to help restore and maintain machine performance.</p>
        </div>
    </div>
</section>
<footer class="site-footer" id="footer-2"></footer>
''', 'html.parser'))


# 4. Build Page 3 (Products & Technology)
page3 = soup.find(id='page3')
page3.clear()
page3.append(bs4.BeautifulSoup('''
<div class="screen-tag">hexacore.com / products</div>
<header class="site-header">
    <div class="brand">
        <div class="hex-mark">HX</div>
        <div class="brand-text"><div class="name">HEXACORE</div><div class="sub">Precision Technologies</div></div>
    </div>
    <nav class="main-nav">
        <a onclick="showPage(1)">Home</a><a onclick="showPage(2)">About Us</a><a class="current" onclick="showPage(3)">Products</a><a onclick="showPage(4)">Services &amp; Support</a><a onclick="showPage(5)">Contact</a>
    </nav>
    <a class="nav-cta btn btn-orange" onclick="showPage(5)">GET IN TOUCH</a>
</header>
<section class="section">
    <div class="section-head">
        <div class="tag">Technology</div>
        <h2 class="t-h2">Products & Technology</h2>
        <p class="section-lead">Precision measurement equipment, laser calibration technology, and CNC diagnostic solutions for industrial requirements.</p>
    </div>
    <div class="product-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
        <p>Loading products...</p>
    </div>
</section>
<footer class="site-footer" id="footer-3"></footer>
''', 'html.parser'))


# 5. Build Page 4 (Services & Technical Support)
page4 = soup.find(id='page4')
page4.clear()
page4.append(bs4.BeautifulSoup('''
<div class="screen-tag">hexacore.com / services</div>
<header class="site-header">
    <div class="brand">
        <div class="hex-mark">HX</div>
        <div class="brand-text"><div class="name">HEXACORE</div><div class="sub">Precision Technologies</div></div>
    </div>
    <nav class="main-nav">
        <a onclick="showPage(1)">Home</a><a onclick="showPage(2)">About Us</a><a onclick="showPage(3)">Products</a><a class="current" onclick="showPage(4)">Services &amp; Support</a><a onclick="showPage(5)">Contact</a>
    </nav>
    <a class="nav-cta btn btn-orange" onclick="showPage(5)">GET IN TOUCH</a>
</header>
<section class="section">
    <div class="section-head">
        <div class="tag">Calibration & Diagnostics</div>
        <h2 class="t-h2">Services & Technical Support</h2>
        <p class="section-lead">From machine calibration to technical troubleshooting, our services are designed to help manufacturers maintain accuracy and keep production running reliably.</p>
    </div>
    <div class="svc-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
        <p>Loading services...</p>
    </div>
</section>

<section class="section grey">
    <div class="section-head">
        <div class="tag">Reporting</div>
        <h2 class="t-h2">Clear Technical Reports. Better Decisions.</h2>
        <p class="section-lead">After measurement and analysis, we provide clear technical information that helps customers understand the condition of their machine and decide what action is required.</p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;">
        <div style="background: #fff; padding: 24px; border: 1px solid var(--line);">
            <h4 style="margin-bottom: 12px; font-size: 16px;">Measurement Results</h4>
            <p style="color: var(--steel); font-size: 14px;">Detailed positioning accuracy, repeatability, and geometric errors.</p>
        </div>
        <div style="background: #fff; padding: 24px; border: 1px solid var(--line);">
            <h4 style="margin-bottom: 12px; font-size: 16px;">Graphical Results</h4>
            <p style="color: var(--steel); font-size: 14px;">Visual representation of error analysis and rotary-axis results.</p>
        </div>
        <div style="background: #fff; padding: 24px; border: 1px solid var(--line);">
            <h4 style="margin-bottom: 12px; font-size: 16px;">Actionable Advice</h4>
            <p style="color: var(--steel); font-size: 14px;">Corrective recommendations and official calibration records.</p>
        </div>
    </div>
</section>
<footer class="site-footer" id="footer-4"></footer>
''', 'html.parser'))


# 6. Build Page 5 (Contact)
page5 = soup.find(id='page5')
page5.clear()
page5.append(bs4.BeautifulSoup('''
<div class="screen-tag">hexacore.com / contact</div>
<header class="site-header">
    <div class="brand">
        <div class="hex-mark">HX</div>
        <div class="brand-text"><div class="name">HEXACORE</div><div class="sub">Precision Technologies</div></div>
    </div>
    <nav class="main-nav">
        <a onclick="showPage(1)">Home</a><a onclick="showPage(2)">About Us</a><a onclick="showPage(3)">Products</a><a onclick="showPage(4)">Services &amp; Support</a><a class="current" onclick="showPage(5)">Contact</a>
    </nav>
</header>

<section class="section">
    <div class="section-head">
        <div class="tag">Get In Touch</div>
        <h2 class="t-h2">Contact Hexacore Precision Technologies</h2>
    </div>
    
    <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 60px;">
        <!-- Contact Form -->
        <div class="contact-form" style="background: var(--grey-l); padding: 40px; border: 1px solid var(--line); border-radius: 4px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Name</label><input type="text" id="cf-name" placeholder="Your name" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Company</label><input type="text" id="cf-company" placeholder="Company name" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Phone</label><input type="text" id="cf-phone" placeholder="Phone number" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Email</label><input type="email" id="cf-email" placeholder="Email address" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Machine Type</label><input type="text" id="cf-mtype" placeholder="e.g. VMC, CNC Lathe" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Machine Make</label><input type="text" id="cf-mmake" placeholder="e.g. Haas, Mazak" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Machine Model</label><input type="text" id="cf-mmodel" placeholder="Model number" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Controller</label><input type="text" id="cf-ctrl" placeholder="e.g. Fanuc, Siemens" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                <div class="field">
                    <label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Service Required</label>
                    <select id="cf-service" style="width:100%; padding:12px; border:1px solid #ccc;">
                        <option>Linear Laser Calibration</option>
                        <option>Ballbar Test</option>
                        <option>Rotary Axis Calibration</option>
                        <option>Off-Axis Rotary Calibration</option>
                        <option>Axis Straightness Testing</option>
                        <option>Squareness Testing</option>
                        <option>Machine Leveling</option>
                        <option>Servo Tuning</option>
                        <option>Software Troubleshooting</option>
                        <option>Ballscrew Support</option>
                        <option>Preventive Maintenance</option>
                        <option>Other</option>
                    </select>
                </div>
                <div class="field"><label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Location</label><input type="text" id="cf-location" placeholder="City, State" style="width:100%; padding:12px; border:1px solid #ccc;"></div>
            </div>
            <div class="field" style="margin-bottom: 24px;">
                <label style="display:block; margin-bottom:6px; font-weight:600; font-size:13px;">Message</label>
                <textarea id="cf-message" placeholder="Provide any additional details..." style="width:100%; padding:12px; border:1px solid #ccc; height:120px;"></textarea>
            </div>
            
            <div id="cf-status" style="display:none; margin-bottom:16px; padding:12px; font-size:14px; border-radius:4px;"></div>
            <button class="btn btn-orange" id="cf-submit" onclick="submitContact()" style="border:none; width: 100%; justify-content: center; font-size: 15px; cursor: pointer;">Send Enquiry</button>
        </div>
        
        <!-- Contact Info -->
        <div>
            <div style="background: var(--navy); color: #fff; padding: 40px; border-radius: 4px;">
                <h3 style="color: var(--orange); margin-bottom: 24px; text-transform: uppercase;">Reach Us</h3>
                <div style="margin-bottom: 20px;">
                    <strong style="display:block; margin-bottom:4px; font-size:13px; color:#AAB6C9;">Address</strong>
                    No. 1190/1, FD 211, 4th Floor,<br>HSR Layout, Sector 3, 22nd Cross Road,<br>Bengaluru – 560102
                </div>
                <div style="margin-bottom: 20px;">
                    <strong style="display:block; margin-bottom:4px; font-size:13px; color:#AAB6C9;">Phone</strong>
                    +91 44 4567 8900
                </div>
                <div style="margin-bottom: 20px;">
                    <strong style="display:block; margin-bottom:4px; font-size:13px; color:#AAB6C9;">Email</strong>
                    info@hexacoreprecision.com
                </div>
            </div>
        </div>
    </div>
</section>

<footer class="site-footer" id="footer-5"></footer>
''', 'html.parser'))


# 7. Update JS for loadProductsFromAPI and loadServicesFromAPI to work on multiple pages
js_code = soup.find('script')
if js_code:
    js_text = js_code.string
    
    # Update products API inject logic
    js_text = re.sub(
        r"const grid = document\.querySelector\('#page3 \.product-grid'\);",
        "const grids = document.querySelectorAll('.product-grid');",
        js_text
    )
    js_text = re.sub(
        r"if \(\!grid\) return;",
        "if (!grids.length) return;",
        js_text
    )
    js_text = re.sub(
        r"grid\.innerHTML = data\.map\(p => `(.*?)`\)\.join\(''\);",
        r"grids.forEach(g => g.innerHTML = data.map(p => `\1`).join(''));",
        js_text, flags=re.DOTALL
    )

    # Update services API inject logic
    js_text = re.sub(
        r"const grid = document\.querySelector\('#page4 \.svc-grid'\);",
        "const grids = document.querySelectorAll('.svc-grid');",
        js_text
    )
    js_text = re.sub(
        r"if \(\!grid\) return;",
        "if (!grids.length) return;",
        js_text
    )
    js_text = re.sub(
        r"grid\.innerHTML = data\.map\(s => `(.*?)`\)\.join\(''\);",
        r"grids.forEach(g => g.innerHTML = data.map(s => `\1`).join(''));",
        js_text, flags=re.DOTALL
    )

    # Update submitContact to handle new fields and format them into message
    new_submit_js = """
        async function submitContact() {
            const btn  = document.getElementById('cf-submit');
            const stat = document.getElementById('cf-status');
            
            // Gather base fields
            const name = document.getElementById('cf-name').value.trim();
            const company = document.getElementById('cf-company').value.trim();
            const phone = document.getElementById('cf-phone').value.trim();
            const email = document.getElementById('cf-email').value.trim();
            const serviceReq = document.getElementById('cf-service').value;
            
            // Gather new extra fields
            const mType = document.getElementById('cf-mtype').value.trim();
            const mMake = document.getElementById('cf-mmake').value.trim();
            const mModel = document.getElementById('cf-mmodel').value.trim();
            const ctrl = document.getElementById('cf-ctrl').value.trim();
            const loc = document.getElementById('cf-location').value.trim();
            const rawMsg = document.getElementById('cf-message').value.trim();
            
            if (!name || !email) {
                showStatus(stat, 'Please fill in your name and email.', '#ef4444');
                return;
            }
            
            // Concatenate extra fields into the message body so we don't break the DB schema
            let formattedMessage = rawMsg;
            formattedMessage += "\\n\\n--- Technical Details ---";
            if (mType) formattedMessage += "\\nMachine Type: " + mType;
            if (mMake) formattedMessage += "\\nMachine Make: " + mMake;
            if (mModel) formattedMessage += "\\nMachine Model: " + mModel;
            if (ctrl) formattedMessage += "\\nController: " + ctrl;
            if (loc) formattedMessage += "\\nLocation: " + loc;
            if (serviceReq) formattedMessage += "\\nService Required: " + serviceReq;
            
            const body = {
                name: name,
                company: company,
                email: email,
                phone: phone,
                subject: serviceReq, // maps to subject in backend
                message: formattedMessage
            };
            
            btn.textContent = 'Sending...';
            btn.style.pointerEvents = 'none';
            try {
                const res  = await fetch(API_BASE + '/api/contacts', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) });
                const data = await res.json();
                if (res.ok) {
                    showStatus(stat, 'Thank you for contacting Hexacore Precision Technologies. Our team will review your requirement and get back to you shortly.', '#22c55e');
                    ['cf-name','cf-company','cf-phone','cf-email','cf-mtype','cf-mmake','cf-mmodel','cf-ctrl','cf-location','cf-message'].forEach(id => {
                        let el = document.getElementById(id);
                        if (el) el.value = '';
                    });
                    btn.textContent = 'Enquiry Sent ✓';
                } else {
                    throw new Error(data.error);
                }
            } catch (e) {
                showStatus(stat, 'Failed to send. Please try again or call us directly.', '#ef4444');
                btn.textContent = 'Send Enquiry';
                btn.style.pointerEvents = 'auto';
            }
        }
"""
    # Replace the existing submitContact function
    js_text = re.sub(r'async function submitContact\(\) \{.*?\n\s{8}\}', new_submit_js, js_text, flags=re.DOTALL)
    js_code.string = js_text

with open('frontend_new.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
