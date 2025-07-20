
![GitHub release downloads](https://img.shields.io/github/downloads/CyberiusCompany/Cyberius-Unzip-Cracker/latest/total)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![System](https://img.shields.io/badge/windows-x64-green)
![System](https://img.shields.io/badge/linux-x64-green)
![License](https://img.shields.io/badge/license-Private-red)
![Usage](https://img.shields.io/badge/usage-legal%20only-important)
![Python](https://img.shields.io/badge/python-3.7%2B-yellow)
![Tested on](https://img.shields.io/badge/tested%20on-Windows%2010%2F11%20%7C%20Ubuntu%2022.04-blue)

<p align="center">
  <a href="https://github.com/cyberiuscompany/Perm_Scope">
    <img src="https://flagcdn.com/w40/es.png" alt="Español" title="Español">
    <strong>Español</strong>
  </a>
  &nbsp;|&nbsp;
  <img src="https://flagcdn.com/w40/us.png" alt="English" title="English">
  <strong>English</strong>
  &nbsp;|&nbsp;
  <a href="https://www.youtube.com/watch?v=xvFZjo5PgG0&list=RDxvFZjo5PgG0&start_radio=1&pp=ygUTcmljayByb2xsaW5nIG5vIGFkc6AHAQ%3D%3D">
    <img src="https://flagcdn.com/w40/jp.png" alt="Japanese" title="Japanese">
    <strong>日本語</strong>
  </a>
</p>

# PermScope

Local analysis tool for Privilege Escalation and AV/EDR/Firewall Evasion

Compatible with **Windows** and **Linux**. Designed for **pentesters**, sysadmins and cybersecurity enthusiasts.

---

<p align="center">
  <img src="Icono.png" alt="Banner" width="500"/>
</p>

---

## 🧠 What is PermScope?

PermScope is a hybrid tool that allows analysis of insecure configurations on local systems using modular scanning. You can run it via **command-line** or through a modern **graphical interface (GUI)**.

### Key Features:

- Detection of privileged users and groups
- Listing of scheduled tasks and risky services
- Detection of dangerous permissions in files, registry or folders
- Network configuration checks
- Typical evasions for AVs, EDRs and Firewalls
- Executable in **GUI mode** or **CLI mode**

---

## 💻 Project Structure

- perm_scope/
  - modulos/
    - comunes/
    - windows/
    - linux/
  - ventanas/
    - home/
    - cli/
    - about/
  - Icono.ico
  - banner.txt
  - perm_scope.py
  - README.md

---

## 📄 Additional Documentation

- [🔐 Security](.github/SECURITY.md)
- [📜 License](LICENSE)
- [🤝 Code of Conduct](.github/CODE_OF_CONDUCT.md)
- [📬 Contributing](.github/CONTRIBUTING.md)
- [📢 Support](.github/SUPPORT.md)
- [⚠️ Legal Notice](DISCLAIMER.md)

---

## 🎥 Demonstration

<p align="center">
  <img src="docs/perm_scope.gif" width="1200" alt="PermScope Demo">
</p>

## 🖼️ GUI View

<table>
  <tr>
    <td><strong>GUI Mode (Light)</strong></td>
    <td><strong>GUI Mode (Dark)</strong></td>
  </tr>
  <tr>
    <td><img src="Foto Gui Modo Claro.png" alt="Light Mode" width="1020"/></td>
    <td><img src="Foto Gui Modo Oscuro.png" alt="Dark Mode" width="1020"/></td>
  </tr>
</table>

---

## 🖥️ CLI View

<img src="Foto CLI.png" alt="PermScope CLI" width="1000"/>

---

## 🧩 System Requirements

- Python 3.8 or higher  
- Windows 64-bit or 32-bit

---

# 🕵️ Using PermScope

```bash
python perm_scope.py
python perm_scope.py --modo gui
python perm_scope.py --modo consola --listar
python perm_scope.py --modo consola --modulo whoami_all
python perm_scope.py --modo consola --modulo whoami_all,list_hotfixes,kernel_version_check
python perm_scope.py --modo consola --tipo comunes
python perm_scope.py --modo consola --tipo windows
python perm_scope.py --modo consola --tipo linux
```

## ⚙️ Installation

### 1.1 Basic installation with cloning 🪟 Windows

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python perm_scope.py
```
### 1.2 Basic installation with cloning 🐧 Linux

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python perm_scope.py
```

### 2.1 Install as if it were a professional package on 🪟 Windows

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
.\venv\Scripts\activate
pip install .
perm_scope --help
```

### 2.2 Install as if it were a professional package on 🐧 Linux 

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
source venv/bin/activate
pip install .
perm_scope --help
```

### 3.0 Generate compiled .exe in 🪟 Windows

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
pip install pyinstaller
pyinstaller perm_scope.spec

# The .exe file would be in :

Perm_Scope/
├── dist/
│   └── perm_scope.exe   ← ✔️ AQUÍ está el ejecutable final
```
