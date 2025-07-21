import sys
import os
import subprocess

def update_config(program_path, var_path, fun_path, lib_path, py_lib_path, doc_path, one_to_one):
    lines_to_update = {
        "FILE_PATH_PROGRAM": f"{repr(program_path)}\n",
        "FILE_PATH_VARS": f"{repr(var_path)}\n",
        "FILE_PATH_FUN": f"{repr(fun_path)}\n",
        "FILE_PATH_LIB": f"{repr(lib_path)}\n",
        "FILE_PATH_PY_LIB": f"{repr(py_lib_path)}\n",
        "FILE_DOCUMENTATION_PATH": f"{repr(doc_path)}\n",
        "ONE_TO_ONE_PROGRAM_PATH": f"{repr(one_to_one)}\n"
    }

    config_path = "D:\\ST to Py\\Python\\skripte\\config.py"
    with open(config_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    found_keys = {k: False for k in lines_to_update}

    for line in lines:
        updated = False
        for key in lines_to_update:
            if line.strip().startswith(key):
                updated_lines.append(f"{key} = {lines_to_update[key]}")
                found_keys[key] = True
                updated = True
                break
        if not updated:
            updated_lines.append(line)

    for key, found in found_keys.items():
        if not found:
            updated_lines.append(f"{key} = {lines_to_update[key]}")

    with open(config_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("Config file updated successfully.")

def run_make():
    print("Running make.py...\n")
    result = subprocess.run(["python", "D:\\ST to Py\\Python\\skripte\\make.py"])
    if result.returncode != 0:
        print("Error running make.py!")
    else:
        print("make.py finished successfully!\n")
    print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['1', '2']:	
        print("Usage: python combined_script.py [1|2]")
        print("1: RampController\n2: SignalTools\n")
        sys.exit(1)

    choice = int(sys.argv[1])

    # RampController
    if choice == 1:
        project_dir = "D:\\AS_projects\\RampController"
        program_examples = [f"{project_dir}\\Logical\\Program\\Ramp.st"]
        fun_path = f"{project_dir}\\Logical\\Libraries\\RampLib\\RampLib.fun"
        lib_path = f"{project_dir}\\Logical\\Libraries\\RampLib"
        py_lib_path = "D:\\ST to Py\\py_libs\\RampController\\RampLib.py"
        doc_path = "D:\\ST to Py\\Dokumentacija\\RampController"
        one_to_one = "D:\\ST to Py\\1to1\\Ramp\\Program.py"

        for idx, program_path in enumerate(program_examples, 1):
            base_dir = os.path.dirname(program_path)
            var_path = os.path.join(base_dir, "Variables.var")
            print(f"\n=== Running test case {idx} ===")
            update_config(program_path, var_path, fun_path, lib_path, py_lib_path, doc_path, one_to_one)
            run_make()

    #SignalTools
    elif choice == 2:
        project_dir = "D:\\AS_projects\\MySignalTools"
        program_examples = [f"{project_dir}\\Logical\\Program\\SignalProcess.st"]
        fun_path = f"{project_dir}\\Logical\\Libraries\\SignalLib\\SignalLib.fun"
        lib_path = f"{project_dir}\\Logical\\Libraries\\SignalLib"
        py_lib_path = "D:\\ST to Py\\py_libs\\SignalLib\\SignalLib.py"
        doc_path = "D:\\ST to Py\\Dokumentacija\\SignalLib"
        one_to_one = "D:\\ST to Py\\1to1\\Signal\\Program.py"

        for idx, program_path in enumerate(program_examples, 1):
            base_dir = os.path.dirname(program_path)
            var_path = os.path.join(base_dir, "Variables.var")
            print(f"\n=== Running test case {idx} ===")
            update_config(program_path, var_path, fun_path, lib_path, py_lib_path, doc_path, one_to_one)
            run_make()

    #ArUser
    elif choice == 3:
        project_dir = "D:\\AS_projects\\BR_Vendor"
        program_examples = [f"{project_dir}\\Logical\\UserRole\\UserRole.st"]
        fun_path = f"{project_dir}\\Logical\\Libraries\\ArUser\\ArUser.fun"
        lib_path = f"{project_dir}\\Logical\\Libraries\\ArUser"
        py_lib_path = "D:\\ST to Py\\py_libs\\ArUser\\ArUser.py"
        doc_path = "D:\\ST to Py\\Dokumentacija\\ArUser"

        for idx, program_path in enumerate(program_examples, 1):
            base_dir = os.path.dirname(program_path)
            var_path = os.path.join(base_dir, "Variables.var")
            print(f"\n=== Running test case {idx} ===")
            update_config(program_path, var_path, fun_path, lib_path, py_lib_path, doc_path)
            run_make()
        