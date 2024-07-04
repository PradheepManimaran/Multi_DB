document.addEventListener('DOMContentLoaded', function () {
    const dbSelectionForm = document.getElementById('db-selection-form');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const configurationButton = document.getElementById('configuration-btn');
    const metaButton = document.getElementById('meta-btn');

    if (dbSelectionForm) {
        dbSelectionForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const dbType = document.getElementById('db-type').value;
            sessionStorage.setItem('dbType', dbType);
            window.location.href = 'login.html';
        });
    }

    if (loginForm) {
        document.getElementById('login-db-type').value = sessionStorage.getItem('dbType');
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const dbType = document.getElementById('login-db-type').value;
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const apiUrl = dbType === 'mysql'
                ? 'http://127.0.0.1:8000/api/users/login/'
                : 'http://127.0.0.1:8080/api/postgresusers/login/';

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const responseData = await response.json();
                const accessToken = responseData.access;
                sessionStorage.setItem('accessToken', accessToken);
                window.location.href = 'users.html';
            } else {
                const errorData = await response.json();
                console.error('Login Error:', errorData);
                alert('Login failed: ' + errorData.detail);
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const dbType = document.getElementById('register-db-type').value;
            const username = document.getElementById('reg-username').value;
            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;

            const apiUrl = dbType === 'mysql'
                ? 'http://127.0.0.1:8000/api/users/register/'
                : 'http://127.0.0.1:8080/api/postgresusers/register/';

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });

            if (response.ok) {
                alert('Registration successful');
                window.location.href = 'login.html';
            } else {
                const errorData = await response.json();
                console.error('Registration Error:', errorData);
                alert('Registration failed: ' + errorData.detail);
            }
        });
    }

    if (configurationButton) {
        configurationButton.addEventListener('click', function () {
            window.location.href = 'register.html';
        });
    }

    if (metaButton) {
        metaButton.addEventListener('click', function () {
            alert('Meta button clicked');
            // Add further actions for the Meta button as needed
        });
    }

    if (window.location.pathname.endsWith('users.html')) {
        const dbType = sessionStorage.getItem('dbType');
        const accessToken = sessionStorage.getItem('accessToken');

        const userDetailsApi = dbType === 'mysql'
            ? 'http://127.0.0.1:8000/api/users/user-details/'
            : 'http://127.0.0.1:8080/api/postgresusers/user-details/';

        fetch(userDetailsApi, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        })
            .then(response => response.json())
            .then(data => {
                populateUserTable(data.users);
            })
            .catch(error => {
                console.error('User Details Fetch Error:', error);
            });
    }

    function populateUserTable(users) {
        const userTable = document.getElementById('user-table');
        const tbody = userTable.querySelector('tbody');
        tbody.innerHTML = '';

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${JSON.stringify({ last_login: user.last_login })}</td>
            `;
            tbody.appendChild(row);
        });

        userTable.classList.remove('hidden');
    }
});
