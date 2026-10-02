import os
import re
import django
import shutil
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lims_core.settings')
django.setup()

from django.core.files import File
from management.models import Document
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

iso_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager/ISO 17025'

id_pattern = re.compile(r'(QCL-[A-Z]+-\d+(?:\.\d+)?)')
rev_pattern = re.compile(r'Rev(?:ision|#|\.\#)?\s*0*(\d+)', re.IGNORECASE)

docs_added = 0

for root, dirs, files in os.walk(iso_dir):
    for filename in files:
        if filename.startswith('~') or filename.startswith('.'):
            continue
            
        if filename.endswith(('.doc', '.docx', '.pdf', '.xlsx', '.xls')):
            filepath = os.path.join(root, filename)
            
            doc_id_match = id_pattern.search(filename)
            if doc_id_match:
                base_doc_id = doc_id_match.group(1)
            else:
                continue 
                
            rev_match = rev_pattern.search(filename)
            version = rev_match.group(1) if rev_match else "1"
            
            # Make document_id genuinely unique to bypass IntegrityError
            unique_doc_id = f"{base_doc_id}-v{version}"
            
            # Skip if we already ingested this exact version
            if Document.objects.filter(document_id=unique_doc_id).exists():
                continue
                
            title = filename
            title = id_pattern.sub('', title)
            title = rev_pattern.sub('', title)
            title = title.replace('.docx', '').replace('.doc', '').replace('.pdf', '').replace('.xlsx', '')
            title = title.replace('()', '').replace('  ', ' ').strip(" -_")
            
            doc_type = 'SOP'
            if 'FRM' in base_doc_id or 'FIL' in base_doc_id:
                doc_type = 'FORM'
            elif 'POL' in base_doc_id:
                doc_type = 'POLICY'
            elif 'LSM' in base_doc_id:
                doc_type = 'MANUAL'
                
            status = 'OBSOLETE' if 'Obselete' in root else 'ACTIVE'
            
            with open(filepath, 'rb') as f:
                doc = Document(
                    document_id=unique_doc_id,
                    title=title if title else base_doc_id,
                    doc_type=doc_type,
                    version=version,
                    status=status,
                    author=admin_user,
                    approved_by=admin_user,
                    issue_date=datetime.now().date(),
                    next_review_date=(datetime.now() + timedelta(days=365)).date()
                )
                doc.file.save(filename, File(f), save=True)
                docs_added += 1
                print(f"Ingested: {unique_doc_id} - {title}")

print(f"\nSuccessfully ingested {docs_added} official ISO documents into the LIMS!")
