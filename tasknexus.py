import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import threading
import json
import psutil
from pathlib import Path
import base64

# =============================
# Constants and Branding
# =============================
APP_NAME = base64.b64decode("UjAwdFJldmVyc2FsU1NIJ3MgUGVuIFRlc3RpbmcgVG9vbGtpdA==").decode("utf-8")
APP_VERSION = "1.0.0"  # Update this with the current version when making updates
LICENSE = "MIT License"  # Change license type if necessary

# =============================
# Splash Screen
# =============================
def splash_screen():
    splash = tk.Tk()
    splash.title(APP_NAME)
    splash.geometry("800x250")  # Adjust dimensions if you want a larger or smaller splash screen
    splash.configure(bg="#1c1c1c")

    tk.Label(splash, text=APP_NAME, font=("Consolas", 18, "bold"), bg="#1c1c1c", fg="#e74c3c").pack(pady=20)
    tk.Label(splash, text=f"Version {APP_VERSION}", font=("Consolas", 12), bg="#1c1c1c", fg="#ffffff").pack(pady=10)
    tk.Label(
        splash,
        text="!Shout-Out To HackForums.net!",
        font=("Consolas", 10),
        bg="#1c1c1c",
        fg="#ff9900",
    ).pack(pady=10)

    splash.after(3000, splash.destroy)  # Adjust the time (in milliseconds) the splash screen is visible
    splash.mainloop()

# =============================
# Modular Plugin System
# =============================
def load_plugins():
    plugins_dir = Path("plugins")  # Change directory path if plugins are stored elsewhere
    plugins_dir.mkdir(exist_ok=True)
    plugins = []
    for plugin_file in plugins_dir.glob("*.json"):
        try:
            with open(plugin_file, "r") as f:
                plugin = json.load(f)
                plugins.append(plugin)
        except json.JSONDecodeError:
            continue
    return plugins

# =============================
# AI Recommendations
# =============================
def recommend_tools(context):
    if "scan" in context.lower():
        return "Recommended: Nmap for deep scans, or use masscan for faster results."
    elif "subdomain" in context.lower():
        return "Recommended: Amass or Sublist3r for comprehensive subdomain enumeration."
    elif "traffic" in context.lower():
        return "Recommended: Wireshark or tcpdump for live packet analysis."
    return "Explore available tools for your specific task."

# =============================
# Enhanced Tool Runner
# =============================
def run_tool(tool_command, context=""):
    def execute():
        try:
            # Validate the tool command before execution
            if not isinstance(tool_command, str) or "rm" in tool_command.lower():
                raise ValueError("Invalid or potentially dangerous command.")

            result_text.insert(tk.END, f"\n[INFO] Running: {tool_command}\n")
            if context:
                recommendation = recommend_tools(context)
                result_text.insert(tk.END, f"[AI Suggestion] {recommendation}\n")
            result_text.insert(tk.END, f"[INFO] CPU Usage: {psutil.cpu_percent()}% | Memory Usage: {psutil.virtual_memory().percent}%\n")
            output = subprocess.check_output(tool_command, shell=True, text=True)
            result_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            result_text.insert(tk.END, f"\n[ERROR] {e}\n")
        except ValueError as ve:
            result_text.insert(tk.END, f"\n[ERROR] {ve}\n")
        finally:
            result_text.insert(tk.END, "\n" + "-" * 50 + "\n")
            result_text.see(tk.END)
    threading.Thread(target=execute).start()

# =============================
# Export Configurations
# =============================
def export_config():
    file_path = asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open("tool_config.json", "r") as f:
                config = json.load(f)
            with open(file_path, "w") as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Export Successful", f"Configurations exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export configurations: {e}")

def import_config():
    file_path = askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
            with open("tool_config.json", "w") as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Import Successful", "Configurations imported successfully!")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import configurations: {e}")

# =============================
# Load Tools with Plugins
# =============================
def load_tools():
    try:
        with open("tool_config.json", "r") as f:
            tools = json.load(f)
    except FileNotFoundError:
        tools = {
            "Nmap Scan": "nmap -sS 127.0.0.1",  # Modify the command based on the tool setup
            "Directory Brute-force": "gobuster dir -u http://127.0.0.1 -w /usr/share/wordlists/dirb/common.txt",  # Update wordlist path
            "Subdomain Enumeration": "amass enum -d example.com",  # Replace 'example.com' with target domain
            "Wi-Fi Scan": "airodump-ng wlan0",  # Ensure 'wlan0' matches your Wi-Fi adapter name
            "Port Scan": "netcat -zv 127.0.0.1 1-65535",  # Adjust IP address or port range as needed
            "Live Traffic Analysis": "tcpdump -i wlan0"  # Replace 'wlan0' with the correct interface
        }
        with open("tool_config.json", "w") as f:
            json.dump(tools, f, indent=4)
    plugins = load_plugins()
    for plugin in plugins:
        tools.update(plugin.get("tools", {}))
    return tools

