document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('upload-form');
    const submitBtn = document.getElementById('submit-btn');
    const loader = document.getElementById('loader');
    const reportResult = document.getElementById('reportResult');
    const reportContent = document.getElementById('report-content');
    const manualFileInput = document.getElementById('manualFile');
    const fileNameDisplay = document.getElementById('fileName');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');

    // Display the name of the selected file
    manualFileInput.addEventListener('change', () => {
        if (manualFileInput.files.length > 0) {
            fileNameDisplay.textContent = `Selected: ${manualFileInput.files[0].name}`;
        } else {
            fileNameDisplay.textContent = '';
        }
    });

    // Handle form submission
    uploadForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        // Show loader and hide form/results
        loader.classList.remove('hidden');
        reportResult.classList.add('hidden');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Generating...';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            reportContent.textContent = data.report;
            reportResult.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            reportContent.textContent = `An error occurred: ${error.message}`;
            reportResult.classList.remove('hidden');
        } finally {
            // Hide loader and re-enable button
            loader.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate Report';
        }
    });

    // Handle copy button
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(reportContent.textContent).then(() => {
            copyBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyBtn.textContent = 'Copy Text';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    });

    // Handle download button
    downloadBtn.addEventListener('click', () => {
        const blob = new Blob([reportContent.textContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'lab_report.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});