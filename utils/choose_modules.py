import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def choose_modules(always_include: list[str]) -> list[str]:
    custom_modules_path = os.path.join(PROJECT_ROOT, "..", "custom_modules")
    available_modules = [f for f in os.listdir(custom_modules_path) 
                         if os.path.isdir(os.path.join(custom_modules_path, f)) 
                         and f not in always_include]
    available_list = "\n".join(available_modules)
    format_asterisks = f"{'*' *20}"
    print("***Available modules***\n", 
          available_list,
          format_asterisks,
    )
    chosen_modules = input("Enter the modules you want to include (comma-separated): ").split(',')
    chosen_modules = [module.strip() for module in chosen_modules]

    # Always include the required folders
    chosen_modules.extend(always_include)
    chosen_modules = list(set(chosen_modules))  # Remove duplicates
    print(f"chosen modules: {chosen_modules}")
    return chosen_modules



# Upload results of QGIS to SQL database