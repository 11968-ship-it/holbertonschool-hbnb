document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('jwt'); // Assume you have a function to get JWT from cookie
    if (token) {
        document.getElementById('add-review-section').style.display = 'block';
    }
});
