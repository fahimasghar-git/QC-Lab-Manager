import os

template_dirs = [
    '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates'
]

# We will use Django's local static root or absolute path. 
# xhtml2pdf handles absolute paths like /Users/fahimasghar/.../static/images/logo.png perfectly.
absolute_logo_path = "/Users/fahimasghar/Documents/QC-Lab-Manager/static/images/logo.png"

old_img_src = '{{ request.scheme }}://{{ request.get_host }}/static/images/logo.png'
old_img_src_2 = 'http://{{ request.get_host }}/static/images/logo.png'

count = 0
for d in template_dirs:
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                new_content = content.replace(old_img_src, absolute_logo_path).replace(old_img_src_2, absolute_logo_path)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    count += 1
print(f"Fixed logo path in {count} templates.")
