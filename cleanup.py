#!/usr/bin/env python3
"""Clean up nested ai_club folder and deploy."""
import os
import shutil
import subprocess
from pathlib import Path

def run(cmd):
    """Run shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd="c:\\HTML\\club app")
    return result.returncode == 0

def main():
    nested_folder = Path(r"c:\HTML\club app\ai_club\ai_club")
    
    # Remove the nested folder
    if nested_folder.exists():
        print(f"Deleting {nested_folder}...")
        shutil.rmtree(nested_folder, ignore_errors=True)
        if not nested_folder.exists():
            print("✓ Nested folder deleted")
        else:
            print("✗ Failed to delete folder")
            return False
    
    # Git operations
    os.chdir(r"c:\HTML\club app")
    run("git add -A")
    run('git commit -m "chore: remove nested duplicate ai_club package folder"')
    run("git push origin main")
    
    # Collectstatic
    run("python manage.py collectstatic --noinput --clear")
    
    print("\n✓ All done! Nested folder removed, changes pushed, static files collected.")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
