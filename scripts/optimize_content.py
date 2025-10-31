#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para optimizar y traducir contenido de páginas al español uruguayo
"""

import re
from pathlib import Path

# Páginas a optimizar
TARGET_FILES = [
    'index.html',
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
    'affiliates.html',
    'about-us.html',
    'contact-us.html',
]

# Diccionario masivo de traducciones
TRANSLATIONS = {
    # Títulos y headings comunes
    'Web Hosting': 'Hosting Web',
    'Best Web Hosting': 'Mejor Hosting Web',
    'Powerful Web Hosting': 'Hosting Web Potente',
    'Fast & Secure': 'Rápido y Seguro',
    'Secure Web Hosting': 'Hosting Web Seguro',
    
    # Botones y CTAs
    'Order Now': 'Ordenar Ahora',
    'Get Started': 'Comenzar',
    'Get Started Now': 'Comenzá Ahora',
    'Buy Now': 'Comprar Ahora',
    'Sign Up': 'Registrarse',
    'Sign Up Now': 'Registrate Ahora',
    'Learn More': 'Conocer Más',
    'View Plans': 'Ver Planes',
    'Choose Plan': 'Elegir Plan',
    'Contact Us': 'Contactanos',
    'Contact Sales': 'Contactar Ventas',
    'Get Support': 'Obtener Soporte',
    'Read More': 'Leer Más',
    'View More': 'Ver Más',
    'Try Free': 'Probar Gratis',
    'Free Trial': 'Prueba Gratuita',
    
    # Features comunes
    'Free Domain': 'Dominio Gratis',
    'Free SSL': 'SSL Gratis',
    'Free SSL Certificate': 'Certificado SSL Gratis',
    'Unlimited Bandwidth': 'Ancho de Banda Ilimitado',
    'Unlimited Storage': 'Almacenamiento Ilimitado',
    'Unlimited Disk Space': 'Espacio en Disco Ilimitado',
    'Daily Backup': 'Respaldo Diario',
    'Daily Backups': 'Respaldos Diarios',
    'Automatic Backups': 'Respaldos Automáticos',
    '24/7 Support': 'Soporte 24/7',
    '24/7 Customer Support': 'Soporte al Cliente 24/7',
    'Technical Support': 'Soporte Técnico',
    'Expert Support': 'Soporte Experto',
    'Live Chat Support': 'Soporte por Chat en Vivo',
    'Phone Support': 'Soporte Telefónico',
    'Email Support': 'Soporte por Email',
    'Free Migration': 'Migración Gratuita',
    'Free Website Migration': 'Migración de Sitio Web Gratuita',
    'One-Click Install': 'Instalación con Un Clic',
    'Easy Setup': 'Configuración Fácil',
    'Quick Setup': 'Configuración Rápida',
    'Instant Setup': 'Configuración Instantánea',
    'Money Back Guarantee': 'Garantía de Devolución de Dinero',
    '30-Day Money Back': 'Devolución de Dinero en 30 Días',
    '45-Day Money Back': 'Devolución de Dinero en 45 Días',
    'Uptime Guarantee': 'Garantía de Uptime',
    '99.9% Uptime': 'Uptime del 99.9%',
    '99.9% Uptime Guarantee': 'Garantía de Uptime del 99.9%',
    
    # Hosting types
    'Shared Hosting': 'Hosting Compartido',
    'VPS Hosting': 'Hosting VPS',
    'Dedicated Hosting': 'Hosting Dedicado',
    'Cloud Hosting': 'Hosting en la Nube',
    'Reseller Hosting': 'Hosting para Revendedores',
    'WordPress Hosting': 'Hosting WordPress',
    'Managed WordPress': 'WordPress Administrado',
    'WooCommerce Hosting': 'Hosting WooCommerce',
    
    # Pricing
    'Starting at': 'Desde',
    'Starting from': 'Desde',
    'Per Month': 'Por Mes',
    'per month': 'por mes',
    '/month': '/mes',
    '/mo': '/mes',
    'Per Year': 'Por Año',
    'per year': 'por año',
    '/year': '/año',
    '/yr': '/año',
    'Save': 'Ahorrá',
    'Off': 'Descuento',
    'Best Value': 'Mejor Valor',
    'Most Popular': 'Más Popular',
    'Recommended': 'Recomendado',
    
    # Technical specs
    'Storage': 'Almacenamiento',
    'Disk Space': 'Espacio en Disco',
    'SSD Storage': 'Almacenamiento SSD',
    'NVMe Storage': 'Almacenamiento NVMe',
    'Bandwidth': 'Ancho de Banda',
    'Transfer': 'Transferencia',
    'Data Transfer': 'Transferencia de Datos',
    'Websites': 'Sitios Web',
    'Domains': 'Dominios',
    'Subdomains': 'Subdominios',
    'Email Accounts': 'Cuentas de Email',
    'Databases': 'Bases de Datos',
    'MySQL Databases': 'Bases de Datos MySQL',
    'FTP Accounts': 'Cuentas FTP',
    'CPU Cores': 'Núcleos de CPU',
    'RAM Memory': 'Memoria RAM',
    'Memory': 'Memoria',
    'IPv4 Address': 'Dirección IPv4',
    'IPv6 Support': 'Soporte IPv6',
    'Root Access': 'Acceso Root',
    'Full Root Access': 'Acceso Root Completo',
    'Control Panel': 'Panel de Control',
    'cPanel': 'cPanel',
    'Plesk': 'Plesk',
    'Custom Control Panel': 'Panel de Control Personalizado',
    
    # Performance
    'High Performance': 'Alto Rendimiento',
    'Fast Loading': 'Carga Rápida',
    'Lightning Fast': 'Velocidad Relámpago',
    'Blazing Fast': 'Extremadamente Rápido',
    'Super Fast': 'Súper Rápido',
    'Speed Optimization': 'Optimización de Velocidad',
    'Performance Boost': 'Impulso de Rendimiento',
    'Optimized Performance': 'Rendimiento Optimizado',
    'Maximum Speed': 'Velocidad Máxima',
    
    # Security
    'Security': 'Seguridad',
    'Secure': 'Seguro',
    'Protection': 'Protección',
    'DDoS Protection': 'Protección DDoS',
    'Malware Protection': 'Protección contra Malware',
    'Malware Scanning': 'Escaneo de Malware',
    'Virus Protection': 'Protección Antivirus',
    'Firewall': 'Firewall',
    'Web Application Firewall': 'Firewall de Aplicaciones Web',
    'Advanced Security': 'Seguridad Avanzada',
    'Security Monitoring': 'Monitoreo de Seguridad',
    'SSL Certificate': 'Certificado SSL',
    'Wildcard SSL': 'SSL Wildcard',
    'Encryption': 'Encriptación',
    
    # Reliability
    'Reliable': 'Confiable',
    'Reliability': 'Confiabilidad',
    'Stable': 'Estable',
    'Stability': 'Estabilidad',
    'Redundant': 'Redundante',
    'High Availability': 'Alta Disponibilidad',
    'Failover': 'Failover',
    'Load Balancing': 'Balanceo de Carga',
    
    # Common phrases
    'Easy to use': 'Fácil de usar',
    'User-friendly': 'Fácil de usar',
    'Simple and easy': 'Simple y fácil',
    'No technical knowledge required': 'No se requiere conocimiento técnico',
    'Perfect for beginners': 'Perfecto para principiantes',
    'Ideal for': 'Ideal para',
    'Best for': 'Mejor para',
    'Designed for': 'Diseñado para',
    'Built for': 'Construido para',
    'Grow your business': 'Hacé crecer tu negocio',
    'Take your business online': 'Llevá tu negocio online',
    'Start your website': 'Comenzá tu sitio web',
    'Launch your website': 'Lanzá tu sitio web',
    'Build your website': 'Construí tu sitio web',
    'Create your website': 'Creá tu sitio web',
    
    # Support & Service
    'Customer Support': 'Soporte al Cliente',
    'Professional Support': 'Soporte Profesional',
    'Dedicated Support': 'Soporte Dedicado',
    'Priority Support': 'Soporte Prioritario',
    'Help Center': 'Centro de Ayuda',
    'Knowledge Base': 'Base de Conocimientos',
    'Video Tutorials': 'Tutoriales en Video',
    'Documentation': 'Documentación',
    'FAQs': 'Preguntas Frecuentes',
    'Frequently Asked Questions': 'Preguntas Frecuentes',
    
    # Company & Trust
    'About Us': 'Quiénes Somos',
    'Our Story': 'Nuestra Historia',
    'Our Team': 'Nuestro Equipo',
    'Our Mission': 'Nuestra Misión',
    'Our Values': 'Nuestros Valores',
    'Why Choose Us': 'Por Qué Elegirnos',
    'What We Do': 'Qué Hacemos',
    'How It Works': 'Cómo Funciona',
    'Testimonials': 'Testimonios',
    'Customer Reviews': 'Reseñas de Clientes',
    'Success Stories': 'Historias de Éxito',
    'Trusted by': 'Confiado por',
    'Join thousands of': 'Unite a miles de',
    'Years of experience': 'Años de experiencia',
    
    # Common words
    'Features': 'Características',
    'Plans': 'Planes',
    'Pricing': 'Precios',
    'Compare': 'Comparar',
    'Comparison': 'Comparación',
    'Overview': 'Resumen',
    'Details': 'Detalles',
    'Specifications': 'Especificaciones',
    'Include': 'Incluye',
    'Includes': 'Incluye',
    'Everything in': 'Todo en',
    'Plus': 'Más',
    'And more': 'Y más',
    'All features': 'Todas las características',
    'Full features': 'Características completas',
    'Complete': 'Completo',
    'Advanced': 'Avanzado',
    'Professional': 'Profesional',
    'Enterprise': 'Empresarial',
    'Business': 'Negocios',
    'Personal': 'Personal',
    'Basic': 'Básico',
    'Standard': 'Estándar',
    'Premium': 'Premium',
    'Ultimate': 'Ultimate',
    'Unlimited': 'Ilimitado',
    'Unmetered': 'Sin Medición',
    'Custom': 'Personalizado',
    'Customizable': 'Personalizable',
    'Flexible': 'Flexible',
    'Scalable': 'Escalable',
    'Powerful': 'Potente',
    'Robust': 'Robusto',
    'Comprehensive': 'Completo',
    'Complete': 'Completo',
    'Full': 'Completo',
    'Total': 'Total',
    'Maximum': 'Máximo',
    'Minimum': 'Mínimo',
    'Optional': 'Opcional',
    'Required': 'Requerido',
    'Included': 'Incluido',
    'Available': 'Disponible',
    'Coming Soon': 'Próximamente',
    'New': 'Nuevo',
    'Updated': 'Actualizado',
    'Latest': 'Último',
    'Popular': 'Popular',
    'Trending': 'Tendencia',
    'Best Seller': 'Más Vendido',
}

# Traducciones de frases largas (regex patterns)
PHRASE_TRANSLATIONS = [
    (r'Get your website online in minutes', 'Poné tu sitio web online en minutos'),
    (r'Everything you need to', 'Todo lo que necesitás para'),
    (r'The perfect solution for', 'La solución perfecta para'),
    (r'Choose the plan that\'s right for you', 'Elegí el plan que sea perfecto para vos'),
    (r'All plans include', 'Todos los planes incluyen'),
    (r'No hidden fees', 'Sin cargos ocultos'),
    (r'Cancel anytime', 'Cancelá cuando quieras'),
    (r'Try risk-free', 'Probá sin riesgo'),
    (r'No credit card required', 'No se requiere tarjeta de crédito'),
    (r'Satisfaction guaranteed', 'Satisfacción garantizada'),
]

def translate_content(content):
    """Aplica todas las traducciones al contenido"""
    changes = 0
    
    # Traducciones exactas
    for english, spanish in TRANSLATIONS.items():
        if english in content:
            count = content.count(english)
            content = content.replace(english, spanish)
            changes += count
    
    # Traducciones de frases con regex
    for pattern, replacement in PHRASE_TRANSLATIONS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            changes += len(matches)
    
    return content, changes

def optimize_page(filepath):
    """Optimiza y traduce una página HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content, changes = translate_content(content)
        
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
    
    print("🌐 Optimizando contenido de páginas al español uruguayo...")
    print(f"📁 Directorio base: {base_dir}")
    print(f"📄 Archivos a procesar: {len(TARGET_FILES)}\n")
    
    total_changes = 0
    files_modified = 0
    files_skipped = 0
    
    for filename in TARGET_FILES:
        filepath = base_dir / filename
        print(f"Procesando: {filename}...", end=' ')
        
        changes = optimize_page(filepath)
        
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
