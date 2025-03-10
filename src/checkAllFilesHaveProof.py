from xml.etree.ElementTree import parse as parse_xml
from os import listdir
from sys import exit

def extract_mlw_filenames_from_session():
    root = parse_xml('src/why3session.xml').getroot()
    mlw_filenames = set()

    for elem in root.iter():
        if elem.tag == 'path': # 'path' is used by why3 for filenames
            if elem.attrib['name'].endswith('.mlw'):
                mlw_filenames.add(elem.attrib['name'])

    return mlw_filenames

def extract_mlw_filenames_from_directory():
    mlw_filenames = set()

    for file_name in listdir('src/'):
        if file_name.endswith('.mlw'):
            mlw_filenames.add(file_name)

    return mlw_filenames

def check_whyml_files_proven():
    session_filenames = extract_mlw_filenames_from_session()
    directory_filenames = extract_mlw_filenames_from_directory()
    # twoHonestParties.mlw is run for the simple payment test, it thus does not need a proof. We therefore ignore it.
    relevant_directory_filenames = directory_filenames - {'twoHonestParties.mlw'}

    if session_filenames == relevant_directory_filenames:
        print("Proof availability check PASSED:")
        print("Apart from twoHonestParties.mlw, all *.mlw files in the directory have a proof in the proof tree and vice versa.")
    else:
        print("Proof availability check FAILED:")
        extra_in_session = session_filenames - relevant_directory_filenames
        if extra_in_session:
            print("*.mlw files in proof tree but not in directory:")
            for file in extra_in_session:
                print(file)
        extra_in_directory = relevant_directory_filenames - session_filenames
        if extra_in_directory:
            print("*.mlw files in directory but not in proof tree:")
            for file in extra_in_directory:
                print(file)
        exit(1)

if __name__ == "__main__":
    check_whyml_files_proven()
