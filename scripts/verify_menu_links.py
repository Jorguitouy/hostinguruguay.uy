#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que todos los enlaces del menú en alojamiento-web.html existen
"""

import os
from pathlib import Path

# Enlaces del menú desde alojamiento-web.html
MENU_LINKS = {
    'Inicio': 'index.html',
    'Hosting > Alojamiento Web': 'alojamiento-web.html',
    'Hosting > VPS': 'vps-hosting.html',
    'Hosting > Cloud': 'cloud-hosting.html',
    'Hosting > Email': 'email-hosting.html',
    'Hosting > Windows VPS': 'windows-vps-hosting.html',
    'Hosting > Servidor Dedicado': 'dedicated-server-hosting.html',
    'Hosting > WordPress': 'wp-hosting.html',
    'Hosting > Joomla': 'joomla-hosting.html',
    'Hosting > Magento': 'magento-hosting.html',
    'Hosting > OpenCart': 'opencart-hosting.html',
    'Hosting > PrestaShop': 'prestashop-hosting.html',
    'Hosting > Drupal': 'drupal-hosting.html',
    'Dominios > Buscador': 'buscador-de-dominios.html',
    'Dominios > Transferencia': 'transferencia-de-dominios.html',
    'Dominios > Registro': 'registro-de-dominios.html',
    'Afiliados': 'affiliates.html',
    'Quiénes Somos': 'about-us.html',
    'Contacto': 'contact-us.html',
}

def verify_links():
    """Verifica que todos los archivos del menú existen"""
    base_dir = Path(__file__).parent.parent
    
    print("🔍 Verificando enlaces del menú en alojamiento-web.html...\n")
    print(f"📁 Directorio base: {base_dir}\n")
    
    all_exist = True
    missing_files = []
    existing_files = []
    
    for menu_item, filename in MENU_LINKS.items():
        filepath = base_dir / filename
        
        if filepath.exists():
            print(f"✅ {menu_item:40} → {filename}")
            existing_files.append(filename)
        else:
            print(f"❌ {menu_item:40} → {filename} (NO EXISTE)")
            missing_files.append((menu_item, filename))
            all_exist = False
    
    print(f"\n{'='*80}")
    print(f"📊 Resumen:")
    print(f"   • Total de enlaces: {len(MENU_LINKS)}")
    print(f"   • Archivos existentes: {len(existing_files)}")
    print(f"   • Archivos faltantes: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️  ARCHIVOS FALTANTES:")
        for menu_item, filename in missing_files:
            print(f"   • {menu_item} → {filename}")
        print(f"\n{'='*80}")
        return 1
    else:
        print(f"\n✨ Todos los enlaces del menú apuntan a archivos existentes!")
        print(f"{'='*80}")
        return 0

if __name__ == '__main__':
    exit(verify_links())
