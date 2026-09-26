import os, glob

files = [
    'index.html',
    'about.html',
    'contact.html',
    'products.html',
    'services.html',
    'service.html',
    'frontend.html',
    'admin/index.html',
    'src/js/main.js',
    'src/js/api.js'
]

for fpath in files:
    if not os.path.exists(fpath): continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace('Analysis', 'Analyse')
    content = content.replace('ANALYSIS', 'ANALYSE')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ Updated spelling "Analysis" -> "Analyse" in {fpath}')
    else:
        print(f'ℹ️ No changes needed in {fpath}')
