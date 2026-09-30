import os
import re

files_to_update = [
    'index.html',
    'about.html',
    'services.html',
    'service.html',
    'products.html',
    'contact.html',
    'frontend.html',
    'newsletter.html',
    'quote.html',
    'admin/index.html'
]

replacements = [
    # Canonical URLs
    (r'<link rel="canonical" href="https://xacore.com/services.html" />', r'<link rel="canonical" href="https://hexacoreprecision.com/services" />'),
    (r'<link rel="canonical" href="https://xacore.com/" />', r'<link rel="canonical" href="https://hexacoreprecision.com/" />'),

    # Navigation & Link hrefs
    (r'href="index.html"', r'href="/"'),
    (r'href="about.html"', r'href="/about"'),
    (r'href="services.html"', r'href="/services"'),
    (r'href="service.html\?', r'href="/service?'),
    (r'href="service.html"', r'href="/service"'),
    (r'href="products.html"', r'href="/products"'),
    (r'href="product.html"', r'href="/products"'),
    (r'href="contact.html"', r'href="/contact"'),
    (r'href="newsletter.html"', r'href="/about#newsletter-section"'),
    (r'href="quote.html"', r'href="/contact"'),

    # JavaScript window.location & page maps
    (r'window\.location\.href = `service\.html\?', r'window.location.href = `/service?'),
    (r"window\.location\.href = 'services\.html'", r"window.location.href = '/services'"),
    (r'window\.location\.href = "about\.html#newsletter-section"', r'window.location.href = "/about#newsletter-section"'),
    (r'window\.location\.href = "contact\.html"', r'window.location.href = "/contact"'),
    (r'url=about\.html#newsletter-section', r'url=/about#newsletter-section'),
    (r'url=contact\.html', r'url=/contact'),
    (r"const pages = \{ 1: 'index\.html', 2: 'about\.html', 3: 'products\.html', 4: 'services\.html', 5: 'contact\.html', 7: 'newsletter\.html' \};",
     r"const pages = { 1: '/', 2: '/about', 3: '/products', 4: '/services', 5: '/contact', 7: '/about#newsletter-section' };"),
    
    # Admin link
    (r'href="/frontend\.html"', r'href="/"'),
]

for file_path in files_to_update:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")
