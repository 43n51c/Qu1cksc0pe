#!/usr/bin/python3

import os
import readline
import sys
import glob
import getpass

# Testing prompt_toolkit existence
try:
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.completion import NestedCompleter
    from prompt_toolkit.styles import Style
except:
    print("Error: >prompt_toolkit< module not found.")
    sys.exit(1)

# Testing puremagic existence
try:
    import puremagic as pr
except:
    print("Error: >puremagic< module not found.")
    sys.exit(1)

# Testing pyaxmlparser existence
try:
    import pyaxmlparser
except:
    print("Error: >pyaxmlparser< module not found.")
    sys.exit(1)

try:
    from rich import print
except:
    print("Error: >rich< module not found.")
    sys.exit(1)

try:
    from colorama import Fore, Style
except:
    print("Error: >colorama< module not found.")
    sys.exit(1)

# Colors
red = Fore.LIGHTRED_EX
cyan = Fore.LIGHTCYAN_EX
white = Style.RESET_ALL

# Legends
infoC = f"{cyan}[{red}*{cyan}]{white}"
infoS = f"[bold cyan][[bold red]*[bold cyan]][white]"
foundS = f"[bold cyan][[bold red]+[bold cyan]][white]"
errorS = f"[bold cyan][[bold red]![bold cyan]][white]"

# Path variable
sc0pe_path = open(".path_handler", "r").read()

# Gathering username
username = getpass.getuser()

# User home detection
homeD = "/home"
if sys.platform == "darwin":
    homeD = "/Users"

console_style = Style.from_dict({
    # User input (default text).
    'input':          '#ff0066',

    # Prompt.
    'wall1': 'ansicyan',
    'program': 'ansired underline',
    'wall2':    'ansicyan',
    'shell':    '#00aa00',
})

console_output = [
    ('class:wall1', '['),
    ('class:program', 'Qu1cksc0pe'),
    ('class:wall2', ']'),
    ('class:shell', '>> '),
    ('class:input', ''),
]

# File path completer
def complete(text, state):
    return (glob.glob(text+"*")+[None])[state]
readline.set_completer_delims(" \t\n;")
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

# Message
print(f"{infoS} Entering interactive shell mode...")

# Parsing commands
console_commands = NestedCompleter.from_nested_dict({
    "analyze": {
        "windows",
        "linux",
        "android",
        "osx"
    },
    "set": {
        "target-file",
        "target-folder"
    },
    "document": None,
    "domain": None,
    "language": None,
    "metadata": None,
    "packer": None,
    "resource-scan": None,
    "sigcheck": None,
    "health": None,
    "hash-scan": None,
    "exit": None,
    "clear": None,
    "key_init": None,
    "virustotal": None
})

