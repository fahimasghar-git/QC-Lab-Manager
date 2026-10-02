import os

def generate_header(title, format_no, revision):
    return f"""        <!-- MASTER DOCUMENT CONTROL HEADER -->
        <table style="width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; font-family: Arial, sans-serif;">
            <tr>
                <td rowspan="3" style="width: 20%; border: 1px solid #000; padding: 5px;">
                    <strong>VITAL AGRI NUTRIENTS</strong><br>QC LABORATORY
                </td>
                <td rowspan="2" style="width: 50%; border: 1px solid #000; font-size: 18px; font-weight: bold; padding: 5px;">
                    {title}
                </td>
                <td style="width: 30%; border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Format No:</strong> {format_no}
                </td>
            </tr>
            <tr>
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Revision No:</strong> {revision}
                </td>
            </tr>
            <tr>
                <td style="border: 1px solid #000; font-size: 12px; font-weight: bold; padding: 5px;">
                    ISO/IEC 17025 Accredited
                </td>
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Page:</strong> 1 of 1
                </td>
            </tr>
        </table>
        <!-- END MASTER HEADER -->"""

# 1. Update analysis_request.html
ar_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/analysis_request.html'
with open(ar_path, 'r') as f:
    ar_content = f.read()

# Remove old footer
ar_content = ar_content.split('<div style="margin-top: 20px; font-size: 10px; border-top: 1px solid #000; padding-top: 5px;">')[0] + "    </div>\n    {% endfor %}\n</body>\n</html>"

# Replace old header with new master header
old_ar_header = """        <div style="text-align: center; font-weight: bold; font-size: 16px; text-decoration: underline; margin-bottom: 20px;">
            ANALYSIS REQUEST
        </div>"""
ar_content = ar_content.replace(old_ar_header, generate_header("ANALYSIS REQUEST", "QCL-FRM-12.01", "02"))

with open(ar_path, 'w') as f:
    f.write(ar_content)


# 2. Update certificate_of_analysis.html
coa_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
with open(coa_path, 'r') as f:
    coa_content = f.read()

# Remove xhtml2pdf footer frames and divs
coa_css_old = """            @frame footer_frame {
                -pdf-frame-content: footer_content;
                left: 2cm; width: 17cm; top: 27cm; height: 1.5cm;
            }"""
coa_content = coa_content.replace(coa_css_old, "")

coa_footer_div = """    <div id="footer_content" style="text-align: left; font-size: 8pt; border-top: 1px solid #000; padding-top: 5px; color: #555;">
        <table width="100%">
            <tr>
                <td align="left"><strong>Format No:</strong> QCL-FRM-12.03</td>
                <td align="center"><strong>Revision No:</strong> 04</td>
                <td align="right"><strong>Page:</strong> <pdf:pagenumber> of <pdf:pagecount></td>
            </tr>
        </table>
    </div>"""
coa_content = coa_content.replace(coa_footer_div, "")

old_coa_header = """        <div class="header">
            <h1>CERTIFICATE OF ANALYSIS</h1>
            <p style="margin-top: -10px; font-size: 12px; font-weight: bold;">Quality Control Laboratory</p>
        </div>"""
coa_content = coa_content.replace(old_coa_header, generate_header("CERTIFICATE OF ANALYSIS", "QCL-FRM-12.03", "04"))

# Fix the page number in the header for PDF
coa_content = coa_content.replace("<strong>Page:</strong> 1 of 1", "<strong>Page:</strong> <pdf:pagenumber> of <pdf:pagecount>")

with open(coa_path, 'w') as f:
    f.write(coa_content)

