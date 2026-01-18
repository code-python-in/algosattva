document.addEventListener('DOMContentLoaded', function() {
    // Initialize all DOM elements first
    const symbolInput = document.getElementById('symbol');
    const symbolField = document.getElementById('symbol-field');
    const exchangeSelect = document.getElementById('exchange');
    const productSelect = document.getElementById('product');
    const actionSelect = document.getElementById('action');
    const quantityInput = document.getElementById('quantity');
    const actionField = document.getElementById('action-field');
    const quantityField = document.getElementById('quantity-field');
    const webhookDisplay = document.getElementById('webhook-display');
    const searchResults = document.getElementById('searchResults');
    const loadingIndicator = document.querySelector('.loading-indicator');
    const tradingviewForm = document.getElementById('tradingview-form');

    // Bracket order fields
    const bracketActionSelect = document.getElementById('bracket-action');
    const bracketQuantityInput = document.getElementById('bracket-quantity');
    const bracketActionField = document.getElementById('bracket-action-field');
    const bracketQuantityField = document.getElementById('bracket-quantity-field');
    const entryPriceInput = document.getElementById('entry-price');
    const entryPriceField = document.getElementById('entry-price-field');
    const slPriceInput = document.getElementById('sl-price');
    const slPriceField = document.getElementById('sl-price-field');
    const targetPriceInput = document.getElementById('target-price');
    const targetPriceField = document.getElementById('target-price-field');

    let debounceTimeout;
    let currentMode = 'strategy'; // Default mode

    // Host URL from template (set in tradingview.html before this script loads)
    const hostURL = window.OPENALGO_HOST || window.location.origin;

    // Set default values and generate JSON
    if (symbolInput && exchangeSelect && productSelect) {
        symbolInput.value = 'SAIL';
        exchangeSelect.value = 'NSE';
        productSelect.value = 'CNC';

        // Set bracket order defaults to 1
        if (entryPriceInput) entryPriceInput.value = '2';
        if (slPriceInput) slPriceInput.value = '1';
        if (targetPriceInput) targetPriceInput.value = '3';
        if (bracketQuantityInput) bracketQuantityInput.value = '1';

        // Auto-generate JSON on load
        generateJSON();
    }

    // Symbol input handler
    if (symbolInput) {
        symbolInput.addEventListener('input', function(e) {
            clearTimeout(debounceTimeout);
            const query = e.target.value.trim();
            const exchange = exchangeSelect ? exchangeSelect.value : '';

            if (query.length < 2) {
                if (searchResults) {
                    searchResults.classList.add('hidden');
                }
                return;
            }

            debounceTimeout = setTimeout(() => {
                fetchSearchResults(query, exchange);
            }, 300);
        });
    }

    // Exchange select handler
    if (exchangeSelect) {
        exchangeSelect.addEventListener('change', function(e) {
            const query = symbolInput ? symbolInput.value.trim() : '';
            if (query.length >= 2) {
                fetchSearchResults(query, e.target.value);
            }
            generateJSON();
        });
    }

    // Product type change handler
    if (productSelect) {
        productSelect.addEventListener('change', generateJSON);
    }

    // Action change handler (Line Mode)
    if (actionSelect) {
        actionSelect.addEventListener('change', generateJSON);
    }

    // Quantity change handler (Line Mode)
    if (quantityInput) {
        quantityInput.addEventListener('input', generateJSON);
    }

    // Bracket order change handlers
    if (bracketActionSelect) {
        bracketActionSelect.addEventListener('change', generateJSON);
    }
    if (bracketQuantityInput) {
        bracketQuantityInput.addEventListener('input', generateJSON);
    }
    if (entryPriceInput) {
        entryPriceInput.addEventListener('input', generateJSON);
    }
    if (slPriceInput) {
        slPriceInput.addEventListener('input', generateJSON);
    }
    if (targetPriceInput) {
        targetPriceInput.addEventListener('input', generateJSON);
    }

    // Click outside search results handler
    document.addEventListener('click', function(e) {
        if (searchResults && symbolInput && 
            !symbolInput.contains(e.target) && 
            !searchResults.contains(e.target)) {
            searchResults.classList.add('hidden');
        }
    });

    // Form submit handler
    if (tradingviewForm) {
        tradingviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            generateJSON();
        });
    }

    async function fetchSearchResults(query, exchange) {
        if (!searchResults || !loadingIndicator) return;

        try {
            loadingIndicator.style.display = 'block';
            const response = await fetch(`/search/api/search?q=${encodeURIComponent(query)}&exchange=${encodeURIComponent(exchange)}`);
            const data = await response.json();

            searchResults.innerHTML = '';

            if (data.results && data.results.length > 0) {
                data.results.forEach(result => {
                    const div = document.createElement('div');
                    div.className = 'menu-item p-3 hover:bg-base-200';
                    div.innerHTML = `
                        <div class="flex items-center justify-between">
                            <span class="font-medium">${result.symbol}</span>
                            <span class="badge badge-${result.exchange.toLowerCase()}">${result.exchange}</span>
                        </div>
                        <div class="text-sm text-base-content/70 mt-1">${result.name || ''}</div>
                        <div class="text-xs text-base-content/60 mt-1">Token: ${result.token}</div>
                    `;
                    div.addEventListener('click', () => {
                        if (symbolInput && exchangeSelect) {
                            symbolInput.value = result.symbol;
                            exchangeSelect.value = result.exchange;
                            searchResults.classList.add('hidden');
                            generateJSON();
                        }
                    });
                    searchResults.appendChild(div);
                });
                searchResults.classList.remove('hidden');
            } else {
                searchResults.classList.add('hidden');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Error fetching search results');
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }

    // Click outside search results handler
    document.addEventListener('click', function(e) {
        if (searchResults && symbolInput &&
            !symbolInput.contains(e.target) &&
            !searchResults.contains(e.target)) {
            searchResults.classList.add('hidden');
        }
    });

    // Form submit handler
    if (tradingviewForm) {
        tradingviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            generateJSON();
        });
    }

    function generateJSON() {
        if (!exchangeSelect || !productSelect) return;

        // Use actual symbol for strategy/line, {{ticker}} for bracket
        let symbolValue = '{{ticker}}';
        if (currentMode !== 'bracket' && symbolInput) {
            symbolValue = symbolInput.value;
        }

        const formData = {
            symbol: symbolValue,
            exchange: exchangeSelect.value,
            product: productSelect.value,
            mode: currentMode
        };

        // Add action and quantity for Line mode
        if (currentMode === 'line') {
            if (!actionSelect || !quantityInput) return;
            formData.action = actionSelect.value;
            formData.quantity = quantityInput.value;
        }

        // Add bracket order specific fields
        if (currentMode === 'bracket') {
            if (!bracketActionSelect || !bracketQuantityInput || !entryPriceInput || !slPriceInput || !targetPriceInput) return;

            const action = bracketActionSelect.value;
            const entryPrice = parseFloat(entryPriceInput.value) || 0;
            const slPrice = parseFloat(slPriceInput.value) || 0;
            const targetPrice = parseFloat(targetPriceInput.value) || 0;

            // Validate prices based on action
            if (action === 'BUY') {
                if (slPrice >= entryPrice) {
                    showToast('For BUY orders: Stoploss price must be less than entry price', 'error');
                    return;
                }
                if (targetPrice <= entryPrice) {
                    showToast('For BUY orders: Target price must be greater than entry price', 'error');
                    return;
                }
            } else if (action === 'SELL') {
                if (slPrice <= entryPrice) {
                    showToast('For SELL orders: Stoploss price must be greater than entry price', 'error');
                    return;
                }
                if (targetPrice >= entryPrice) {
                    showToast('For SELL orders: Target price must be less than entry price', 'error');
                    return;
                }
            }

            formData.action = action;
            formData.quantity = bracketQuantityInput.value;
            formData.entry_price = entryPrice;
            formData.sl_price = slPrice;
            formData.target_price = targetPrice;
        }

        fetch('/tradingview/', {
            method: 'POST',
            body: JSON.stringify(formData),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json().then(data => ({status: response.status, data: data})))
        .then(({status, data}) => {
            if (status === 404 && data.error === 'API key not found') {
                showToast('Please set up your API key in the API Key section first', 'warning', true);
                return;
            }
            if (status !== 200) {
                throw new Error(data.error || 'Network response was not ok');
            }

            // Reconstruct the JSON object in the correct order
            let orderedData;
            if (currentMode === 'line') {
                orderedData = {
                    "apikey": data.apikey,
                    "strategy": data.strategy,
                    "symbol": symbolInput.value,
                    "action": data.action,
                    "exchange": exchangeSelect.value,
                    "pricetype": data.pricetype,
                    "product": productSelect.value,
                    "quantity": data.quantity
                };
            } else if (currentMode === 'bracket') {
                orderedData = {
                    "apikey": data.apikey,
                    "strategy": data.strategy,
                    "symbol": "{{ticker}}",
                    "exchange": exchangeSelect.value,
                    "product": productSelect.value,
                    "action": data.action,
                    "quantity": data.quantity,
                    "entry_price": data.entry_price,
                    "sl_price": data.sl_price,
                    "target_price": data.target_price
                };
            } else {
                orderedData = {
                    "apikey": data.apikey,
                    "strategy": data.strategy,
                    "symbol": symbolInput.value,
                    "action": data.action,
                    "exchange": exchangeSelect.value,
                    "pricetype": data.pricetype,
                    "product": productSelect.value,
                    "quantity": data.quantity,
                    "position_size": data.position_size
                };
            }

            const jsonOutput = document.getElementById('json-output');
            if (jsonOutput) {
                const formattedJson = JSON.stringify(orderedData, null, 2);
                jsonOutput.textContent = formattedJson;
                Prism.highlightElement(jsonOutput);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error generating JSON');
        });
    }

    // Copy webhook URL handler
    const webhookCopyBtn = document.getElementById('copy-webhook');
    if (webhookCopyBtn) {
        webhookCopyBtn.addEventListener('click', function() {
            const webhookURL = document.getElementById('webhookURL');
            const alert = document.getElementById('webhookCopyAlert');
            if (webhookURL && alert) {
                copyText(webhookURL.textContent.trim(), this, alert);
            }
        });
    }

    // Copy JSON handler
    const copyJsonBtn = document.getElementById('copy-json');
    if (copyJsonBtn) {
        copyJsonBtn.addEventListener('click', function() {
            const jsonOutput = document.getElementById('json-output');
            const alert = document.getElementById('copy-success-alert');
            if (jsonOutput && alert) {
                copyText(jsonOutput.textContent, this, alert);
            }
        });
    }

    function copyText(text, button, alert) {
        const originalText = button.innerHTML;
        
        navigator.clipboard.writeText(text).then(() => {
            alert.classList.remove('hidden');
            button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Copied!
            `;
            
            setTimeout(() => {
                alert.classList.add('hidden');
                button.innerHTML = originalText;
            }, 2000);
        }).catch(() => {
            showToast('Failed to copy text');
        });
    }

    function showToast(message, type = 'error', withLink = false) {
        const toast = document.createElement('div');
        toast.className = 'toast toast-end';

        let alertClass = type === 'warning' ? 'alert-warning' : 'alert-error';
        let content = message;

        if (withLink) {
            content = `
                ${message}
                <a href="/apikey" class="btn btn-sm btn-primary ml-2">Go to API Key Setup</a>
            `;
        }

        toast.innerHTML = `
            <div class="alert ${alertClass} flex items-center">
                <span>${content}</span>
            </div>
        `;

        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 5000);
    }

    // Mode switching function (globally accessible for onclick)
    window.switchMode = function(mode) {
        currentMode = mode;

        // Update tab states
        const strategyTab = document.getElementById('strategy-tab');
        const lineTab = document.getElementById('line-tab');
        const bracketTab = document.getElementById('bracket-tab');

        // Remove active class from all tabs
        if (strategyTab) strategyTab.classList.remove('tab-active');
        if (lineTab) lineTab.classList.remove('tab-active');
        if (bracketTab) bracketTab.classList.remove('tab-active');

        // Hide all mode-specific fields
        if (actionField) actionField.classList.add('hidden');
        if (quantityField) quantityField.classList.add('hidden');
        if (bracketActionField) bracketActionField.classList.add('hidden');
        if (bracketQuantityField) bracketQuantityField.classList.add('hidden');
        if (entryPriceField) entryPriceField.classList.add('hidden');
        if (slPriceField) slPriceField.classList.add('hidden');
        if (targetPriceField) targetPriceField.classList.add('hidden');

        if (mode === 'strategy') {
            if (strategyTab) strategyTab.classList.add('tab-active');

            // Show symbol field for strategy mode
            if (symbolField) symbolField.classList.remove('hidden');

            // Update webhook URL
            if (webhookDisplay) {
                webhookDisplay.textContent = '.../api/v1/placesmartorder';
                webhookDisplay.setAttribute('data-tip', `${hostURL}/api/v1/placesmartorder`);
            }
        } else if (mode === 'line') {
            if (lineTab) lineTab.classList.add('tab-active');

            // Show symbol and line mode fields
            if (symbolField) symbolField.classList.remove('hidden');
            if (actionField) actionField.classList.remove('hidden');
            if (quantityField) quantityField.classList.remove('hidden');

            // Set default values for line mode
            if (actionSelect) actionSelect.value = 'BUY';
            if (quantityInput) quantityInput.value = '1';

            // Update webhook URL
            if (webhookDisplay) {
                webhookDisplay.textContent = '.../api/v1/placeorder';
                webhookDisplay.setAttribute('data-tip', `${hostURL}/api/v1/placeorder`);
            }
        } else if (mode === 'bracket') {
            if (bracketTab) bracketTab.classList.add('tab-active');

            // Hide symbol field for bracket mode (uses {{ticker}})
            if (symbolField) symbolField.classList.add('hidden');

            // Show bracket mode fields
            if (bracketActionField) bracketActionField.classList.remove('hidden');
            if (bracketQuantityField) bracketQuantityField.classList.remove('hidden');
            if (entryPriceField) entryPriceField.classList.remove('hidden');
            if (slPriceField) slPriceField.classList.remove('hidden');
            if (targetPriceField) targetPriceField.classList.remove('hidden');

            // Set default values for bracket mode
            if (bracketActionSelect) bracketActionSelect.value = 'BUY';
            if (bracketQuantityInput) bracketQuantityInput.value = '1';
            if (entryPriceInput) entryPriceInput.value = '2';
            if (slPriceInput) slPriceInput.value = '1';
            if (targetPriceInput) targetPriceInput.value = '3';

            // Update webhook URL
            if (webhookDisplay) {
                webhookDisplay.textContent = '.../tradingview/webhook/bracket';
                webhookDisplay.setAttribute('data-tip', `${hostURL}/tradingview/webhook/bracket`);
            }
        }

        // Regenerate JSON
        generateJSON();
    };
});
