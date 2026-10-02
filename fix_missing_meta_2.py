import re

def append_to_meta(filepath, model_name, extra_lines):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # find class Meta inside model_name
    pattern = rf"(class {model_name}\(models\.Model\):.*?class Meta:.*?)(?=\n\w|\Z)"
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        old_block = match.group(1)
        new_block = old_block + extra_lines
        content = content.replace(old_block, new_block)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Added to {model_name}")

append_to_meta('/Users/fahimasghar/Documents/QC-Lab-Manager/resources/models.py', 'ReagentStandard', "\n        verbose_name = 'CRM / Reagent List (QCL-FRM-5.01)'\n        verbose_name_plural = 'CRM / Reagent Lists (QCL-FRM-5.01)'\n")

def insert_meta_no_meta(filepath, model_name, verbose_name):
    with open(filepath, 'r') as f:
        content = f.read()
    pattern = rf"(class {model_name}\(models\.Model\):.*?)(?=\nclass |\Z)"
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        class_body = match.group(1)
        if "class Meta:" not in class_body:
            meta_block = f"\n    class Meta:\n        verbose_name = '{verbose_name}'\n        verbose_name_plural = '{verbose_name}s'\n"
            new_class_body = class_body + meta_block
            new_content = content.replace(class_body, new_class_body)
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Added Meta to {model_name}")

insert_meta_no_meta('/Users/fahimasghar/Documents/QC-Lab-Manager/samples/models.py', 'SampleReturn', 'Sample Return Form (QCL-FRM-22.01)')

