#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para traducir menús en todas las páginas HTML del sitio
Aplica las mismas traducciones que se hicieron en alojamiento-web.html
"""

import os
import re
from pathlib import Path

# Lista de páginas a procesar
TARGET_FILES = [
    'index.html',
    'buscador-de-dominios.html',
    'registro-de-dominios.html',
    'transferencia-de-dominios.html',
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

# Mapa de traducciones exactas (case-sensitive)
TRANSLATIONS = {
    # Menú principal
    '>Domain<': '>Dominios<',
    '>Home<': '>Inicio<',
    
    # Domain submenu items
    'Domain Checker': 'Buscador de Dominios',
    'Domain Transfer': 'Transferencia de Dominios',
    'Domain Registration': 'Registro de Dominios',
    
    # Hosting submenu items
    'Shared Web Hosting': 'Hosting Web Compartido',
    'VPS Hosting': 'Hosting VPS',
    'Cloud Hosting': 'Hosting en la Nube',
    'Email Hosting': 'Hosting de Email',
    'Windows VPS Hosting': 'Hosting VPS Windows',
    'Dedicated Server Hosting': 'Hosting Servidor Dedicado',
    
    # Application names
    'WordPress Hosting': 'Hosting WordPress',
    'Joomla Hosting': 'Hosting Joomla',
    'Magento Hosting': 'Hosting Magento',
    'Opencart Hosting': 'Hosting Opencart',
    'Prestashop Hosting': 'Hosting Prestashop',
    'Drupal Hosting': 'Hosting Drupal',
    
    # Section titles
    'Application For Hosting': 'Aplicaciones para Hosting',
    
    # Descriptive texts
    'Find the perfect domain for your business': 'Encontrá el dominio perfecto para tu negocio',
    'Transfer your domain easily': 'Transferí tu dominio fácilmente',
    'Register your domain name for lifetime': 'Registrá tu nombre de dominio de por vida',
    
    'Reliable quality Starting at': 'Calidad confiable desde',
    'Maintain Starting at': 'Mantenimiento desde',
    'Cloud Starting at': 'Cloud desde',
    'First Starting at': 'Primero desde',
    'Globally Starting at': 'Global desde',
    'Conveniently Starting at': 'Convenientemente desde',
    
    # Price format
    '$0.99/mo': '$0.99/mes',
    '$2.99/mo': '$2.99/mes',
    '$5.99/mo': '$5.99/mes',
    '$9.99/mo': '$9.99/mes',
    '$11.99/mo': '$11.99/mes',
    
    # Feature panel
    '#1 Web Hosting Company': 'Empresa N.º 1 en Hosting Web',
    '<strong>Flexible</strong>\n                                                            Easy to Use Control Panel': '<strong>Panel de Control</strong>\n                                                            Flexible y Fácil de Usar',
    '<strong>99%</strong>\n                                                            Uptime Guarantee': '<strong>Garantía de Uptime</strong>\n                                                            del 99%',
    '<strong>45-Day</strong>\n                                                            Money-Back Guarantee': '<strong>Garantía de Devolución</strong>\n                                                            de 45 Días',
    '<strong>Free SSL</strong>\n                                                            Certificate Included': '<strong>Certificado SSL Gratis</strong>\n                                                            Incluido',
    
    # Buttons
    'Learn More': 'Conocer Más',
}

# Traducciones con espacios variables (regex)
REGEX_TRANSLATIONS = [
    # Control panel - flexible pattern
    (r'<strong>Flexible</strong>\s+Easy to Use Control Panel', 
     '<strong>Panel de Control</strong> Flexible y Fácil de Usar'),
    
    # Uptime guarantee
    (r'<strong>99%</strong>\s+Uptime Guarantee', 
     '<strong>Garantía de Uptime</strong> del 99%'),
    
    # Money back guarantee
    (r'<strong>45-Day</strong>\s+Money-Back Guarantee', 
     '<strong>Garantía de Devolución</strong> de 45 Días'),
    
    # SSL certificate
    (r'<strong>Free SSL</strong>\s+Certificate Included', 
     '<strong>Certificado SSL Gratis</strong> Incluido'),
]

def translate_file(filepath):
    """Traduce los menús en un archivo HTML"""
    try:
        # Leer archivo
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # Aplicar traducciones exactas
        for english, spanish in TRANSLATIONS.items():
            if english in content:
                count = content.count(english)
                content = content.replace(english, spanish)
                changes += count
        
        # Aplicar traducciones regex
        for pattern, replacement in REGEX_TRANSLATIONS:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes += len(matches)
        
        # Guardar solo si hubo cambios
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
    base_dir = Path(__file__).parent.parent
    
    print("🌐 Iniciando traducción de menús...")
    print(f"📁 Directorio base: {base_dir}")
    print(f"📄 Archivos a procesar: {len(TARGET_FILES)}\n")
    
    total_changes = 0
    files_modified = 0
    files_skipped = 0
    
    for filename in TARGET_FILES:
        filepath = base_dir / filename
        print(f"Procesando: {filename}...", end=' ')
        
        changes = translate_file(filepath)
        
        if changes == -1:
            files_skipped += 1
            continue
        elif changes > 0:
            print(f"✅ {changes} traducciones aplicadas")
            files_modified += 1
            total_changes += changes
        else:
            print("⏭️  Sin cambios necesarios")
    
    print(f"\n{'='*60}")
    print(f"✨ Proceso completado:")
    print(f"   • Archivos modificados: {files_modified}")
    print(f"   • Archivos sin cambios: {len(TARGET_FILES) - files_modified - files_skipped}")
    print(f"   • Archivos no encontrados: {files_skipped}")
    print(f"   • Total de traducciones: {total_changes}")
    print(f"{'='*60}")
    
    return files_modified

if __name__ == '__main__':
    exit(main())
