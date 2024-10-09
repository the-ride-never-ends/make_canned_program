import os

def choose_modules(always_include: list[str]) -> list[str]:
    custom_modules_path = "../custom_modules"
    available_modules = [f for f in os.listdir(custom_modules_path) 
                         if os.path.isdir(os.path.join(custom_modules_path, f)) 
                         and f not in always_include]
    print("***Available modules***\n", "\n".join(available_modules), "\n**********")
    chosen_modules = input("Enter the modules you want to include (comma-separated): ").split(',')
    chosen_modules = [module.strip() for module in chosen_modules]

    # Always include the required folders
    chosen_modules.extend(always_include)
    chosen_modules = list(set(chosen_modules))  # Remove duplicates
    print(f"chosen modules: {chosen_modules}")
    return chosen_modules