# =============================
# Save Output as HTML Report
# =============================
def export_report():
    file_path = asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
    if file_path:
        try:
            html_content = f"""<html>
<head><title>{APP_NAME} Report</title></head>
<body style='background-color: #1c1c1c; color: #e74c3c;'>
<h1 style='text-align: center;'>Command Output</h1>
<pre style='font-family: monospace; color: #ffffff;'>{result_text.get('1.0', tk.END)}</pre>
</body>
</html>"""
            with open(file_path, "w") as f:
                f.write(html_content)
            messagebox.showinfo("Report Exported", f"Report saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Report Export Error", f"Failed to export report: {e}")

# =============================
# Additional Functionalities
# =============================
def open_documentation():
    messagebox.showinfo("Documentation", "Refer to the user manual for detailed guidance.")

def reset_defaults():
    try:
        os.remove("tool_config.json")
        load_tools()  # Recreate default config
        messagebox.showinfo("Defaults Reset", "All configurations reset to defaults.")
    except FileNotFoundError:
        messagebox.showinfo("Defaults Reset", "No configurations found to reset.")
    except Exception as e:
        messagebox.showerror("Reset Error", f"Failed to reset configurations: {e}")

def view_system_info():
    try:
        system_info = f"CPU Usage: {psutil.cpu_percent()}%\nMemory Usage: {psutil.virtual_memory().percent}%\nDisk Usage: {psutil.disk_usage('/').percent}%"
        messagebox.showinfo("System Info", system_info)
    except Exception as e:
        messagebox.showerror("System Info Error", f"Failed to retrieve system information: {e}")

# =============================
# Create Modern GUI
# =============================
def create_gui():
    global root, result_text

    root = tk.Tk()
    root.title(f"{APP_NAME} - Version {APP_VERSION}")
    root.geometry("1200x800")  # Adjust window size if necessary
    root.configure(bg="#1c1c1c")

    ttk.Style().configure("TFrame", background="#1c1c1c")
    ttk.Style().configure("TLabel", background="#1c1c1c", foreground="#e74c3c")
    ttk.Style().configure("TButton", padding=10, relief="flat", background="#2c2c2c", foreground="#ffffff", font=("Helvetica", 10, "bold"))
    ttk.Style().map("TButton",
                    background=[("active", "#e74c3c")],
                    foreground=[("active", "#ffffff")])

    title_label = tk.Label(root, text=APP_NAME, font=("Consolas", 24, "bold"), bg="#1c1c1c", fg="#e74c3c")
    title_label.pack(pady=20)

    tool_frame = ttk.Frame(root)
    tool_frame.pack(fill="x", padx=20, pady=10)

    tools = load_tools()
    for tool_name, tool_command in tools.items():
        ttk.Button(tool_frame, text=tool_name, command=lambda cmd=tool_command: run_tool(cmd, context=tool_name)).pack(fill="x", pady=5)

    control_frame = ttk.Frame(root)
    control_frame.pack(fill="x", padx=20, pady=10)

    ttk.Button(control_frame, text="Export Configurations", command=export_config).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Import Configurations", command=import_config).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Export Report", command=export_report).pack(side="left", padx=5)
    ttk.Button(control_frame, text="System Info", command=view_system_info).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Open Documentation", command=open_documentation).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Reset Defaults", command=reset_defaults).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Clear Output", command=lambda: result_text.delete("1.0", tk.END)).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Exit", command=root.quit).pack(side="left", padx=5)

    result_frame = ttk.Frame(root)
    result_frame.pack(fill="both", expand=True, padx=20, pady=20)

    result_text = tk.Text(result_frame, wrap="word", bg="#0e0e0e", fg="#ffffff", font=("Courier", 12), relief="flat", insertbackground="#e74c3c")
    result_text.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    splash_screen()
    create_gui()
    root.mainloop()

# =============================
# User Instructions
# =============================
# - Modify the 'tool_config.json' file to customize tool commands.
# - Ensure dependencies are installed: Nmap, Gobuster, Amass, etc.
# - Run the program using `python3 tasknexus.py`.
# - For custom plugins, add valid JSON files in the 'plugins' directory.
