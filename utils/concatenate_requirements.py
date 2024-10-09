import os
import glob

def concatenate_requirements(program_path: str) -> set:
    """
    Concatenate requirements.txt files
    """
    requirements_files = glob.glob(os.path.join(program_path, "**", "requirements.txt"), recursive=True)
    all_requirements = set()
    for req_file in requirements_files:
        print(f"Found requirements.txt for {req_file}")
        with open(req_file, 'r') as f:
            all_requirements.update(f.read().splitlines())

    with open(os.path.join(program_path, "requirements.txt"), 'w') as f:
        for req in sorted(all_requirements):
            f.write(f"{req}\n")
    print("Made requirements.txt for main program")
    return all_requirements
