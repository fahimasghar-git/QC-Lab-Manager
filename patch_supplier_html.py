html_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/supplier_evaluation.html'
with open(html_path, 'r') as f:
    content = f.read()

content = content.replace('___________________</td>\n                <td style="width: 15%;"><strong>Date</strong></td>', '{{ s.evaluated_by.get_full_name|default:"___________________" }}</td>\n                <td style="width: 15%;"><strong>Date</strong></td>')
content = content.replace('<td>___________________</td>\n                <td><strong>Date</strong></td>', '<td>{{ s.approved_by.get_full_name|default:"___________________" }}</td>\n                <td><strong>Date</strong></td>')

with open(html_path, 'w') as f:
    f.write(content)
print("Updated Supplier template HTML")
