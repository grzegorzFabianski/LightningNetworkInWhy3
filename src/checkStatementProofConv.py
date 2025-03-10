import os
import re
from sys import exit

def remove_comments(content):
    """
    Removes all block comments (from (* to *)) from the content.
    """
    comment_pattern = re.compile(r'\(\*.*?\*\)', re.DOTALL)
    return re.sub(comment_pattern, '', content)

def check_lemma_axiom_in_lemmas(file_path):
    """
    Check that all 'val lemma' and 'axiom' declarations only appear in modules ending with 'Lemmas'.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Remove comments from the content
    content = remove_comments(content)

    # Find all module declarations
    module_pattern = re.compile(r'module\s+(\w+)\s*')
    modules = module_pattern.findall(content)

    # Find all 'val lemma' and 'axiom' declarations
    lemma_pattern = re.compile(r'\b(val lemma|axiom)\b')
    declarations = lemma_pattern.findall(content)

    # Current module tracking
    current_module = None
    errors = []

    for line in content.splitlines():
        module_match = re.match(module_pattern, line)
        if module_match:
            current_module = module_match.group(1)

        if 'val lemma' in line or 'axiom' in line:
            if current_module and not current_module.endswith('Lemmas') and not current_module.endswith('Spec'):
                errors.append(f"Error in {file_path}: 'val lemma' or 'axiom' found in non-Lemmas module '{current_module}")

    return errors

def check_proofs_for_lemmas(file_path):
    """
    Check that each XLemmas module has a corresponding XProofs module declared as 'module XProofs : XLemmas'.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Find all Lemmas modules
    lemmas_pattern = re.compile(r'module\s+(\w+Lemmas)\b')
    lemmas_modules = lemmas_pattern.findall(content)

    # Find all Proofs modules that reference Lemmas modules
    proofs_pattern = re.compile(r'module\s+(\w+Proofs)\s*:\s*(\w+Lemmas)')
    proofs_modules = proofs_pattern.findall(content)

    # Create a dictionary to map Lemmas to their Proofs modules
    proofs_dict = {proof: lemma for proof, lemma in proofs_modules}

    errors = []

    # Check that every Lemmas module has a corresponding Proofs module
    for lemmas in lemmas_modules:
        corresponding_proofs = lemmas.replace('Lemmas', 'Proofs')
        if corresponding_proofs not in proofs_dict or proofs_dict[corresponding_proofs] != lemmas:
            errors.append(f"Error in {file_path}: No corresponding Proofs module for Lemmas module '{lemmas}'")

    return errors

def check_whyml_files():
    """
    Go through all WhyML files in the current directory and check the conditions.
    """
    errors = []
    for file_name in os.listdir('.'):
        if file_name.endswith('.mlw'):
            errors.extend(check_lemma_axiom_in_lemmas(file_name))
            errors.extend(check_proofs_for_lemmas(file_name))

    if errors:
        print("Statement-proof-separation check FAILED:")
        print("Errors found:")
        for error in errors:
            print(error)
        exit(1)
    else:
        print("Statement-proof-separation check PASSED:")
        print("All declared lemmas have proofs in their corresponding -Proof modules.")

if __name__ == "__main__":
    check_whyml_files()
