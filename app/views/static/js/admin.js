// Function to handle form submissions with file uploads
async function submitFormWithFiles(url, formData, method = 'POST') {
    try {
        const response = await fetch(url, {
            method: method,
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Function to preview image uploads
function previewImage(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            previewElement.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}

// Function to show confirmation dialog
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Function to format dates for input fields
function formatDateForInput(dateString) {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
}

// Function to handle API errors
function handleApiError(error) {
    console.error('API Error:', error);
    alert('An error occurred: ' + error.message);
}

// Add loading state handler
function setLoading(buttonElement, isLoading) {
    if (isLoading) {
        buttonElement.disabled = true;
        buttonElement.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Loading...';
    } else {
        buttonElement.disabled = false;
        buttonElement.innerHTML = buttonElement.getAttribute('data-original-text');
    }
}

// Add toast notifications
function showToast(message, type = 'success') {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    const toastContainer = document.getElementById('toast-container');
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toast = new bootstrap.Toast(toastContainer.lastElementChild);
    toast.show();
}

function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}
