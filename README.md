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


