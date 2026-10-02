import os

coa_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
with open(coa_path, 'r') as f:
    content = f.read()

# I will replace the top left cell of the header table with a grid that holds the logos.
# In my previous script, the first TD in the header table was:
# <td rowspan="3" width="25%">
#     <strong>VITAL AGRI NUTRIENTS</strong><br/>QC LABORATORY
# </td>

# Let's replace the whole header table with a 4-column one to accommodate logos.
old_header = """        <table border="1" cellpadding="5" cellspacing="0" width="100%" style="text-align: center; margin-bottom: 20px;">
            <tr>
                <td rowspan="3" width="25%">
                    <strong>VITAL AGRI NUTRIENTS</strong><br/>QC LABORATORY
                </td>
                <td rowspan="2" width="45%" style="font-size: 16px; font-weight: bold;">
                    CERTIFICATE OF ANALYSIS
                </td>
                <td width="30%" align="left" style="font-size: 9px;">
                    <strong>Format No:</strong> QCL-FRM-12.03
                </td>
            </tr>
            <tr>
                <td align="left" style="font-size: 9px;">
                    <strong>Revision No:</strong> 04
                </td>
            </tr>
            <tr>
                <td style="font-size: 11px; font-weight: bold;">
                    ISO/IEC 17025 Accredited
                </td>
                <td align="left" style="font-size: 9px;">
                    <strong>Page:</strong> <pdf:pagenumber> of <pdf:pagecount>
                </td>
            </tr>
        </table>"""

new_header = """        <table border="1" cellpadding="5" cellspacing="0" width="100%" style="text-align: center; margin-bottom: 20px;">
            <tr>
                <td rowspan="3" width="15%" style="text-align: center; vertical-align: middle;">
                    <!-- PNAC Logo (Left) -->
                    <img src="/Users/fahimasghar/Documents/QC-Lab-Manager/static/images/logo1.png" width="60" height="60" />
                </td>
                <td rowspan="3" width="15%" style="text-align: center; vertical-align: middle;">
                    <!-- VAN Horse Logo (Right) -->
                    <img src="/Users/fahimasghar/Documents/QC-Lab-Manager/static/images/logo2.png" width="60" height="60" />
                </td>
                <td rowspan="2" width="45%" style="font-size: 16px; font-weight: bold;">
                    VITAL AGRI NUTRIENTS QC LAB<br/>
                    CERTIFICATE OF ANALYSIS
                </td>
                <td width="25%" align="left" style="font-size: 9px;">
                    <strong>Format No:</strong> QCL-FRM-12.03
                </td>
            </tr>
            <tr>
                <td align="left" style="font-size: 9px;">
                    <strong>Revision No:</strong> 04
                </td>
            </tr>
            <tr>
                <td style="font-size: 11px; font-weight: bold;">
                    ISO/IEC 17025 Accredited
                </td>
                <td align="left" style="font-size: 9px;">
                    <strong>Page:</strong> <pdf:pagenumber> of <pdf:pagecount>
                </td>
            </tr>
        </table>"""

content = content.replace(old_header, new_header)
with open(coa_path, 'w') as f:
    f.write(content)
