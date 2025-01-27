document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');

    const jobDescCheckbox = document.getElementById('job-desc-checkbox');
    const jobDescContainer = document.getElementById('job-desc-container');
    const uploadForm = document.getElementById('upload-form');

    if (jobDescCheckbox) {
        jobDescCheckbox.addEventListener('change', function () {
            console.log('Job description checkbox changed');
            if (this.checked) {
                jobDescContainer.classList.remove('d-none');
            } else {
                jobDescContainer.classList.add('d-none');
            }
        });
    } else {
        console.log('Job description checkbox not found');
    }

    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            console.log('Form submitted');

            const formData = new FormData();
            const fileField = document.querySelector('input[type="file"]');
            const jobDescCheckbox = document.getElementById('job-desc-checkbox');
            const jobDescField = document.getElementById('job-desc');

            formData.append('resume', fileField.files[0]);
            if (jobDescCheckbox.checked) {
                formData.append('job_desc', jobDescField.value);
            }

            console.log('Submitting form data...');

            try {
                const response = await fetch('http://127.0.0.1:5000/upload', {  // Ensure this URL matches your Flask app URL
                    method: 'POST',
                    body: formData
                });

                console.info('Response received:', response);

                const result = await response.json();

                console.info('Result:', result);

                if (response.ok) {
                    if (result.ats_score !== undefined) {
                        document.getElementById('score').textContent = result.ats_score.toFixed(2);
                        document.getElementById('ats-score').classList.remove('d-none');
                        document.getElementById('status-message').classList.add('d-none');
                        console.log('ATS Score:', result.ats_score.toFixed(2));  // Log the ATS score to the console
                    } else {
                        document.getElementById('status-message').textContent = 'ATS score not found.';
                        document.getElementById('ats-score').classList.add('d-none');
                    }
                } else {
                    document.getElementById('status-message').textContent = result.error;
                    document.getElementById('ats-score').classList.add('d-none');
                }
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('status-message').textContent = 'An error occurred while processing your request.';
                document.getElementById('ats-score').classList.add('d-none');
            }
        });
    } else {
        console.log('Upload form not found');
    }
});
