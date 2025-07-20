![GitHub release downloads](https://img.shields.io/github/downloads/CyberiusCompany/Cyberius-Unzip-Cracker/latest/total)
![Versión](https://img.shields.io/badge/versión-1.0.0-blue)
![Sistema](https://img.shields.io/badge/windows-x64-green)
![Sistema](https://img.shields.io/badge/linux-x64-green)
![Licencia](https://img.shields.io/badge/licencia-Privada-red)
![Uso](https://img.shields.io/badge/uso-solo%20legal-important)
![Python](https://img.shields.io/badge/python-3.7%2B-yellow)
![Tested on](https://img.shields.io/badge/tested%20on-Windows%2010%2F11%20%7C%20Ubuntu%2022.04-blue)

<p align="center">
  <img src="https://flagcdn.com/w40/es.png" alt="Español" title="Español">
  <strong>Español</strong>
  &nbsp;|&nbsp;
  <a href="README.en.md">
    <img src="https://flagcdn.com/w40/us.png" alt="English" title="English">
    <strong>English</strong>
  </a>
  &nbsp;|&nbsp;
  <a href="https://www.youtube.com/watch?v=xvFZjo5PgG0&list=RDxvFZjo5PgG0&start_radio=1&pp=ygUTcmljayByb2xsaW5nIG5vIGFkc6AHAQ%3D%3D">
    <img src="https://flagcdn.com/w40/jp.png" alt="日本語" title="Japanese">
    <strong>日本語</strong>
  </a>
</p>

# PermScope

Herramienta de Análisis Local para Escalada de Privilegios y Evasiones de AV/EDR/Firewall  

Compatible con **Windows** y **Linux**. Diseñada para **pentesters**, administradores de sistemas y entusiastas de la ciberseguridad.

---

<p align="center">
  <img src="Icono.png" alt="Banner" width="500"/>
</p

---

## 🧠 ¿Qué es PermScope?

PermScope es una herramienta híbrida que permite el análisis de configuraciones inseguras en sistemas locales a través de módulos personalizables. Puedes ejecutarla tanto desde consola como desde una interfaz gráfica intuitiva.

### Funcionalidades destacadas:

- Detección de usuarios y grupos privilegiados
- Listado de tareas programadas y servicios con riesgos
- Detección de permisos peligrosos en archivos, registros o directorios
- Comprobación de configuraciones de red
- Evasiones típicas para AV, EDR y Firewalls
- Ejecutable en **modo gráfico (GUI)** o **modo consola**

---

## 💻 Estructura del proyecto

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

## 📄 Documentación adicional

- [🔐 Seguridad](.github/SECURITY.md)
- [📜 Licencia](LICENSE)
- [🤝 Código de Conducta](.github/CODE_OF_CONDUCT.md)
- [📬 Cómo contribuir](.github/CONTRIBUTING.md)
- [📢 Soporte](.github/SUPPORT.md)
- [⚠️ Aviso legal](DISCLAIMER.md)

---

## 🎥 Demostración

<p align="center">
  <img src="docs/perm_scope.gif" width="1200" alt="Demostración de Perm_Scope">
</p>

## 🖼️ Vista de la herramienta en GUI

<table>
  <tr>
    <td><strong>Modo GUI (Claro)</strong></td>
    <td><strong>Modo GUI (Oscuro)</strong></td>
  </tr>
  <tr>
    <td><img src="Foto Gui Modo Claro.png" alt="Modo claro" width="1020"/></td>
    <td><img src="Foto Gui Modo Oscuro.png" alt="Modo oscuro" width="1020"/></td>
  </tr>
</table>

---

---

## 🖥️ Vista CLI

<img src="Foto CLI.png" alt="CLI PermScope" width="1000"/>

---

## 🧩 Requisitos del sistema

- Python 3.8 o superior  
- Windows 64-bit  o 32-Bits

---

# 🕵️ Uso de PermScope

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

## ⚙️ Instalación

### 1.1 Instalación básica con clonado 🪟 Windows

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python perm_scope.py
```
### 1.2 Instalación básica con clonado 🐧 Linux

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python perm_scope.py
```

### 2.1 Instalación como si fuese paquete profesional en 🪟 Windows 

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
.\venv\Scripts\activate
pip install .
perm_scope --help
```

### 2.2 Instalación como si fuese paquete profesional en 🐧 Linux 

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
python3 -m venv venv
source venv/bin/activate
pip install .
perm_scope --help
```

### 3.0 Generar compilado .exe en 🪟 Windows

```bash
git clone https://github.com/cyberiuscompany/Perm_Scope.git
cd Perm_Scope
pip install pyinstaller
pyinstaller perm_scope.spec

# El fichero .exe estaría en :

Perm_Scope/
├── dist/
│   └── perm_scope.exe   ← ✔️ AQUÍ está el ejecutable final
```




