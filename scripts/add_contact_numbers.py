import os, re, glob

# Old phone string
old_phone_line = '<li>+91 44 4567 8900</li>'
new_phone_line = '<li><a href="tel:+917339015820" style="color:#ffffff;text-decoration:none;">+91 73390 15820</a> &nbsp;|&nbsp; <a href="tel:+919094479695" style="color:#ffffff;text-decoration:none;">+91 90944 79695</a></li>'

old_phone_raw = '+91 44 4567 8900'
new_phone_formatted = '<a href="tel:+917339015820" style="color:#ffffff;text-decoration:none;">+91 73390 15820</a> &nbsp;|&nbsp; <a href="tel:+919094479695" style="color:#ffffff;text-decoration:none;">+91 90944 79695</a>'

files = glob.glob('*.html') + ['admin/index.html', 'src/js/api.js', 'src/js/main.js']

for fpath in files:
    if not os.path.exists(fpath): continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace footer phone line
    content = content.replace(old_phone_line, new_phone_line)

    # Replace contact card phone line in contact.html & service.html
    content = re.sub(
        r'<strong\s+style="display:block;\s*margin-bottom:4px;\s*font-size:13px;\s*color:#AAB6C9;">Phone</strong>\s*\+91 44 4567 8900',
        r'<strong style="display:block; margin-bottom:4px; font-size:13px; color:#AAB6C9;">Phone</strong>\n                            <a href="tel:+917339015820" style="color:#ffffff;text-decoration:none;">+91 73390 15820</a><br><a href="tel:+919094479695" style="color:#ffffff;text-decoration:none;">+91 90944 79695</a>',
        content
    )

    # Replace standalone phone text in service.html contact sections
    content = content.replace('📞 Phone: +91 44 4567 8900', '📞 Phone: +91 73390 15820 / +91 90944 79695')
    content = content.replace('<span>+91 44 4567 8900</span>', '<span>+91 73390 15820 / +91 90944 79695</span>')

    # Replace Schema.org telephone string
    content = content.replace('"telephone": "+91-44-4567-8900"', '"telephone": "+91 73390 15820, +91 90944 79695"')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ Updated contact numbers in {fpath}')
    else:
        print(f'ℹ️ No changes needed in {fpath}')
