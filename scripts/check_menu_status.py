#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar el estado del menú y traducciones en todas las páginas
"""

import re
from pathlib import Path

# Páginas del menú
MENU_PAGES = [
    'index.html',
    'alojamiento-web.html',
    'vps-hosting.html',
    'cloud-hosting.html',
    'email-hosting.html',
    'windows-vps-hosting.html',
    'dedicated-server-hosting.html',
    'wp-hosting.html',
    'joomla-hosting.html',
    'magento-hosting.html',
    'opencart-hosting.html',
    'prestashop-hosting.html',
    'drupal-hosting.html',
    'buscador-de-dominios.html',
    'transferencia-de-dominios.html',
    'registro-de-dominios.html',
    'affiliates.html',
    'about-us.html',
    'contact-us.html',
]

def check_page_menu(filepath):
    """Verifica el estado del menú en una página"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {
            'has_simplified_menu': False,
            'has_inicio': False,
            'has_dominios': False,
            'has_hosting': False,
            'has_home_megamenu': False,
            'has_pages_dropdown': False,
            'menu_is_translated': False,
        }
        
        # Verificar estructura simplificada
        results['has_simplified_menu'] = '<!--inicio start-->' in content or '<!--inicio end-->' in content
        
        # Verificar presencia de elementos clave
        results['has_inicio'] = '>Inicio<' in content
        results['has_dominios'] = '>Dominios<' in content
        results['has_hosting'] = '>Hosting<' in content
        
        # Verificar elementos viejos que NO deben estar
        results['has_home_megamenu'] = 'homeMegaMenu' in content and 'Home different style' in content
        results['has_pages_dropdown'] = '>Pages<' in content and 'pricing-default.html' in content
        
        # Verificar si está traducido (buscar textos en inglés del menú)
        english_patterns = [
            'Domain Checker',
            'Domain Transfer',
            'Domain Registration',
            'Shared Web Hosting',
            'VPS Hosting',
            'Cloud Hosting',
            'Email Hosting',
        ]
        
        has_english = any(pattern in content for pattern in english_patterns)
        results['menu_is_translated'] = not has_english
        
        return results
        
    except Exception as e:
        return None

def generate_report():
    """Genera reporte del estado de todas las páginas"""
    base_dir = Path(__file__).parent.parent
    
    print("📋 REPORTE DE ESTADO DEL MENÚ Y TRADUCCIONES\n")
    print("="*100)
    print(f"{'Página':<35} {'Menú':<12} {'Traducido':<12} {'Inicio':<8} {'Hosting':<9} {'Dominios':<10} {'Problemas'}")
    print("="*100)
    
    total_ok = 0
    total_warnings = 0
    total_errors = 0
    
    for filename in MENU_PAGES:
        filepath = base_dir / filename
        
        if not filepath.exists():
            print(f"{filename:<35} {'❌ NO EXISTE':^12}")
            total_errors += 1
            continue
        
        results = check_page_menu(filepath)
        
        if results is None:
            print(f"{filename:<35} {'❌ ERROR':^12}")
            total_errors += 1
            continue
        
        # Determinar estado
        menu_status = '✅ Simple' if results['has_simplified_menu'] else '⚠️ Antiguo'
        translated = '✅ Sí' if results['menu_is_translated'] else '❌ No'
        inicio = '✅' if results['has_inicio'] else '❌'
        hosting = '✅' if results['has_hosting'] else '❌'
        dominios = '✅' if results['has_dominios'] else '❌'
        
        # Detectar problemas
        problems = []
        if results['has_home_megamenu']:
            problems.append('Home mega-menu')
        if results['has_pages_dropdown']:
            problems.append('Pages dropdown')
        if not results['menu_is_translated']:
            problems.append('Sin traducir')
        if not results['has_simplified_menu']:
            problems.append('Menú antiguo')
        
        problems_str = ', '.join(problems) if problems else '✅ OK'
        
        print(f"{filename:<35} {menu_status:^12} {translated:^12} {inicio:^8} {hosting:^9} {dominios:^10} {problems_str}")
        
        if problems:
            if 'Sin traducir' in problems or 'Menú antiguo' in problems:
                total_errors += 1
            else:
                total_warnings += 1
        else:
            total_ok += 1
    
    print("="*100)
    print(f"\n📊 RESUMEN:")
    print(f"   • Páginas OK: {total_ok}")
    print(f"   • Advertencias: {total_warnings}")
    print(f"   • Errores: {total_errors}")
    print(f"   • Total: {len(MENU_PAGES)}")
    
    if total_errors > 0:
        print(f"\n⚠️  Hay {total_errors} páginas con problemas que requieren atención")
        return 1
    elif total_warnings > 0:
        print(f"\n⚠️  Hay {total_warnings} páginas con advertencias menores")
        return 0
    else:
        print(f"\n✨ Todas las páginas están correctamente configuradas!")
        return 0

if __name__ == '__main__':
    exit(generate_report())
