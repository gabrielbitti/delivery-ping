// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    
    // Show toast
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Format date to Brazilian format
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format phone number
function formatPhone(phone) {
    if (!phone) return '-';
    return phone.replace(/^(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
}

// Format CPF
function formatCPF(cpf) {
    if (!cpf) return '-';
    return cpf.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

// Format CNPJ
function formatCNPJ(cnpj) {
    if (!cnpj) return '-';
    return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
}

// Confirm dialog
function confirmAction(message) {
    return confirm(message);
}

// API helper functions
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        return {
            ok: response.ok,
            status: response.status,
            data: await response.json()
        };
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Export functions for use in other scripts
window.showToast = showToast;
window.formatDate = formatDate;
window.formatPhone = formatPhone;
window.formatCPF = formatCPF;
window.formatCNPJ = formatCNPJ;
window.confirmAction = confirmAction;
window.apiRequest = apiRequest;
