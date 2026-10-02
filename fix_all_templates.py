import os
import re

template_dirs = [
    '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates',
    '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates'
]

# The broken @page CSS pattern
old_page_pattern = r'@page\s*{\s*size:\s*A4\s*landscape;\s*margin:\s*1\.5cm;\s*@frame\s*header_frame\s*{\s*-pdf-frame-content:\s*header_content;\s*top:\s*1\.5cm;\s*left:\s*1\.5cm;\s*right:\s*1\.5cm;\s*height:\s*3cm;\s*}\s*@frame\s*footer_frame\s*{\s*-pdf-frame-content:\s*footer_content;\s*bottom:\s*1cm;\s*left:\s*1\.5cm;\s*right:\s*1\.5cm;\s*height:\s*1cm;\s*}\s*}'

new_page_css = """@page {
            size: a4 landscape;
            margin-top: 4cm;
            margin-bottom: 2cm;
            margin-left: 1.5cm;
            margin-right: 1.5cm;
            @frame header_frame {
                -pdf-frame-content: header_content;
                left: 1.5cm; right: 1.5cm; top: 1cm; height: 3cm;
            }
            @frame footer_frame {
                -pdf-frame-content: footer_content;
                left: 1.5cm; right: 1.5cm; bottom: 0.5cm; height: 1cm;
            }
        }"""
        
# For portrait pages
old_page_portrait = r'@page\s*{\s*size:\s*A4\s*portrait;\s*margin:\s*1\.5cm;\s*@frame\s*header_frame\s*{\s*-pdf-frame-content:\s*header_content;\s*top:\s*1\.5cm;\s*left:\s*1\.5cm;\s*right:\s*1\.5cm;\s*height:\s*3cm;\s*}\s*@frame\s*footer_frame\s*{\s*-pdf-frame-content:\s*footer_content;\s*bottom:\s*1cm;\s*left:\s*1\.5cm;\s*right:\s*1\.5cm;\s*height:\s*1cm;\s*}\s*}'
new_page_portrait = """@page {
            size: a4 portrait;
            margin-top: 4cm;
            margin-bottom: 2cm;
            margin-left: 1.5cm;
            margin-right: 1.5cm;
            @frame header_frame {
                -pdf-frame-content: header_content;
                left: 1.5cm; right: 1.5cm; top: 1cm; height: 3cm;
            }
            @frame footer_frame {
                -pdf-frame-content: footer_content;
                left: 1.5cm; right: 1.5cm; bottom: 0.5cm; height: 1cm;
            }
        }"""

count = 0
for d in template_dirs:
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                original = content
                
                # 1. Replace logo.png with logo1.png
                content = content.replace('static/images/logo.png', 'static/images/logo1.png')
                
                # 2. Fix the width percentages in style
                content = content.replace('style="width: 20%;"', 'width="20%"')
                content = content.replace('style="width: 50%; font-size: 16px; font-weight: bold;"', 'width="50%" style="font-size: 16px; font-weight: bold;"')
                content = content.replace('style="width: 30%; text-align: left;"', 'width="30%" style="text-align: left;"')
                
                # 3. Fix @page CSS (Landscape)
                content = re.sub(old_page_pattern, new_page_css, content, flags=re.DOTALL)
                # Fix @page CSS (Portrait)
                content = re.sub(old_page_portrait, new_page_portrait, content, flags=re.DOTALL)
                
                if content != original:
                    with open(filepath, 'w') as f:
                        f.write(content)
                    count += 1

print(f"Fixed CSS and logos in {count} templates.")
