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
        
        .header-table { width: 100%; border-collapse: collapse; border: 2px solid #000; margin-bottom: 20px; text-align: center; }
        .header-table td { border: 1px solid #000; padding: 5px; }
        
        .info-table { width: 100%; border-collapse: collapse; font-size: 10px; margin-bottom: 10px; }
        .info-table td { border: none; padding: 3px; }
        .info-table .uline { border-bottom: 1px solid #000; display: inline-block; width: 150px; text-align: center; }
        
        .results-table { width: 100%; border-collapse: collapse; font-size: 10px; margin-bottom: 15px; }
        .results-table th, .results-table td { border: 1px solid #000; padding: 4px; text-align: left; }
        .results-table th { background-color: #f2f2f2; font-weight: bold; text-align: center; }
        .results-table .category-row { font-weight: bold; background-color: #e8e8e8; text-transform: uppercase; }
        
        .checkbox-box { display: inline-block; width: 10px; height: 10px; border: 1px solid #000; margin-right: 5px; text-align: center; line-height: 10px; font-size: 10px; }
        
        .signatures { width: 100%; margin-top: 30px; text-align: center; font-size: 10px; }
        .signatures td { padding: 5px; }
        
        .disclaimer { font-size: 9px; text-align: justify; margin-top: 10px; }
    </style>
</head>
<body>
    {% for sample in samples %}
    <div style="page-break-after: always;">
        <!-- MASTER DOCUMENT CONTROL HEADER -->
        <table class="header-table">
            <tr>
                <td rowspan="3" style="width: 20%;">
                    <strong>VITAL AGRI NUTRIENTS</strong><br>QC LABORATORY
                </td>
                <td rowspan="2" style="width: 50%; font-size: 16px; font-weight: bold;">
                    CERTIFICATE OF ANALYSIS
                </td>
                <td style="width: 30%; text-align: left; font-size: 9px;">
                    <strong>Format No:</strong> QCL-FRM-12.03
                </td>
            </tr>
            <tr>
                <td style="text-align: left; font-size: 9px;">
                    <strong>Revision No:</strong> 04
                </td>
            </tr>
            <tr>
                <td style="font-size: 11px; font-weight: bold;">
                    ISO/IEC 17025 Accredited
                </td>
                <td style="text-align: left; font-size: 9px;">
                    <strong>Page:</strong> 1 of 1
                </td>
            </tr>
        </table>

        <!-- TOP CHECKBOXES -->
        <div style="margin-bottom: 10px; font-size: 11px;">
            <span class="checkbox-box">{% if sample.sample_type_category == 'RAW_MATERIAL' %}x{% else %}&nbsp;{% endif %}</span> Raw Material &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span class="checkbox-box">{% if sample.sample_type_category == 'BATCH_ANALYSIS' %}x{% else %}&nbsp;{% endif %}</span> Batch Analysis &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span class="checkbox-box">{% if sample.sample_type_category == 'OUTSIDE_SAMPLE' %}x{% else %}&nbsp;{% endif %}</span> Outside Sample
        </div>

        <!-- INFO GRID -->
        <table class="info-table">
            <tr>
                <td width="50%"><strong>Issue Date:</strong> <span class="uline">{% now "d-M-Y" %}</span></td>
                <td width="50%"><strong>Issue status:</strong> <span class="uline">{{ sample.get_status_display }}</span></td>
            </tr>
            <tr>
                <td><strong>Item Name:</strong> <span class="uline" style="width:200px;">{{ sample.product_name }}</span></td>
                <td><strong>Standard Reference:</strong> <span class="uline">{{ sample.standard_reference|default:"-" }}</span></td>
            </tr>
            <tr>
                <td><strong>Source:</strong> <span class="uline" style="width:220px;">{{ sample.source|default:"Vital Agri Nutrients (Pvt) Ltd" }}</span></td>
                <td><strong>Company:</strong> <span class="uline">{{ sample.customer_org|default:sample.client.name }}</span></td>
            </tr>
            <tr>
                <td><strong>Batch No:</strong> <span class="uline">{{ sample.batch_number|default:"-" }}</span></td>
                <td><strong>Quantity:</strong> <span class="uline">{{ sample.sample_quantity|default:"-" }}</span></td>
            </tr>
            <tr>
                <td><strong>Mfg. Date:</strong> <span class="uline">{{ sample.mfg_date|date:"d-M-Y"|default:"N/A" }}</span></td>
                <td><strong>Exp. Date:</strong> <span class="uline">{{ sample.exp_date|date:"d-M-Y"|default:"N/A" }}</span></td>
            </tr>
            <tr>
                <td><strong>Q.C. No:</strong> <span class="uline">{{ sample.sample_id }}</span></td>
                <td><strong>Receiving Date:</strong> <span class="uline">{{ sample.received_date|date:"d-M-Y" }}</span></td>
            </tr>
            <tr>
                <td><strong>Sampled Received by:</strong> <span class="uline">{{ sample.received_by.username|default:"-" }}</span></td>
                <td><strong>Sample Quantity:</strong> <span class="uline">{{ sample.sample_quantity|default:"-" }}</span></td>
            </tr>
            <tr>
                <td><strong>Analysis Time:</strong> <span class="uline">{{ sample.approved_at|date:"H:i"|default:"-" }}</span></td>
                <td><strong>Date of Test:</strong> <span class="uline">{{ sample.approved_at|date:"d-M-Y"|default:"-" }}</span></td>
            </tr>
            <tr>
                <td><strong>Temperature ˚C:</strong> <span class="uline">{{ sample.temperature|default:"-" }}</span></td>
                <td><strong>Humidity %:</strong> <span class="uline">{{ sample.humidity|default:"-" }}</span></td>
            </tr>
        </table>

        <!-- RESULTS GRID -->
        <table class="results-table">
            <thead>
                <tr>
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
                <tr>
                    <td colspan="6" class="category-row">PHYSICAL PARAMETER</td>
                </tr>
                {% for test in sample.test_results.all %}
                    {% if 'Physical' in test.parameter.name or 'Color' in test.parameter.name or 'Density' in test.parameter.name or 'Solubility' in test.parameter.name or 'Insoluble' in test.parameter.name %}
                    <tr>
                        <td><span class="checkbox-box">x</span> {{ test.parameter.name }}</td>
                        <td>{{ test.specs|default:"-" }}</td>
                        <td>{{ test.result_value|default:"-" }} {{ test.unit }}</td>
                        <td>{{ test.method.name|default:"-" }}</td>
                        <td>{{ test.measurement_uncertainty|default:"-" }}</td>
                        <td>{{ test.notes|default:"-" }}</td>
                    </tr>
                    {% endif %}
                {% endfor %}

                <!-- CHEMICAL PARAMETER SECTION -->
                <tr>
                    <td colspan="6" class="category-row">CHEMICAL PARAMETER &nbsp;&nbsp;&nbsp; Assay: __________________</td>
                </tr>
                {% for test in sample.test_results.all %}
                    {% if 'Physical' not in test.parameter.name and 'Color' not in test.parameter.name and 'Density' not in test.parameter.name and 'Solubility' not in test.parameter.name and 'Insoluble' not in test.parameter.name %}
                    <tr>
                        <td><span class="checkbox-box">x</span> {{ test.parameter.name }}</td>
                        <td>{{ test.specs|default:"-" }}</td>
                        <td>{{ test.result_value|default:"-" }} {{ test.unit }}</td>
                        <td>{{ test.method.name|default:"-" }}</td>
                        <td>{{ test.measurement_uncertainty|default:"-" }}</td>
                        <td>{{ test.notes|default:"-" }}</td>
                    </tr>
                    {% endif %}
                {% endfor %}
                
                <!-- Fill empty rows to make the form look standard -->
                {% if sample.test_results.count < 10 %}
                    <tr><td style="color:#fff;">-</td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr><td style="color:#fff;">-</td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr><td style="color:#fff;">-</td><td></td><td></td><td></td><td></td><td></td></tr>
                {% endif %}
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
        <table class="signatures">
            <tr>
                <td style="width: 33%; vertical-align: bottom;">
                    ________________________<br/>
                    <strong>Analyst</strong>
                </td>
                <td style="width: 33%; vertical-align: bottom;">
                    ________________________<br/>
                    <strong>Verified By (AQCM)</strong>
                </td>
                <td style="width: 33%; vertical-align: bottom;">
                    ________________________<br/>
                    <strong>Approved By (QCM)</strong>
                </td>
            </tr>
        </table>
        
    </div>
    {% endfor %}
</body>
</html>
"""

with open(coa_path, 'w') as f:
    f.write(html_content)
