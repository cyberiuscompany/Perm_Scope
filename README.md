# 🛡️ PermScope

![GitHub release downloads](https://img.shields.io/github/downloads/CyberiusCompany/Cyberius-Unzip-Cracker/latest/total)
![Versión](https://img.shields.io/badge/versión-1.0.0-blue)
![Sistema](https://img.shields.io/badge/windows-x64-green)
![Sistema](https://img.shields.io/badge/linux-x64-blue)
![Licencia](https://img.shields.io/badge/licencia-Privada-red)
![Uso](https://img.shields.io/badge/uso-solo%20legal-important)
![Estado](https://img.shields.io/badge/release-estable-brightgreen)
![Python](https://img.shields.io/badge/python-3.7%2B-yellow)
![Interfaz](https://img.shields.io/badge/interfaz-GUI%20%2B%20CLI-lightgrey)

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

## 🖼️ Vista de la herramienta

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

### 1. Clonar o descargar el repositorio

Puedes clonar o descargar este proyecto y usarlo directamente con Python:

```bash
git clone https://github.com/cyberiuscompany/PermScope.git
cd PermScope
pip install -r requirements.txt
python perm_scope.py
```

### 2. Instalación profesional como paquete

```bash
git clone https://github.com/cyberiuscompany/PermScope.git
cd PermScope
pip install .
perm_scope --help
```

### 3. Compilación a formato `.exe`

Si deseas generar un archivo ejecutable (`.exe`) de **Perm_Scope**  con su icono personalizado sigue estos pasos:

Esto generará el archivo ejecutable dentro de la carpeta:
- dist/perm_scope/perm_scope.exe

#### Pasos:

```bash
git clone https://github.com/cyberiuscompany/PermScope.git
cd perm_scope
pip install pyinstaller
pyinstaller CyberiusUnzipCracker.spec
```
