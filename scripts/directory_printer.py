import os

def print_directory_structure(root_dir, indent=""):
    try:
        entries = sorted(os.listdir(root_dir))
    except PermissionError:
        print(indent + "⛔ [Permission Denied]")
        return
    except FileNotFoundError:
        print(indent + "❌ [Not Found]")
        return

    for entry in entries:
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path):
            print(f"{indent}📁 {entry}/")
            print_directory_structure(full_path, indent + "    ")
        else:
            print(f"{indent}📄 {entry}")

if __name__ == "__main__":
    project_root = r"D:\PhD\prog_report_2025_June_project"  # <-- Adjust this if needed
    print(f"📂 Directory Structure of: {project_root}\n")
    print_directory_structure(project_root)
