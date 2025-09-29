import os

def create_debug_input_and_output_folders(program_path: str) -> None:
    """Create debug_logs, input, and output folders with placeholder files.
    
    Creates three folders (debug_logs, input, output) in the specified program
    directory and places a placeholder text file in each one to ensure the 
    folders are preserved in version control.
    
    Args:
        program_path (str): The base directory where the folders will be created.
    """
    folders = [
        ('debug_logs','_debug_logs_go_here'), 
        ('input', '_input_goes_here'), 
        ('output', "_output_goes_here")
    ]

    for folder in folders:
        folder_path = os.path.join(program_path, folder[0])
        os.makedirs(folder_path, exist_ok=True)
        with open(os.path.join(folder_path, f'{folder[1]}.txt'), 'w') as file:
            file.write(f'This is a text file in the {folder[0]} folder.')
