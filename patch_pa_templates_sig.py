import re

def patch_template(path, old_sig, new_sig):
    with open(path, 'r') as f:
        content = f.read()
    if old_sig in content:
        content = content.replace(old_sig, new_sig)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Patched {path}")
    else:
        print(f"Could not find old_sig in {path}")

old_101 = """    <table class="signature-table" style="margin-top: 30px;">
        <tr>
            <td style="width: 50%; text-align: center;">
                __________________________________<br/><br/>
                {{ auth.prepared_by.get_full_name|default:"Prepared by (AQCM/QCM)" }}
            </td>
            <td style="width: 50%; text-align: center;">
                __________________________________<br/><br/>
                {{ auth.authorized_by.get_full_name|default:"Authorized by (QCM/CEO)" }}
            </td>
        </tr>
    </table>"""
new_101 = """    <table class="signature-table" style="margin-top: 30px;">
        <tr>
            <td style="width: 50%; text-align: center;">
                {% if auth.prepared_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ auth.prepared_by.get_full_name }}<br/>
                    {{ auth.prepared_at|date:"d-m-Y H:i" }}<br/><br/>
                    <strong>Prepared by (AQCM/QCM)</strong>
                {% else %}
                    __________________________________<br/><br/>
                    {{ auth.prepared_by.get_full_name|default:"Prepared by (AQCM/QCM)" }}
                {% endif %}
            </td>
            <td style="width: 50%; text-align: center;">
                {% if auth.authorized_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ auth.authorized_by.get_full_name }}<br/>
                    {{ auth.authorized_at|date:"d-m-Y H:i" }}<br/><br/>
                    <strong>Authorized by (QCM/CEO)</strong>
                {% else %}
                    __________________________________<br/><br/>
                    {{ auth.authorized_by.get_full_name|default:"Authorized by (QCM/CEO)" }}
                {% endif %}
            </td>
        </tr>
    </table>"""

patch_template('/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/personnel_authorization_permit.html', old_101, new_101)

old_102 = """    <table style="border: none; margin-top: 50px;">
        <tr>
            <td style="border: none; width: 50%; text-align: center;">
                _____________________________________<br/><br/>
                Prepared by (QCM)
            </td>
            <td style="border: none; width: 50%; text-align: center;">
                _____________________________________<br/><br/>
                Authorized by (CEO)
            </td>
        </tr>
    </table>"""
new_102 = """    <table style="border: none; margin-top: 50px;">
        <tr>
            <td style="border: none; width: 50%; text-align: center;">
                {% if authorizations.0.prepared_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ authorizations.0.prepared_by.get_full_name }}<br/>
                    {{ authorizations.0.prepared_at|date:"d-m-Y H:i" }}<br/><br/>
                    <strong>Prepared by (QCM)</strong>
                {% else %}
                    _____________________________________<br/><br/>
                    Prepared by (QCM)
                {% endif %}
            </td>
            <td style="border: none; width: 50%; text-align: center;">
                {% if authorizations.0.authorized_at %}
                    <span style="font-family: 'Courier New', monospace; font-size: 14px;"><i>Digitally Signed</i></span><br/>
                    {{ authorizations.0.authorized_by.get_full_name }}<br/>
                    {{ authorizations.0.authorized_at|date:"d-m-Y H:i" }}<br/><br/>
                    <strong>Authorized by (CEO)</strong>
                {% else %}
                    _____________________________________<br/><br/>
                    Authorized by (CEO)
                {% endif %}
            </td>
        </tr>
    </table>"""

patch_template('/Users/fahimasghar/Documents/QC-Lab-Manager/resources/templates/resources/list_of_authorized_staff.html', old_102, new_102)
