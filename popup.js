// Configuration par défaut
const DEFAULT_CONFIG = {
    apiUrl: 'http://localhost:5000',
    grocyUrl: 'http://100.83.155.21:9283',
    grocyApiKey: ''
};

// Éléments DOM
const importBtn = document.getElementById('importBtn');
const previewBtn = document.getElementById('previewBtn');
const statusDiv = document.getElementById('status');
const recipePreviewDiv = document.getElementById('recipePreview');
const settingsLink = document.getElementById('settingsLink');
const configSection = document.getElementById('configSection');
const saveConfigBtn = document.getElementById('saveConfig');

// Inputs de configuration
const apiUrlInput = document.getElementById('apiUrl');
const grocyUrlInput = document.getElementById('grocyUrl');
const grocyApiKeyInput = document.getElementById('grocyApiKey');

let currentUrl = '';
let config = {};

// Charger la configuration au démarrage
chrome.storage.sync.get(DEFAULT_CONFIG, (items) => {
    config = items;
    apiUrlInput.value = config.apiUrl;
    grocyUrlInput.value = config.grocyUrl;
    grocyApiKeyInput.value = config.grocyApiKey;
});

// Récupérer l'URL de la page courante
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
        currentUrl = tabs[0].url;
    }
});

// Afficher/masquer la section configuration
settingsLink.addEventListener('click', (e) => {
    e.preventDefault();
    configSection.classList.toggle('show');
});

// Sauvegarder la configuration
saveConfigBtn.addEventListener('click', () => {
    const newConfig = {
        apiUrl: apiUrlInput.value.trim(),
        grocyUrl: grocyUrlInput.value.trim(),
        grocyApiKey: grocyApiKeyInput.value.trim()
    };
    
    chrome.storage.sync.set(newConfig, () => {
        config = newConfig;
        showStatus('✓ Configuration sauvegardée', 'success');
        setTimeout(() => {
            configSection.classList.remove('show');
        }, 1500);
    });
});

// Prévisualiser la recette
previewBtn.addEventListener('click', async () => {
    if (!currentUrl) {
        showStatus('✗ Impossible de récupérer l\'URL de la page', 'error');
        return;
    }
    
    if (!config.apiUrl) {
        showStatus('⚠️ Veuillez configurer l\'URL de l\'API', 'error');
        return;
    }
    
    showStatus('🔍 Extraction de la recette...', 'loading');
    setButtonsEnabled(false);
    
    try {
        const response = await fetch(`${config.apiUrl}/api/preview`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: currentUrl })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus('✓ Recette extraite', 'success');
            showPreview(data.data);
        } else {
            showStatus(`✗ Erreur: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`✗ Erreur de connexion: ${error.message}`, 'error');
    } finally {
        setButtonsEnabled(true);
    }
});

// Importer la recette
importBtn.addEventListener('click', async () => {
    if (!currentUrl) {
        showStatus('✗ Impossible de récupérer l\'URL de la page', 'error');
        return;
    }
    
    if (!config.apiUrl || !config.grocyApiKey) {
        showStatus('⚠️ Veuillez configurer l\'API et la clé Grocy', 'error');
        configSection.classList.add('show');
        return;
    }
    
    showStatus('📤 Import en cours...', 'loading');
    setButtonsEnabled(false);
    
    try {
        const response = await fetch(`${config.apiUrl}/api/import`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: currentUrl,
                grocy_url: config.grocyUrl,
                grocy_api_key: config.grocyApiKey
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(`✅ ${data.message}`, 'success');
            
            // Afficher un lien vers la recette dans Grocy
            if (data.data && data.data.grocy_url) {
                const link = document.createElement('a');
                link.href = data.data.grocy_url;
                link.target = '_blank';
                link.textContent = '🔗 Voir dans Grocy';
                link.style.display = 'block';
                link.style.marginTop = '10px';
                link.style.color = '#667eea';
                link.style.textAlign = 'center';
                statusDiv.appendChild(link);
            }
            
            // Fermer la popup après 3 secondes
            setTimeout(() => {
                window.close();
            }, 3000);
        } else {
            showStatus(`✗ Erreur: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`✗ Erreur de connexion: ${error.message}`, 'error');
        console.error('Erreur:', error);
    } finally {
        setButtonsEnabled(true);
    }
});

// Fonctions utilitaires
function showStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.style.display = 'block';
}

function showPreview(recipe) {
    const html = `
        <h3>${recipe.title}</h3>
        <p><strong>Portions:</strong> ${recipe.yields}</p>
        ${recipe.total_time ? `<p><strong>Temps:</strong> ${recipe.total_time} min</p>` : ''}
        <p><strong>Ingrédients:</strong> ${recipe.ingredients_count}</p>
        <p style="font-size: 11px; color: #999; margin-top: 8px;">
            ${recipe.ingredients.slice(0, 3).join(', ')}...
        </p>
    `;
    recipePreviewDiv.innerHTML = html;
    recipePreviewDiv.style.display = 'block';
}

function setButtonsEnabled(enabled) {
    importBtn.disabled = !enabled;
    previewBtn.disabled = !enabled;
    
    if (!enabled) {
        importBtn.innerHTML = '<span class="spinner"></span> Import...';
    } else {
        importBtn.textContent = 'Importer cette recette';
    }
}
