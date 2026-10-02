import os

coa_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Certificate of Analysis</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 1.5cm;
        }
        body { font-family: Helvetica, Arial, sans-serif; font-size: 11px; }
        
        .disclaimer { font-size: 9px; text-align: justify; margin-top: 15px; }
    </style>
</head>
<body>
    {% for sample in samples %}
    <div>
        <!-- MASTER DOCUMENT CONTROL HEADER -->
        <table border="1" cellpadding="5" cellspacing="0" width="100%" style="text-align: center; margin-bottom: 20px;">
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
        </table>

        <!-- TOP CHECKBOXES -->
        <table border="0" width="100%" style="font-size: 11px; margin-bottom: 10px;">
            <tr>
                <td>
                    [{% if sample.sample_type_category == 'RAW_MATERIAL' %}X{% else %}&nbsp;{% endif %}] Raw Material 
                </td>
                <td>
                    [{% if sample.sample_type_category == 'BATCH_ANALYSIS' %}X{% else %}&nbsp;{% endif %}] Batch Analysis
                </td>
                <td>
                    [{% if sample.sample_type_category == 'OUTSIDE_SAMPLE' %}X{% else %}&nbsp;{% endif %}] Outside Sample
                </td>
            </tr>
        </table>

        <!-- INFO GRID -->
        <table border="0" cellpadding="3" cellspacing="0" width="100%" style="font-size: 10px; margin-bottom: 10px;">
            <tr>
                <td width="50%"><strong>Issue Date:</strong> <u>{% now "d-M-Y" %}</u></td>
                <td width="50%"><strong>Issue status:</strong> <u>{{ sample.get_status_display }}</u></td>
            </tr>
            <tr>
                <td><strong>Item Name:</strong> <u>{{ sample.product_name }}</u></td>
                <td><strong>Standard Reference:</strong> <u>{{ sample.standard_reference|default:"-" }}</u></td>
            </tr>
            <tr>
                <td><strong>Source:</strong> <u>{{ sample.source|default:"Vital Agri Nutrients (Pvt) Ltd" }}</u></td>
                <td><strong>Company:</strong> <u>{{ sample.customer_org|default:sample.client.name }}</u></td>
            </tr>
            <tr>
                <td><strong>Batch No:</strong> <u>{{ sample.batch_number|default:"-" }}</u></td>
                <td><strong>Quantity:</strong> <u>{{ sample.sample_quantity|default:"-" }}</u></td>
            </tr>
            <tr>
                <td><strong>Mfg. Date:</strong> <u>{{ sample.mfg_date|date:"d-M-Y"|default:"N/A" }}</u></td>
                <td><strong>Exp. Date:</strong> <u>{{ sample.exp_date|date:"d-M-Y"|default:"N/A" }}</u></td>
            </tr>
            <tr>
                <td><strong>Q.C. No:</strong> <u>{{ sample.sample_id }}</u></td>
                <td><strong>Receiving Date:</strong> <u>{{ sample.received_date|date:"d-M-Y" }}</u></td>
            </tr>
            <tr>
                <td><strong>Sampled Received by:</strong> <u>{{ sample.received_by.username|default:"-" }}</u></td>
                <td><strong>Sample Quantity:</strong> <u>{{ sample.sample_quantity|default:"-" }}</u></td>
            </tr>
            <tr>
                <td><strong>Analysis Time:</strong> <u>{{ sample.approved_at|date:"H:i"|default:"-" }}</u></td>
                <td><strong>Date of Test:</strong> <u>{{ sample.approved_at|date:"d-M-Y"|default:"-" }}</u></td>
            </tr>
            <tr>
                <td><strong>Temperature ˚C:</strong> <u>{{ sample.temperature|default:"-" }}</u></td>
                <td><strong>Humidity %:</strong> <u>{{ sample.humidity|default:"-" }}</u></td>
            </tr>
        </table>

        <!-- RESULTS GRID -->
        <table border="1" cellpadding="4" cellspacing="0" width="100%" style="font-size: 10px; margin-bottom: 15px; text-align: left;">
            <thead>
                <tr style="background-color: #f2f2f2; font-weight: bold; text-align: center;">
                    <th width="30%">TEST</th>
                    <th width="15%">SPECS</th>
                    <th width="15%">RESULTS</th>
                    <th width="20%">METHODS</th>
                    <th width="10%">MU (%)</th>
                    <th width="10%">REMARKS</th>
                </tr>
            </thead>
            <tbody>
                <!-- PHYSICAL PARAMETER SECTION -->
                <tr style="background-color: #e8e8e8; font-weight: bold;">
                    <td colspan="6">PHYSICAL PARAMETER</td>
                </tr>
                {% for test in sample.test_results.all %}
                    {% if 'Physical' in test.parameter.name or 'Color' in test.parameter.name or 'Density' in test.parameter.name or 'Solubility' in test.parameter.name or 'Insoluble' in test.parameter.name %}
                    <tr>
                        <td>[x] {{ test.parameter.name }}</td>
                        <td>{{ test.specs|default:"-" }}</td>
                        <td>{{ test.result_value|default:"-" }} {{ test.unit }}</td>
                        <td>{{ test.method.name|default:"-" }}</td>
                        <td>{{ test.measurement_uncertainty|default:"-" }}</td>
                        <td>{{ test.notes|default:"-" }}</td>
                    </tr>
                    {% endif %}
                {% endfor %}

                <!-- CHEMICAL PARAMETER SECTION -->
                <tr style="background-color: #e8e8e8; font-weight: bold;">
                    <td colspan="6">CHEMICAL PARAMETER &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Assay: __________________</td>
                </tr>
                {% for test in sample.test_results.all %}
                    {% if 'Physical' not in test.parameter.name and 'Color' not in test.parameter.name and 'Density' not in test.parameter.name and 'Solubility' not in test.parameter.name and 'Insoluble' not in test.parameter.name %}
                    <tr>
                        <td>[x] {{ test.parameter.name }}</td>
                        <td>{{ test.specs|default:"-" }}</td>
                        <td>{{ test.result_value|default:"-" }} {{ test.unit }}</td>
                        <td>{{ test.method.name|default:"-" }}</td>
                        <td>{{ test.measurement_uncertainty|default:"-" }}</td>
                        <td>{{ test.notes|default:"-" }}</td>
                    </tr>
                    {% endif %}
                {% endfor %}
            </tbody>
        </table>

        <!-- DISCLAIMER -->
        <div class="disclaimer">
            <strong>Report Disclaimer</strong><br/>
            This test result is based solely on the particular sample supplied by the client. VAN QC Lab doesn't involve in any type of sampling activity.<br/>
            The results are reported with a confidence level of 95%; i.e. [K=2] and are pertaining to analyzed sample(s) only.<br/>
            Provided sample will be retained for 15 days period...
        </div>

        <!-- SIGNATURES -->
        <table border="0" width="100%" style="margin-top: 40px; text-align: center; font-size: 10px;">
            <tr>
                <td width="33%">
                    ________________________<br/>
                    <strong>Analyst</strong>
                </td>
                <td width="33%">
                    ________________________<br/>
                    <strong>Verified By (AQCM)</strong>
                </td>
                <td width="33%">
                    ________________________<br/>
                    <strong>Approved By (QCM)</strong>
                </td>
            </tr>
        </table>
        
        {% if not forloop.last %}
            <pdf:nextpage />
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
"""

with open(coa_path, 'w') as f:
    f.write(html_content)
