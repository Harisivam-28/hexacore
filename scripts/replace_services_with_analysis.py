import os, re, glob

def replace_in_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Title tags & page titles
    content = content.replace('Service Details | Hexacore', 'Analysis Details | Hexacore')
    content = content.replace('Services &amp; Support | Hexacore', 'Analysis &amp; Support | Hexacore')
    content = content.replace('Services & Support | Hexacore', 'Analysis & Support | Hexacore')

    # 2. Main Navigation links & text
    content = content.replace('>Service &amp; Support<', '>Analysis &amp; Support<')
    content = content.replace('>Service & Support<', '>Analysis & Support<')
    content = content.replace('>Services &amp; Support<', '>Analysis &amp; Support<')
    content = content.replace('>Services & Support<', '>Analysis & Support<')
    content = content.replace('>Services<', '>Analysis<')

    # 3. Headings, tags, section titles & CTA buttons
    content = content.replace('Explore Our Services', 'Explore Our Analysis')
    content = content.replace('Services &amp; Technical Support', 'Analysis &amp; Technical Support')
    content = content.replace('Services & Technical Support', 'Analysis & Technical Support')
    content = content.replace('Precision Metrology &amp; Machine Services', 'Precision Metrology &amp; Machine Analysis')
    content = content.replace('Precision Metrology & Machine Services', 'Precision Metrology & Machine Analysis')
    content = content.replace('Machine Services &amp; Calibration', 'Machine Analysis &amp; Calibration')
    content = content.replace('Machine Services & Calibration', 'Machine Analysis & Calibration')
    content = content.replace('View Machine Services', 'View Machine Analysis')
    content = content.replace('CMM Services &amp; Error Mapping', 'CMM Analysis &amp; Error Mapping')
    content = content.replace('CMM Services & Error Mapping', 'CMM Analysis & Error Mapping')
    content = content.replace('View CMM Services', 'View CMM Analysis')
    content = content.replace('Metrology Instruments Services', 'Metrology Instruments Analysis')
    content = content.replace('View Instrument Services', 'View Instrument Analysis')
    content = content.replace('Services Overview', 'Analysis Overview')
    content = content.replace('Service Details &amp; Specifications', 'Analysis Details &amp; Specifications')
    content = content.replace('Service Details & Specifications', 'Analysis Details & Specifications')
    content = content.replace('View Full Service Details', 'View Full Analysis Details')
    content = content.replace('Explore Related Metrology &amp; Calibration Services', 'Explore Related Metrology &amp; Calibration Analysis')
    content = content.replace('Explore Related Metrology & Calibration Services', 'Explore Related Metrology & Calibration Analysis')
    content = content.replace('Calibration Services', 'Calibration Analysis')
    content = content.replace('CMM Services', 'CMM Analysis')
    content = content.replace('Quality Instruments Services', 'Quality Instruments Analysis')
    content = content.replace('Machine Service', 'Machine Analysis')
    content = content.replace('Product / Service Selected', 'Product / Analysis Selected')

    # 4. Admin Navigation & titles
    content = content.replace('<span>Services</span>', '<span>Analysis</span>')
    content = content.replace('Add Service', 'Add Analysis')
    content = content.replace('Edit Service', 'Edit Analysis')
    content = content.replace('Delete Service', 'Delete Analysis')
    content = content.replace('No services yet', 'No analysis records yet')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ Updated visible "Services" -> "Analysis" in {fpath}')
    else:
        print(f'ℹ️ No changes needed in {fpath}')

files = ['index.html', 'about.html', 'contact.html', 'products.html', 'services.html', 'service.html', 'frontend.html', 'admin/index.html', 'src/js/main.js', 'src/js/api.js']

for fpath in files:
    if os.path.exists(fpath):
        replace_in_file(fpath)
