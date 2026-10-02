import os

ar_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/analysis_request.html'
with open(ar_path, 'r') as f:
    content = f.read()

# Make sure we load static
if "{% load static %}" not in content:
    content = content.replace("<body>", "<body>\n    {% load static %}")

old_header = """        <!-- MASTER DOCUMENT CONTROL HEADER -->
        <table style="width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; font-family: Arial, sans-serif;">
            <tr>
                <td rowspan="3" style="width: 20%; border: 1px solid #000; padding: 5px;">
                    <strong>VITAL AGRI NUTRIENTS</strong><br>QC LABORATORY
                </td>
                <td rowspan="2" style="width: 50%; border: 1px solid #000; font-size: 18px; font-weight: bold; padding: 5px;">
                    ANALYSIS REQUEST
                </td>
                <td style="width: 30%; border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Format No:</strong> QCL-FRM-12.01
                </td>
            </tr>
            <tr>
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Revision No:</strong> 02
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
        </table>"""

new_header = """        <!-- MASTER DOCUMENT CONTROL HEADER -->
        <table style="width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; font-family: Arial, sans-serif;">
            <tr>
                <td rowspan="3" style="width: 15%; border: 1px solid #000; padding: 5px; text-align: center; vertical-align: middle;">
                    <img src="{% static 'images/logo1.png' %}" width="60" height="60" alt="PNAC Logo" />
                </td>
                <td rowspan="3" style="width: 15%; border: 1px solid #000; padding: 5px; text-align: center; vertical-align: middle;">
                    <img src="{% static 'images/logo2.png' %}" width="60" height="60" alt="VAN Logo" />
                </td>
                <td rowspan="2" style="width: 45%; border: 1px solid #000; font-size: 16px; font-weight: bold; padding: 5px;">
                    VITAL AGRI NUTRIENTS QC LAB<br/>
                    ANALYSIS REQUEST
                </td>
                <td style="width: 25%; border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Format No:</strong> QCL-FRM-12.01
                </td>
            </tr>
            <tr>
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Revision No:</strong> 02
                </td>
            </tr>
            <tr>
                <td style="border: 1px solid #000; font-size: 11px; font-weight: bold; padding: 5px;">
                    ISO/IEC 17025 Accredited
                </td>
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px; font-size: 10px;">
                    <strong>Page:</strong> 1 of 1
                </td>
            </tr>
        </table>"""

content = content.replace(old_header, new_header)
with open(ar_path, 'w') as f:
    f.write(content)
