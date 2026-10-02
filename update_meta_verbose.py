import os
import re

def update_model_meta(file_path, model_name, form_no):
    with open(file_path, 'r') as f:
        content = f.read()

    # Find the class definition
    pattern = rf"(class {model_name}\(models\.Model\):.*?)(?=class \w+\(models\.Model\):|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        model_block = match.group(1)
        
        # Check if class Meta already exists
        if "class Meta:" in model_block:
            meta_pattern = r"(class Meta:.*?)(def |\Z)"
            meta_match = re.search(meta_pattern, model_block, re.DOTALL)
            if meta_match:
                meta_block = meta_match.group(1)
                new_meta_block = meta_block + f"        verbose_name = '{model_name} ({form_no})'\n        verbose_name_plural = '{model_name}s ({form_no})'\n"
                new_model_block = model_block.replace(meta_block, new_meta_block)
                content = content.replace(model_block, new_model_block)
        else:
            # Inject class Meta before def __str__ or at the end
            meta_code = f"\n    class Meta:\n        verbose_name = '{model_name} ({form_no})'\n        verbose_name_plural = '{model_name}s ({form_no})'\n\n"
            if "def __str__" in model_block:
                new_model_block = model_block.replace("    def __str__", meta_code + "    def __str__")
            else:
                new_model_block = model_block + meta_code
            content = content.replace(model_block, new_model_block)
            
        with open(file_path, 'w') as f:
            f.write(content)

# Define mappings based on ingested ISO docs
mappings = [
    # samples/models.py
    ('samples/models.py', 'Sample', 'QCL-FRM-12.01'),
    
    # management/models.py
    ('management/models.py', 'NonConformance', 'QCL-FRM-14.01'),
    ('management/models.py', 'Risk', 'QCL-FRM-8.01'),
    ('management/models.py', 'InternalAudit', 'QCL-FRM-10.10'),
    ('management/models.py', 'AuditFinding', 'QCL-FRM-10.09'),
    ('management/models.py', 'Document', 'QCL-FRM-7.01'), # Master list
    
    # resources/models.py
    ('resources/models.py', 'Supplier', 'QCL-FRM-6.03'),
    ('resources/models.py', 'PurchaseRequest', 'QCL-FRM-6.07'),
    ('resources/models.py', 'Equipment', 'QCL-FRM-4.02'),
    ('resources/models.py', 'CalibrationRecord', 'QCL-FRM-4.04'),
    ('resources/models.py', 'CompetencyRecord', 'QCL-FRM-1.04'),
]

base_dir = '/Users/fahimasghar/Documents/QC-Lab-Manager/'
for rel_path, model, form in mappings:
    update_model_meta(os.path.join(base_dir, rel_path), model, form)
    print(f"Mapped {model} to {form}")

