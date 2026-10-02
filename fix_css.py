import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates/management/non_conformance_log.html'
with open(path, 'r') as f:
    content = f.read()

# Replace the @page block
old_page = """        @page {
            size: A4 landscape;
            margin: 1.5cm;
            @frame header_frame {
                -pdf-frame-content: header_content;
                top: 1.5cm; left: 1.5cm; right: 1.5cm; height: 3cm;
            }
            @frame footer_frame {
                -pdf-frame-content: footer_content;
                bottom: 1cm; left: 1.5cm; right: 1.5cm; height: 1cm;
            }
        }"""

new_page = """        @page {
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
content = content.replace(old_page, new_page)

# Change the logo to logo1.png
content = content.replace('logo.png', 'logo1.png')

with open(path, 'w') as f:
    f.write(content)
