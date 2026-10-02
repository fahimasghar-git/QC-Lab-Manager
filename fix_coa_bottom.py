import re

p2 = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/templates/samples/certificate_of_analysis.html'
with open(p2, 'r') as f: c2 = f.read()

# Look for Analyst, AQCM, QCM
c2 = re.sub(r'_{5,}<br/>\s*<strong>Analyst</strong>', '{{ sample.test_results.first.analyst.get_full_name|default:"________________________" }}<br/>\n                    <strong>Analyst</strong>', c2)
c2 = re.sub(r'_{5,}<br/>\s*<strong>AQCM</strong>', '{{ sample.verified_by.get_full_name|default:"________________________" }}<br/>\n                    <strong>AQCM</strong>', c2)
c2 = re.sub(r'_{5,}<br/>\s*<strong>QCM / Plant Manager</strong>', '{{ sample.approved_by.get_full_name|default:"________________________" }}<br/>\n                    <strong>QCM / Plant Manager</strong>', c2)

with open(p2, 'w') as f: f.write(c2)
