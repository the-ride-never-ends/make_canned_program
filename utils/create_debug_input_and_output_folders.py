import os

def create_debug_input_and_output_folders() -> None:
    folders = [
        ('debug_logs','_debug_logs_go_here'), 
        ('input', '_input_goes_here'), 
        ('output', "_output_goes_here")
    ]

    for folder in folders:
        os.makedirs(folder[0], exist_ok=True)
        with open(os.path.join(folder[0], f'{folder[1]}.txt'), 'w') as file:
            file.write(f'This is a text file in the {folder} folder.')
