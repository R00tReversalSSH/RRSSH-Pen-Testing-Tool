# RRSSH-Pen-Testing-Tool
A comprehensive, user-friendly penetration testing toolkit designed to streamline security assessments

Shout out to !HACKFORUMS.NET!


**Version**: 1.0.0  
**License**: MIT License  

R00tReversalSSH's Pen Testing Toolkit is a powerful, open-source ethical hacking tool designed to simplify penetration testing and network analysis. I made it with the standard go-to tools. But leaving the source-code open for FULL customization & integration . You can EASILY intergrate all the tools on your Linux/Windows machines for optimal ease of use. With a sleek interface, it brings commonly used tools into one cohesive application. MAKE SURE TO CONFIGURE THE SCRIPT TO YOUR NEEDS!!! OR IT WONT WORK! I have created comments within the script to help the skidz. Enjoy, Learn, & HackThePlanet!

---

## Features
- **Tool Integration**: Run popular tools like `Nmap`, `Gobuster`, and `Amass` directly from the interface.
- **Custom Plugins**: Add your own tools via the modular plugin system.
- **Report Generation**: Save results as beautifully formatted HTML reports.
- **System Information**: Monitor CPU, memory, and disk usage during tests.
- **Configuration Management**: Easily export and import tool configurations.

---

## Installation

### Prerequisites
- **Python**: Version 3.8 or higher is required.
- **Dependencies**:
  Install required Python libraries:
  ```bash
  pip install psutil

Ensure the following tools are installed on your system:

1.Nmap
2.Gobuster
3.Amass
4.tcpdump
5.aircrack-ng
6.netcat

USAGE
------
1.python3 tasknexus.pyCustomize 

Tool Configurations:
2.Edit tool_config.json to add or modify tools and their commands.
3.Plugins: Add JSON files to the plugins directory for additional tools.
4.Export Reports: Save results as an HTML report for sharing or documentation



Default Tools
----------------
Nmap: Network scanning and enumeration.
Gobuster: Directory and subdomain brute-forcing.
Amass: Subdomain enumeration.
tcpdump: Network traffic analysis.
aircrack-ng: Wi-Fi security testing.
netcat: Port scanning and network connectivity testing.

Contributions are welcome! Feel free to fork the repository and submit a pull request. For major changes, please open an issue to discuss your ideas.

DISCLAIMER
___________________________________________________________________________
This toolkit is for ethical use only. Unauthorized use of this tool in violation of laws is strictly prohibited. By using this software, you agree to take full responsibility for your actions.
___________________________________________________________________________
License
This project is licensed under the MIT License. See the LICENSE file for details.


