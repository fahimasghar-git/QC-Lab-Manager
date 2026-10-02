import os

file_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
with open(file_path, 'r') as f:
    content = f.read()

# I want to add a footer to the CoA with the official Form Number.
# The footer in xhtml2pdf is defined in the @page CSS.
css_old = """        @page {
            size: a4 portrait;
            margin: 2cm;
        }"""
css_new = """        @page {
            size: a4 portrait;
            margin: 2cm;
            @frame footer_frame {
                -pdf-frame-content: footer_content;
                left: 2cm; width: 17cm; top: 27cm; height: 2cm;
            }
        }"""

content = content.replace(css_old, css_new)

# Add the footer div right after <body>
footer_div = """<body>
    <div id="footer_content" style="text-align: left; font-size: 8pt; border-top: 1px solid #000; padding-top: 5px; color: #555;">
        <table width="100%">
            <tr>
                <td align="left"><strong>Format No:</strong> QCL-FRM-12.03</td>
                <td align="center"><strong>Revision No:</strong> 04</td>
                <td align="right"><strong>Page:</strong> <pdf:pagenumber> of <pdf:pagecount></td>
            </tr>
        </table>
    </div>"""

content = content.replace('<body>', footer_div)

# Change header to look more like their QCL lab
content = content.replace('<h1>CERTIFICATE OF ANALYSIS</h1>', '<h1>CERTIFICATE OF ANALYSIS</h1>\n        <p style="text-align: center; margin-top: -10px; font-size: 10pt; color: #555;">Quality Control Laboratory</p>')

with open(file_path, 'w') as f:
    f.write(content)
