import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from collections import defaultdict

# Function to recursively find all 'proof' elements
def find_proof_elements(root):
    return root.findall(".//proof")  # .//proof finds all 'proof' elements no matter how deeply nested

# Function to parse XML and extract prover and steps
def parse_prover_steps(xml_content):
    root = ET.fromstring(xml_content)  # Parse XML from string

    prover_steps = defaultdict(list)

    # Find all 'proof' elements no matter where they are nested
    proofs = find_proof_elements(root)

    for proof in proofs:
        prover = proof.get('prover')
        result = proof.find('result')
        if result is not None:
            steps = int(result.get('steps', 0))
            prover_steps[prover].append(steps)
    
    return prover_steps

# Function to plot histograms
def plot_histograms(prover_steps):
    for prover, steps in prover_steps.items():
        plt.figure()
        plt.hist(steps, bins=50, alpha=0.7, color='blue')
        plt.yscale('log')
        plt.title(f'Histogram of Steps for Prover {prover}')
        plt.xlabel('Steps')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

# Main function to load file and generate histograms
def main():
    file_path = 'bitcoin/why3session.xml'  # File path to read the XML content
    with open(file_path, 'r') as file:
        xml_content = file.read()

    prover_steps = parse_prover_steps(xml_content)
    plot_histograms(prover_steps)

if __name__ == "__main__":
    main()
