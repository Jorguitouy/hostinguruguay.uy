/**
 * Modal Comparador Mobile - Hosting Uruguay
 * Script para generar versión móvil optimizada del comparador
 */

(function() {
    'use strict';

    // Esperar a que el DOM esté completamente cargado
    document.addEventListener('DOMContentLoaded', function() {
        initMobileComparison();
    });

    /**
     * Inicializar comparación móvil
     */
    function initMobileComparison() {
        const modal = document.getElementById('comparadorModal');
        if (!modal) return;

        // Crear versión móvil al abrir el modal
        modal.addEventListener('show.bs.modal', function() {
            if (window.innerWidth < 768) {
                createMobileVersion();
            }
        });

        // Actualizar al redimensionar
        window.addEventListener('resize', debounce(function() {
            if (modal.classList.contains('show')) {
                if (window.innerWidth < 768) {
                    createMobileVersion();
                }
            }
        }, 250));
    }

    /**
     * Crear versión móvil del comparador
     */
    function createMobileVersion() {
        const modalBody = document.querySelector('#comparadorModal .modal-body');
        if (!modalBody) return;

        // Verificar si ya existe la versión móvil
        let mobileContainer = modalBody.querySelector('.mobile-comparison');
        if (mobileContainer) return;

        // Extraer datos de la tabla
        const plans = extractPlansData();
        if (!plans || plans.length === 0) return;

        // Crear contenedor móvil
        mobileContainer = document.createElement('div');
        mobileContainer.className = 'mobile-comparison';

        // Crear tabs
        const tabsHtml = createTabs(plans);
        mobileContainer.innerHTML = tabsHtml;

        // Insertar en el modal body
        modalBody.appendChild(mobileContainer);

        // Inicializar funcionalidad de tabs
        initTabs();
    }

    /**
     * Extraer datos de los planes desde la tabla
     */
    function extractPlansData() {
        const table = document.querySelector('#comparadorModal table');
        if (!table) return null;

        const plans = [
            { name: 'Básico', price: '$5.99', features: [] },
            { name: 'Inicio', price: '$8.99', features: [] },
            { name: 'Profesional', price: '$12.99', features: [] }
        ];

        // Extraer características de la tabla
        const rows = table.querySelectorAll('tbody tr');
        let currentSection = '';

        rows.forEach(row => {
            // Verificar si es una sección
            if (row.querySelector('.compare-header')) {
                currentSection = row.querySelector('.compare-header').textContent.trim();
                return;
            }

            const cells = row.querySelectorAll('td');
            if (cells.length >= 4) {
                const featureName = cells[0].textContent.trim();
                
                plans.forEach((plan, index) => {
                    const value = cells[index + 1].innerHTML.trim();
                    plan.features.push({
                        section: currentSection,
                        name: featureName,
                        value: value
                    });
                });
            }
        });

        return plans;
    }

    /**
     * Crear HTML de tabs
     */
    function createTabs(plans) {
        let html = '<ul class="nav nav-tabs" role="tablist">';
        
        plans.forEach((plan, index) => {
            const active = index === 0 ? 'active' : '';
            html += `
                <li class="nav-item" role="presentation">
                    <button class="nav-link ${active}" 
                            data-bs-toggle="tab" 
                            data-bs-target="#plan${index}" 
                            type="button" 
                            role="tab">
                        ${plan.name}
                    </button>
                </li>
            `;
        });
        
        html += '</ul>';
        html += '<div class="tab-content">';
        
        plans.forEach((plan, index) => {
            const active = index === 0 ? 'show active' : '';
            const headerClass = `plan-${plan.name.toLowerCase()}`;
            
            html += `
                <div class="tab-pane fade ${active}" 
                     id="plan${index}" 
                     role="tabpanel">
                    <div class="plan-content">
                        <div class="plan-header ${headerClass}">
                            <div class="plan-name">${plan.name}</div>
                            <div class="plan-price">
                                <span class="currency">$</span>${plan.price.replace('$', '')}<span class="period">/mes</span>
                            </div>
                            <a href="https://panel.hostinguruguay.uy" 
                               target="_blank" 
                               rel="noopener" 
                               class="btn btn-light btn-sm mt-2">
                                Comprar ahora
                            </a>
                        </div>
                        ${createFeaturesList(plan.features)}
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        
        return html;
    }

    /**
     * Crear lista de características
     */
    function createFeaturesList(features) {
        let html = '';
        let currentSection = '';

        features.forEach(feature => {
            // Nueva sección
            if (feature.section && feature.section !== currentSection) {
                if (currentSection) {
                    html += '</ul>';
                }
                currentSection = feature.section;
                html += `<div class="feature-section">
                            <div class="feature-section-title">${currentSection}</div>
                            <ul class="feature-list">`;
            }

            // Item de característica
            html += `
                <li class="feature-item">
                    <span class="feature-name">${feature.name}</span>
                    <span class="feature-value">${feature.value}</span>
                </li>
            `;
        });

        if (currentSection) {
            html += '</ul></div>';
        }

        return html;
    }

    /**
     * Inicializar funcionalidad de tabs
     */
    function initTabs() {
        const tabButtons = document.querySelectorAll('#comparadorModal .nav-tabs button');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Bootstrap ya maneja el cambio de tab
                // Aquí podríamos agregar analytics si fuera necesario
            });
        });
    }

    /**
     * Debounce helper
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

})();
