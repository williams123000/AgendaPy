#!/bin/bash

# Comprobamos si el sistema es Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Si es Windows, usamos el comando 'pip' directamente
    pip install -r requirements.txt
else
    # Si es Linux o macOS, comprobamos si 'pip' está instalado
    if command -v pip3 &>/dev/null; then
        # Si 'pip' está instalado, lo usamos para instalar las dependencias
        pip3 install -r requirements.txt
    elif command -v pip &>/dev/null; then
        # Si 'pip' no está instalado pero 'pip3' sí, lo usamos para instalar las dependencias
        pip install -r requirements.txt
    else
        # Si ni 'pip' ni 'pip3' están instalados, mostramos un mensaje de error
        echo "Error: pip no está instalado. Por favor, instala pip para continuar."
        exit 1
    fi
fi
