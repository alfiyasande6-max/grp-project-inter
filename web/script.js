// API Configuration
const API_URL = 'http://localhost:8000';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileSelected = document.getElementById('fileSelected');
const filename = document.getElementById('filename');
const filesize = document.getElementById('filesize');
const changeFileBtn = document.getElementById('changeFile');
const parseBtn = document.getElementById('parseBtn');
const btnText = document.getElementById('btnText');
const loader = document.getElementById('loader');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const downloadJsonBtn = document.getElementById('downloadJson');
const copyDataBtn = document.getElementById('copyData');

// Store uploaded file and parsed data
let uploadedFile = null;
let parsedData = null;

// Event Listeners
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
changeFileBtn.addEventListener('click', resetFileInput);
parseBtn.addEventListener('click', parseResume);
downloadJsonBtn.addEventListener('click', downloadJSON);
copyDataBtn.addEventListener('click', copyData);

// File Selection Handlers
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        validateAndDisplayFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#764ba2';
    uploadArea.style.background = '#f0f2ff';
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = '#f8f9ff';
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = '#f8f9ff';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        validateAndDisplayFile(file);
    }
}

function validateAndDisplayFile(file) {
    // Reset error message
    hideError();
    
    // Validate file type
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
        showError('Invalid file type. Please upload a PDF or DOCX file.');
        return;
    }
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size exceeds 10MB. Please upload a smaller file.');
        return;
    }
    
    // Store file and display details
    uploadedFile = file;
    filename.textContent = file.name;
    filesize.textContent = formatFileSize(file.size);
    
    // Show file selected UI
    uploadArea.style.display = 'none';
    fileSelected.style.display = 'block';
    parseBtn.disabled = false;
    
    // Hide previous results
    resultsSection.style.display = 'none';
}

function resetFileInput() {
    uploadedFile = null;
    fileInput.value = '';
    uploadArea.style.display = 'block';
    fileSelected.style.display = 'none';
    parseBtn.disabled = true;
    resultsSection.style.display = 'none';
    hideError();
}

// Parse Resume
async function parseResume() {
    if (!uploadedFile) {
        showError('Please select a file first.');
        return;
    }
    
    // Show loading state
    btnText.textContent = 'Parsing...';
    loader.style.display = 'inline-block';
    parseBtn.disabled = true;
    hideError();
    
    // Create FormData
    const formData = new FormData();
    formData.append('file', uploadedFile);
    
    try {
        // Send request to API
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to parse resume');
        }
        
        // Store parsed data
        parsedData = data.extracted_data;
        
        // Display results
        displayResults(parsedData);
        
    } catch (error) {
        showError(`Error: ${error.message}. Make sure the backend server is running at ${API_URL}`);
        console.error('Parse error:', error);
    } finally {
        // Reset button state
        btnText.textContent = 'Parse Resume';
        loader.style.display = 'none';
        parseBtn.disabled = false;
    }
}

// Display Results
function displayResults(data) {
    // Personal Information
    document.getElementById('name').textContent = data.name || 'Not detected';
    document.getElementById('email').textContent = data.email || 'Not detected';
    document.getElementById('phone').textContent = data.phone || 'Not detected';
    
    // Skills
    const skillsContainer = document.getElementById('skillsContainer');
    skillsContainer.innerHTML = '';
    
    if (data.skills && data.skills.length > 0) {
        data.skills.forEach(skill => {
            const skillTag = document.createElement('span');
            skillTag.className = 'skill-tag';
            skillTag.textContent = skill;
            skillsContainer.appendChild(skillTag);
        });
    } else {
        skillsContainer.innerHTML = '<p class="no-data">No skills detected</p>';
    }
    
    // Education
    const educationContainer = document.getElementById('educationContainer');
    educationContainer.innerHTML = '';
    
    if (data.education && data.education.length > 0) {
        data.education.forEach(edu => {
            const eduItem = document.createElement('div');
            eduItem.className = 'list-item';
            eduItem.textContent = edu;
            educationContainer.appendChild(eduItem);
        });
    } else {
        educationContainer.innerHTML = '<p class="no-data">No education information found</p>';
    }
    
    // Experience
    const experienceContainer = document.getElementById('experienceContainer');
    experienceContainer.innerHTML = '';
    
    if (data.experience && data.experience.length > 0) {
        data.experience.forEach(exp => {
            const expItem = document.createElement('div');
            expItem.className = 'list-item';
            expItem.textContent = exp;
            experienceContainer.appendChild(expItem);
        });
    } else {
        experienceContainer.innerHTML = '<p class="no-data">No work experience found</p>';
    }
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Download JSON
function downloadJSON() {
    if (!parsedData) {
        showError('No data to download');
        return;
    }
    
    const dataStr = JSON.stringify(parsedData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `resume_data_${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showSuccess('JSON file downloaded successfully!');
}

// Copy Data
function copyData() {
    if (!parsedData) {
        showError('No data to copy');
        return;
    }
    
    const dataStr = JSON.stringify(parsedData, null, 2);
    
    navigator.clipboard.writeText(dataStr).then(() => {
        showSuccess('Data copied to clipboard!');
    }).catch(err => {
        showError('Failed to copy data: ' + err.message);
    });
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function hideError() {
    errorMessage.style.display = 'none';
}

function showSuccess(message) {
    // Create temporary success message
    const successMsg = document.createElement('div');
    successMsg.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4caf50;
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    successMsg.textContent = message;
    document.body.appendChild(successMsg);
    
    setTimeout(() => {
        successMsg.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(successMsg);
        }, 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
