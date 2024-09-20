import os
import re
import shutil
import subprocess
import webbrowser
import time
from rich.console import Console

console = Console()

def open_vite_server():
    url = "http://localhost:5173"
    console.print(f"Starting app in browser", style="bold green")
    webbrowser.open(url)

def process_markdown_file(file_path, app_folder):
    apps_parent_folder = app_folder

    # Ensure we're using absolute paths
    current_dir = os.getcwd()
    apps_parent_folder = os.path.abspath(os.path.join(current_dir, apps_parent_folder))

    with open(file_path, "r") as file:
        content = file.read()

    # Extract the install script and app folder name
    install_script_match = re.search(
        r"^#+\s+Install script\n\n```bash\n([\s\S]+?)\n```", content, re.MULTILINE | re.IGNORECASE
    )
    if not install_script_match:
        raise ValueError("Install script not found in the markdown file")

    install_script = install_script_match.group(1).strip()

    # Extract app folder name from mkdir and cd commands
    app_folder_match = re.search(
        r"mkdir\s+(\S+).*?\s+cd\s+(\S+)", install_script, re.DOTALL
    )
    if not app_folder_match:
        raise ValueError("Could not determine app folder name from install script")

    app_folder = app_folder_match.group(1)

    full_app_folder = os.path.join(apps_parent_folder, app_folder)
    
    # Remove the app folder if it already exists including all its contents
    if os.path.exists(full_app_folder):
        shutil.rmtree(full_app_folder)

    # Create the apps parent folder if it doesn't exist
    os.makedirs(apps_parent_folder, exist_ok=True)

    # Write and execute install script
    install_script_path = os.path.join(
        apps_parent_folder, f"{app_folder}_install_script.sh"
    )

    # check if the install script already exists
    if os.path.exists(install_script_path):
        os.remove(install_script_path)
        
    with open(install_script_path, "w") as file:
        file.write(install_script)

    os.chmod(install_script_path, 0o755)

    console.print("Installing app...", style="green")
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.run(
                ["/bin/bash", install_script_path],
                check=True,
                cwd=apps_parent_folder,
                stdout=devnull,
                stderr=devnull
            )
    except subprocess.CalledProcessError as e:
        print(f"Error running install script: {e}")
        print(f"Script exit code: {e.returncode}")
        print(f"Script output: {e.output}")
        raise

    # Process other code blocks
    pattern = re.compile(
        r"^#+\s+(?:File:\s+)?(.+?)\n\n```(\w+)?\n([\s\S]+?)\n```", re.MULTILINE
    )

    for match in pattern.finditer(content):
        heading, language, code = match.groups()

        if heading.lower() == "install script":
            continue  # Skip, as we've already processed this

        if heading.lower() == "run script":
            filename = "run_script.sh"
        else:
            filename = heading.strip()

        # Determine the file extension
        if language:
            extension = f".{language}"
        elif filename.endswith((".sh", ".css", ".js", ".jsx")):
            extension = ""
        else:
            extension = ".txt"

        # Construct the full file path
        full_path = os.path.join(full_app_folder, filename)

        # Create any necessary directories
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write the code to the file
        with open(full_path, "w") as file:
            file.write(code.strip())

        # Make shell scripts executable
        if filename.endswith(".sh"):
            os.chmod(full_path, 0o755)

    console.print(f"Installed app successfully...", style="green")
    # Run run script if it exists
    run_script_path = os.path.join(full_app_folder, "run_script.sh")
    if os.path.exists(run_script_path):
        console.print("Running the app...", style="green")
        try:
            # Start the run script in a separate process, redirecting output to /dev/null
            with open(os.devnull, 'w') as devnull:
                process = subprocess.Popen(
                    ["/bin/bash", run_script_path], 
                    cwd=full_app_folder, 
                    stdout=devnull, 
                    stderr=devnull
                )            
            # Wait for a short time to allow the server to start
            time.sleep(5)
            
            # Open the Vite server URL
            open_vite_server()
            
            # Wait for the process to complete
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                console.print(f"Run script exited with non-zero status: {process.returncode}", style="red")
                console.print(f"stdout: {stdout.decode()}", style="red")
                console.print(f"stderr: {stderr.decode()}", style="red")
                raise subprocess.CalledProcessError(process.returncode, run_script_path)

        except subprocess.CalledProcessError as e:
            console.print(f"Error running run script: {e}", style="red")
            console.print(f"Script exit code: {e.returncode}", style="red")
            console.print(f"Script output: {e.output}", style="red")
            raise
        finally:
            # Run cleanup script after the app exits
            cleanup_script_path = os.path.join(apps_parent_folder, "cleanup_script.sh")
            if os.path.exists(cleanup_script_path):
                console.print("Running cleanup script...", style="green")
                try:
                    subprocess.run(["/bin/bash", cleanup_script_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError as e:
                    print(f"Error running cleanup script: {e}")

    console.print(f"All operations completed for the app.", style="green")