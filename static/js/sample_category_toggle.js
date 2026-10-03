document.addEventListener('DOMContentLoaded', function() {
    const categoryField = document.querySelector('#id_category');
    if (!categoryField) return;

    function updateClientLabel() {
        const clientLabel = document.querySelector('label[for="id_client"]');
        if (!clientLabel) return;
        
        if (categoryField.value === 'Raw Material') {
            if (clientLabel.innerHTML.includes('Client')) {
                clientLabel.innerHTML = clientLabel.innerHTML.replace('Client', 'Vendor');
            }
        } else {
            if (clientLabel.innerHTML.includes('Vendor')) {
                clientLabel.innerHTML = clientLabel.innerHTML.replace('Vendor', 'Client');
            }
        }
    }

    categoryField.addEventListener('change', updateClientLabel);
    updateClientLabel();
});
