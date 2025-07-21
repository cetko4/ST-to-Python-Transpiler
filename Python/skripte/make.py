import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    result = subprocess.run(["python", script_name])
    if result.returncode != 0:
        print(f"Error running {script_name}")
    else:
        print(f"\n{script_name} finished successfully\n")

if __name__ == "__main__":
    scripts = ["D:\\ST to Py\\Python\\skripte\\compare_functions.py", "D:\\ST to Py\\Python\\skripte\\api_req.py"]
    
    for script in scripts:
        run_script(script)