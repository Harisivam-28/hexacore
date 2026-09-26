import os, re, glob

# WhatsApp wa.me link replacement
old_link = '914445678900'
new_link = '917339015820'

files_to_update = glob.glob('*.html') + glob.glob('src/**/*.*', recursive=True) + ['admin/index.html', 'scripts/make_popup_smaller.py']

for fpath in files_to_update:
    if not os.path.isfile(fpath): continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_link in content:
        content = content.replace(old_link, new_link)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated WhatsApp phone number in {fpath}')
