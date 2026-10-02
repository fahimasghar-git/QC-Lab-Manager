import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/templates/management/non_conformance_log.html'
with open(path, 'r') as f:
    content = f.read()

footer_table = """
    <table class="noborder" style="margin-top: 50px; border: none;">
        <tr>
            <td style="width: 50%; text-align: left; border: none;">
                <strong>Prepared By:</strong> ______________________
            </td>
            <td style="width: 50%; text-align: right; border: none;">
                <strong>Updated On:</strong> ______________________
            </td>
        </tr>
    </table>
"""
if "Prepared By:" not in content:
    content = content.replace("</table>\n\n</body>", "</table>\n" + footer_table + "\n</body>")
    with open(path, 'w') as f:
        f.write(content)
    print("Added signature footer to NC Log.")
