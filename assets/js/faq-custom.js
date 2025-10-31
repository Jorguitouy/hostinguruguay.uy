/**
 * FAQ Custom JavaScript - Hosting Uruguay
 * Mejoras de funcionalidad para el sistema de preguntas frecuentes
 */

(function() {
    'use strict';

    // Esperar a que el DOM esté completamente cargado
    document.addEventListener('DOMContentLoaded', function() {
        
        // Inicializar el FAQ
        initFAQ();
        
        // Agregar smooth scroll al hacer clic en enlaces hacia el FAQ
        initFAQLinks();
        
    });

    /**
     * Inicializar funcionalidad del FAQ
     */
    function initFAQ() {
        const accordionItems = document.querySelectorAll('#faq .accordion-item');
        
        if (!accordionItems.length) return;

        // Agregar contador a cada pregunta
        accordionItems.forEach(function(item, index) {
            const button = item.querySelector('.accordion-button');
            if (button) {
                // Opcional: agregar número a cada pregunta
                // const questionNumber = document.createElement('span');
                // questionNumber.className = 'faq-number me-2';
                // questionNumber.textContent = (index + 1) + '.';
                // button.insertBefore(questionNumber, button.firstChild);
            }
        });

        // Cerrar otras preguntas al abrir una (opcional - comentado por defecto)
        // autoCloseOtherAccordions();
    }

    /**
     * Cerrar automáticamente otros accordions al abrir uno
     * (Opcional - descomentá si querés que solo una pregunta esté abierta a la vez)
     */
    function autoCloseOtherAccordions() {
        const accordionButtons = document.querySelectorAll('#faq .accordion-button');
        
        accordionButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const currentCollapse = this.getAttribute('data-bs-target');
                
                accordionButtons.forEach(function(otherButton) {
                    if (otherButton !== button) {
                        const otherCollapse = otherButton.getAttribute('data-bs-target');
                        const collapseEl = document.querySelector(otherCollapse);
                        
                        if (collapseEl && collapseEl.classList.contains('show')) {
                            otherButton.classList.add('collapsed');
                            otherButton.setAttribute('aria-expanded', 'false');
                        }
                    }
                });
            });
        });
    }

    /**
     * Inicializar enlaces suaves hacia el FAQ
     */
    function initFAQLinks() {
        const faqLinks = document.querySelectorAll('a[href^="#faq"]');
        
        faqLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                
                if (targetId === '#faq') {
                    e.preventDefault();
                    const faqSection = document.querySelector(targetId);
                    
                    if (faqSection) {
                        const offset = 80; // Ajustar según altura del header
                        const elementPosition = faqSection.getBoundingClientRect().top;
                        const offsetPosition = elementPosition + window.pageYOffset - offset;
                        
                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }

    /**
     * Función auxiliar para detectar si hay preguntas sin responder
     * y resaltarlas (opcional - para debugging)
     */
    function validateFAQContent() {
        const accordionBodies = document.querySelectorAll('#faq .accordion-body');
        let emptyCount = 0;
        
        accordionBodies.forEach(function(body) {
            if (!body.textContent.trim()) {
                console.warn('FAQ item sin contenido encontrado:', body);
                emptyCount++;
            }
        });
        
        if (emptyCount > 0) {
            console.warn('Total de FAQs sin contenido:', emptyCount);
        }
    }

    /**
     * Agregar animación suave al abrir/cerrar
     */
    function enhanceAccordionAnimation() {
        const accordionCollapses = document.querySelectorAll('#faq .accordion-collapse');
        
        accordionCollapses.forEach(function(collapse) {
            collapse.addEventListener('show.bs.collapse', function() {
                this.style.opacity = '0';
                setTimeout(() => {
                    this.style.transition = 'opacity 0.3s ease-in-out';
                    this.style.opacity = '1';
                }, 50);
            });
        });
    }

})();
