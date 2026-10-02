import re

# 1. Analysis Request
p1 = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/analysis_request.html'
with open(p1, 'r') as f: c1 = f.read()

c1 = c1.replace('<td><strong>Serial #:</strong> ________________</td>', '<td><strong>Serial #:</strong> {{ sample.serial_number|default:"________________" }}</td>')
c1 = c1.replace('Total Weight = {{ sample.sample_quantity|default:"______" }}', 'Total Weight = {{ sample.sample_quantity|default:"______" }}')
c1 = c1.replace('{{ sample.rejection_reason|default:"□ Improper sample received   □ Out of scope   □ Other ____________________" }}', '{{ sample.rejection_reason|default:"□ Improper sample received   &nbsp;&nbsp;&nbsp; □ Out of scope   &nbsp;&nbsp;&nbsp; □ Other ____________________" }}')

c1 = c1.replace('_________________________<br><strong>Customer Signature</strong>', '{{ sample.customer_signature|default:"_________________________" }}<br><strong>Customer Signature</strong>')
c1 = c1.replace('_________________________<br><strong>Sample Receiver</strong>', '{{ sample.received_by.get_full_name|default:"_________________________" }}<br><strong>Sample Receiver</strong>')
c1 = c1.replace('_________________________<br><strong>Lab Incharge</strong>', '{{ sample.approved_by.get_full_name|default:"_________________________" }}<br><strong>Lab Incharge</strong>')

with open(p1, 'w') as f: f.write(c1)

# 2. Certificate of Analysis
p2 = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
with open(p2, 'r') as f: c2 = f.read()

c2 = c2.replace('CHEMICAL PARAMETER &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Assay: __________________', 'CHEMICAL PARAMETER &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Assay: {{ sample.assay|default:"__________________" }}')
# Replace bottom signatures in CoA which are currently three lines of ________________________<br/>
# Let's find those exact lines.
bottom = """                <td style="text-align: center; border: none;">
                    ________________________<br/>
                    <strong>Analyst</strong>
                </td>
                <td style="text-align: center; border: none;">
                    ________________________<br/>
                    <strong>AQCM</strong>
                </td>
                <td style="text-align: center; border: none;">
                    ________________________<br/>
                    <strong>QCM / Plant Manager</strong>
                </td>"""
new_bottom = """                <td style="text-align: center; border: none;">
                    <!-- Take the first test result's analyst -->
                    {{ sample.test_results.first.analyst.get_full_name|default:"________________________" }}<br/>
                    <strong>Analyst</strong>
                </td>
                <td style="text-align: center; border: none;">
                    {{ sample.verified_by.get_full_name|default:"________________________" }}<br/>
                    <strong>AQCM</strong>
                </td>
                <td style="text-align: center; border: none;">
                    {{ sample.approved_by.get_full_name|default:"________________________" }}<br/>
                    <strong>QCM / Plant Manager</strong>
                </td>"""
c2 = c2.replace(bottom, new_bottom)

with open(p2, 'w') as f: f.write(c2)

print("Patched Sample templates.")