try:
    while True:
        # Print target file or folder if it is specified
        if os.path.exists(".target-file.txt"):
            targ_file = open(".target-file.txt", "r").read()
            con_targ1 = os.path.split(targ_file)[1]
        else:
            con_targ1 = f"[red]Not specified[white]."

        if os.path.exists(".target-folder.txt"):
            targ_fold = open(".target-folder.txt", "r").read()
        else:
            targ_fold = f"[red]Not specified[white]."

        # Console output
        print(f"\n[bold cyan][[white]Target File: [bold green]{con_targ1}[white] {yellow}|[white] Target Folder: [bold green]{targ_fold}[bold cyan]]")
        con_command = prompt(console_output, style=console_style, completer=console_commands)

        # Exit and clear everything
        if con_command == "exit":
            junkFiles = ["temp.txt", ".path_handler", "elves.txt", ".target-file.txt", ".target-folder.txt"]
            for junk in junkFiles:
                if os.path.exists(junk):
                    os.remove(junk)
            print(f"\n{infoS} Goodbye :3")
            sys.exit(0)

        # Simple clear command
        elif con_command == "clear":
            os.system("clear")

        # Specifying target file
        elif con_command == "set target-file":
            filename = str(input(f"{infoC} Enter full path of target file: "))
            if os.path.isfile(filename):
                with open(".target-file.txt", "w") as tfile:
                    tfile.write(filename)
            else:
                print(f"{errorS} Please enter a correct file.")

        # Specifying target folder
        elif con_command == "set target-folder":
            foldername = str(input(f"{infoC} Enter full path of target folder: "))
            if os.path.isdir(foldername):
                with open(".target-folder.txt", "w") as tfolder:
                    tfolder.write(foldername)
            else:
                print(f"{errorS} Please enter a correct folder.")

        # Windows analysis
        elif con_command == "analyze windows":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                print(f"\n{infoS} Analyzing: [bold green]{filename}[white]")
                fileType = str(pr.magic_file(filename))
                if "Windows Executable" in fileType or ".msi" in fileType or ".dll" in fileType or ".exe" in fileType:
                    print(f"{infoS} Target OS: [bold green]Windows[white]\n")
                    command = f"python3 {sc0pe_path}/Modules/winAnalyzer.py {filename}"
                    os.system(command)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Linux Analysis
        elif con_command == "analyze linux":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                print(f"\n{infoS} Analyzing: [bold green]{filename}[white]")
                fileType = str(pr.magic_file(filename))
                if "ELF" in fileType:
                    if os.path.exists("/usr/bin/strings"):
                        command = f"strings --all {filename} > temp.txt"
                        os.system(command)
                        print(f"{infoS} Target OS: [bold green]Linux[white]\n")
                        command = f"readelf -a {filename} > elves.txt"
                        os.system(command)
                        command = f"python3 {sc0pe_path}/Modules/linAnalyzer.py {filename}"
                        os.system(command)
                        os.remove(f"{sc0pe_path}/temp.txt")
                    else:
                        print(f"{errorS} [bold green]strings[white] command not found. You need to install it.")
                        sys.exit(1)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # MacOSX Analysis
        elif con_command == "analyze osx":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                print(f"\n{infoS} Analyzing: [bold green]{filename}[white]")
                fileType = str(pr.magic_file(filename))
                if "Mach-O" in fileType:
                    if os.path.exists("/usr/bin/strings"):
                        command = f"strings --all {filename} > temp.txt"
                        os.system(command)
                        print(f"{infoS} Target OS: [bold green]OSX[white]\n")
                        command = f"python3 {sc0pe_path}/Modules/osXAnalyzer.py {filename}"
                        os.system(command)
                        os.remove(f"{sc0pe_path}/temp.txt")
                    else:
                        print(f"{errorS} [bold green]strings[white] command not found. You need to install it.")
                        sys.exit(1)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Android Analysis
        elif con_command == "analyze android":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                print(f"\n{infoS} Analyzing: [bold green]{filename}[white]")
                fileType = str(pr.magic_file(filename))
                if "PK" in fileType and "Java archive" in fileType:
                    look = pyaxmlparser.APK(filename)
                    if look.is_valid_APK() == True:
                        if os.path.exists("/usr/bin/strings"):
                            command = f"strings --all {filename} > temp.txt"
                            os.system(command)
                            print(f"{infoS} Target OS: [bold green]Android[white]")
                            command = f"apkid -j {filename} > apkid.json"
                            os.system(command)
                            command = f"python3 {sc0pe_path}/Modules/apkAnalyzer.py {filename}"
                            os.system(command)
                            if os.path.exists("apkid.json"):
                                os.remove("apkid.json")
                            os.remove(f"{sc0pe_path}/temp.txt")
                        else:
                            print(f"{errorS} [bold green]strings[white] command not found. You need to install it.")
                            sys.exit(1)
                else:
                    print(f"{errorS} Qu1cksc0pe doesn\'t support archive analysis for now ;)")
                    sys.exit(1)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Document Analysis
        elif con_command == "document":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                print(f"{infoS} Analyzing: [bold green]{filename}[white]")
                command = f"python3 {sc0pe_path}/Modules/nonExecAnalyzer.py {filename}"
                os.system(command)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Domain extractor
        elif con_command == "domain":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                if os.path.exists("/usr/bin/strings"):
                    command = f"strings --all {filename} > temp.txt"
                    os.system(command)
                    command = f"python3 {sc0pe_path}/Modules/domainCatcher.py {filename}"
                    os.system(command)
                    os.remove(f"{sc0pe_path}/temp.txt")
                else:
                    print(f"{errorS} [bold green]strings[white] command not found. You need to install it.")
                    sys.exit(1)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Language Detection
        elif con_command == "language":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                if os.path.exists("/usr/bin/strings"):
                    command = f"strings --all {filename} > temp.txt"
                    os.system(command)
                    command = f"python3 {sc0pe_path}/Modules/languageDetect.py {filename}"
                    os.system(command)
                    os.remove(f"{sc0pe_path}/temp.txt")
                else:
                    print(f"{errorS} [bold green]strings[white] command not found. You need to install it.")
                    sys.exit(1)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Packer Detection
        elif con_command == "packer":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                command = f"python3 {sc0pe_path}/Modules/packerAnalyzer.py {filename} --single"
                os.system(command)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Hash Scanner
        elif con_command == "hash-scan":
            if os.path.exists(".target-folder.txt"):
                foldername = open(".target-folder.txt", "r").read()
                command = f"python3 {sc0pe_path}/Modules/hashScanner.py {foldername} --multiscan"
                os.system(command)
            else:
                print(f"{errorS} You must specify target folder with [bold green]set target-folder[white] command.")

         # File signature analysis
        elif con_command == "sigcheck":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                command = f"python3 {sc0pe_path}/Modules/sigChecker.py {filename}"
                os.system(command)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # Setup health checker
        elif con_command == "health":
            command = f"python3 {sc0pe_path}/Modules/checkHealth.py"
            os.system(command)

        # Metadata analyzer
        elif con_command == "metadata":
            if os.path.exists(".target-file.txt"):
                foldername = open(".target-file.txt", "r").read()
                command = f"python3 {sc0pe_path}/Modules/metadata.py {filename}"
                os.system(command)
            else:
                print(f"{errorS} You must specify target folder with [bold green]set target-folder[white] command.")

        # Packer Detection
        elif con_command == "resource-scan":
            if os.path.exists(".target-file.txt"):
                filename = open(".target-file.txt", "r").read()
                command = f"python3 {sc0pe_path}/Modules/resourceChecker.py {filename}"
                os.system(command)
            else:
                print(f"{errorS} You must specify target file with [bold green]set target-file[white] command.")

        # VirusTotal API Key import
        elif con_command == "key_init":
            try:
                if os.path.exists(f"{homeD}/{username}/sc0pe_Base/"):
                    pass
                else:
                    os.system(f"mkdir {homeD}/{username}/sc0pe_Base/")

                apikey = str(input(f"{infoC} Enter your VirusTotal API key: "))
                apifile = open(f"{homeD}/{username}/sc0pe_Base/sc0pe_VT_apikey.txt", "w")
                apifile.write(apikey)
                print(f"{foundS} Your VirusTotal API key saved. You must restart the program!")
                sys.exit(0)
            except KeyboardInterrupt:
                print(f"{errorS} Program terminated by user.")

        # VirusTotal scan
        elif con_command == "virustotal":
            # if there is no key quit
            try:
                directory = f"{homeD}/{username}/sc0pe_Base/sc0pe_VT_apikey.txt"
                apik = open(directory, "r").read().split("\n")
            except:
                print(f"{errorS} Use key_init to enter your key.")
                sys.exit(1)
            # if key is not valid quit
            if apik[0] == '' or apik[0] is None or len(apik[0]) != 64:
                print(apik[0])
                print(f"{errorS} Please get your API key from -> [bold green]https://www.virustotal.com/[white]")
                sys.exit(1)
            else:
                command = f"python3 {sc0pe_path}/Modules/VTwrapper.py {apik[0]} {filename}"
                os.system(command)

        # Wrong command
        else:
            print(f"{errorS} Wrong command :(")

except Exception as err:
    print(err)
    sys.exit(1)