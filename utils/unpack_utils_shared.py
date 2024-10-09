import os
import shutil

def unpack_utils_shared(chosen_modules, program_path):
    for module in chosen_modules:
        utils_shared_src = os.path.join(program_path, module, "utils", "shared")
        utils_shared_dst = os.path.join(program_path, "utils", "shared")

        if os.path.exists(utils_shared_src):
            if not os.path.exists(utils_shared_dst):
                shutil.copytree(utils_shared_src, utils_shared_dst, ignore=shutil.ignore_patterns('.git', '.gitignore'))
                print(f"Unpacked utils.shared for {module}")

            else:  # Don't overwrite files if they're already there.
                for file in os.listdir(utils_shared_src):
                    src_file = os.path.join(utils_shared_src, file)
                    dst_file = os.path.join(utils_shared_dst, file)

                    if not os.path.exists(dst_file):
                        if os.path.isdir(src_file):
                            shutil.copytree(src_file, dst_file, ignore=shutil.ignore_patterns('.git', '.gitignore'))
                        else:
                            shutil.copy2(src_file, dst_file)
                        print(f"Copied {file} from {module}'s utils.shared to main utils.shared")
                    else:
                        print(f"Skipped {file} from {module}'s utils.shared (already exists in main utils.shared)")

    # Remove the individual module's utils.shared folders
    for module in chosen_modules:
        utils_shared_src = os.path.join(program_path, module, "utils", "shared")
        if os.path.exists(utils_shared_src):
            shutil.rmtree(utils_shared_src)
            print(f"Removed {module}'s utils.shared folder")