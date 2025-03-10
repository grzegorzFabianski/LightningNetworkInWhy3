import xml.etree.ElementTree as ET
import sys

def clean_proof_tree(tree):
    root = tree.getroot()

    # Iterate over all "goal" elements
    for goal in root.findall(".//goal"):
        transf_child = None
        proof_child = None

        for child in goal:
            if child.tag == "transf":
                transf_child = child
                break  # Stop when the first "transf" is found
            elif child.tag == "proof" and proof_child is not None:
                proof_child = child

        child_to_keep = transf_child if transf_child is not None else proof_child

        # Remove all other children of the "goal" element that are "proof" or "transf"
        if child_to_keep is not None:
            for child in list(goal):
                if child != child_to_keep and child.tag in {"proof", "transf"}:
                    goal.remove(child)

    return root

def add_doctype(root):
    res = ET.tostring(root, xml_declaration=True, encoding='utf-8').split(b"\n")
    res.insert(1, b"<!DOCTYPE why3session PUBLIC \"-//Why3//proof session v5//EN\"\n\"https://www.why3.org/why3session.dtd\">")
    return b"\n".join(res)

clean = clean_proof_tree(ET.parse("src/why3session.xml"))

complete = add_doctype(clean)

with open("src/why3session.xml", 'wb') as f:
    f.write(complete)
