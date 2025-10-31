#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para aplicar la estructura de menú simplificada desde alojamiento-web.html
a todas las páginas de hosting, dominios y company
"""

import re
from pathlib import Path

# Páginas que necesitan la estructura de menú actualizada
TARGET_FILES = [
    # Hosting pages
    'vps-hosting.html',
    'cloud-hosting.html',
    'email-hosting.html',
    'windows-vps-hosting.html',
    'dedicated-server-hosting.html',
    # Application hosting
    'wp-hosting.html',
    'joomla-hosting.html',
    'magento-hosting.html',
    'opencart-hosting.html',
    'prestashop-hosting.html',
    'drupal-hosting.html',
    # Company pages
    'affiliates.html',
    'about-us.html',
    'contact-us.html',
]

def extract_menu_from_source():
    """Extrae el menú desktop y offcanvas de alojamiento-web.html"""
    source_file = Path('alojamiento-web.html')
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer menú desktop (desde <!--main menu start--> hasta <!--main menu end-->)
    desktop_pattern = r'(<!--main menu start-->.*?<!--main menu end-->)'
    desktop_match = re.search(desktop_pattern, content, re.DOTALL)
    desktop_menu = desktop_match.group(1) if desktop_match else None
    
    # Extraer offcanvas menu (desde <!--offcanvas menu start--> hasta <!--offcanvas menu end-->)
    offcanvas_pattern = r'(<!--offcanvas menu start-->.*?<!--offcanvas menu end-->)'
    offcanvas_match = re.search(offcanvas_pattern, content, re.DOTALL)
    offcanvas_menu = offcanvas_match.group(1) if offcanvas_match else None
    
    return desktop_menu, offcanvas_menu

def replace_menu_in_file(filepath, desktop_menu, offcanvas_menu):
    """Reemplaza los menús en un archivo HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # Reemplazar menú desktop
        if desktop_menu:
            desktop_pattern = r'<!--main menu start-->.*?<!--main menu end-->'
            if re.search(desktop_pattern, content, re.DOTALL):
                content = re.sub(desktop_pattern, desktop_menu, content, flags=re.DOTALL)
                changes += 1
        
        # Reemplazar offcanvas menu
        if offcanvas_menu:
            offcanvas_pattern = r'<!--offcanvas menu start-->.*?<!--offcanvas menu end-->'
            if re.search(offcanvas_pattern, content, re.DOTALL):
                content = re.sub(offcanvas_pattern, offcanvas_menu, content, flags=re.DOTALL)
                changes += 1
        
        # Guardar si hubo cambios
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes
        
        return 0
        
    except FileNotFoundError:
        print(f"⚠️  Archivo no encontrado: {filepath}")
        return -1
    except Exception as e:
        print(f"❌ Error procesando {filepath}: {e}")
        return -1

def main():
    """Procesa todos los archivos objetivo"""
    print("🔄 Extrayendo estructura de menú desde alojamiento-web.html...")
    
    desktop_menu, offcanvas_menu = extract_menu_from_source()
    
    if not desktop_menu or not offcanvas_menu:
        print("❌ No se pudieron extraer los menús de alojamiento-web.html")
        return 1
    
    print(f"✅ Menú desktop extraído: {len(desktop_menu)} caracteres")
    print(f"✅ Menú offcanvas extraído: {len(offcanvas_menu)} caracteres\n")
    
    print(f"📄 Aplicando estructura a {len(TARGET_FILES)} archivos...\n")
    
    files_modified = 0
    files_skipped = 0
    total_changes = 0
    
    for filename in TARGET_FILES:
        print(f"Procesando: {filename}...", end=' ')
        
        changes = replace_menu_in_file(filename, desktop_menu, offcanvas_menu)
        
        if changes == -1:
            files_skipped += 1
            continue
        elif changes > 0:
            print(f"✅ {changes} menús actualizados")
            files_modified += 1
            total_changes += changes
        else:
            print("⏭️  Sin cambios (menú ya actualizado)")
    
    print(f"\n{'='*60}")
    print(f"✨ Proceso completado:")
    print(f"   • Archivos modificados: {files_modified}")
    print(f"   • Archivos sin cambios: {len(TARGET_FILES) - files_modified - files_skipped}")
    print(f"   • Archivos no encontrados: {files_skipped}")
    print(f"   • Total de menús reemplazados: {total_changes}")
    print(f"{'='*60}")
    
    return 0

if __name__ == '__main__':
    exit(main())
