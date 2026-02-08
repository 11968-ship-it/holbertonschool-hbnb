/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
  });
document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('jwt'); // Assume you have a function to get JWT from cookie
    if (token) {
        document.getElementById('add-review-section').style.display = 'block';
    }
});
