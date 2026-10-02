import re
import os

def insert_meta(filepath, model_name, verbose_name):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # If Meta already exists, this might be tricky, but ReagentStandard has one.
    if model_name == "ReagentStandard":
        new_content = content.replace("class Meta:\n        managed = True", f"class Meta:\n        managed = True\n        verbose_name = '{verbose_name}'\n        verbose_name_plural = '{verbose_name}s'")
    else:
        # Find the last field of the model before the next class or end of file
        # It's easier to append to the end of the class.
        # Find the start of the NEXT class, or the end of the string
        pattern = rf"(class {model_name}\(models\.Model\):.*?)(?=\nclass |\Z)"
        match = re.search(pattern, content, flags=re.DOTALL)
        if match:
            class_body = match.group(1)
            # check if it already has class Meta
            if "class Meta:" not in class_body:
                meta_block = f"\n    class Meta:\n        verbose_name = '{verbose_name}'\n        verbose_name_plural = '{verbose_name}s'\n"
                new_class_body = class_body + meta_block
                new_content = content.replace(class_body, new_class_body)
            else:
                new_content = content
        else:
            new_content = content

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Added Meta to {model_name}")

# Management
mg_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/management/models.py'
insert_meta(mg_path, 'ManagementReview', 'Management Review (QCL-FRM-9.01)')
insert_meta(mg_path, 'LabCleaningInspection', 'Lab Cleaning Inspection (QCL-FRM-17.14)')
insert_meta(mg_path, 'MasterListRecord', 'Master List of Records (QCL-FRM-20.01)')
insert_meta(mg_path, 'MasterListFileFolder', 'Master List of Files (QCL-FRM-20.02)')
insert_meta(mg_path, 'CustomerFeedback', 'Customer Feedback (QCL-FRM-21.01)')

# Resources
res_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py'
insert_meta(res_path, 'ReagentStandard', 'CRM / Reagent List (QCL-FRM-5.01)')
insert_meta(res_path, 'ComparativeStatement', 'Comparative Statement (QCL-FRM-6.05)')
insert_meta(res_path, 'SupplierEvaluationPlan', 'Supplier Evaluation Plan (QCL-FRM-6.06)')

# Samples
sam_path = '/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py'
insert_meta(sam_path, 'SampleReturn', 'Sample Return Form (QCL-FRM-22.01)')

