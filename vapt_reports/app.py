from flask import Flask, render_template_string, request, redirect, url_for, session, send_from_directory
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this for security
app.permanent_session_lifetime = timedelta(minutes=30)  # Session timeout

VAPT_DIR = os.path.abspath(os.path.dirname(__file__))

# ========== Interactive Login Page ==========
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login - VAPT Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-card {
            background: white;
            padding: 40px 30px;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            width: 350px;
            animation: slideIn 0.8s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h2 {
            text-align: center;
            margin-bottom: 25px;
            color: #333;
        }

        .input-group {
            position: relative;
            margin-bottom: 20px;
        }

        .input-group input {
            width: 100%;
            padding: 12px 40px 12px 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 1rem;
        }

        .input-group i {
            position: absolute;
            right: 12px;
            top: 12px;
            color: #aaa;
        }

        button {
            width: 100%;
            padding: 12px;
            background-color: #007BFF;
            color: white;
            font-size: 1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }

        .error {
            color: #e74c3c;
            text-align: center;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }

        .footer-note {
            margin-top: 20px;
            font-size: 0.85rem;
            text-align: center;
            color: #555;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="login-card">
        <h2>VAPT Login🔐</h2>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="input-group">
                <input type="text" name="username" placeholder="Username" required>
                <i class="fas fa-user"></i>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="Password" required>
                <i class="fas fa-lock"></i>
            </div>
            <button type="submit">Login</button>
        </form>
        <div class="footer-note">Access restricted to authorized users only.</div>
    </div>
</body>
</html>
'''

# ========== Main Dashboard Page ==========
MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>VAPT Reports</title>
    <style>
        body {
            font-family: "Segoe UI", sans-serif;
            padding: 30px;
            margin: 0;
            background-color: #f2f2f2;
            color: #333;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 30px;
        }

        .container {
            max-width: 1000px;
            margin: auto;
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
            border: 3px solid #cde8ff;
        }

        .logout-btn {
            float: right;
            padding: 10px 20px;
            font-size: 1rem;
            border: none;
            border-radius: 10px;
            background-color: #dc3545;
            color: white;
            cursor: pointer;
            text-decoration: none;
        }

        .logout-btn:hover {
            background-color: #b52a37;
        }

        .device summary {
            font-size: 1.4rem;
            margin: 12px 0;
            cursor: pointer;
        }

        li {
            list-style: none;
            margin: 8px 0;
        }

        .file-line {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #f5faff;
            padding: 12px 18px;
            border-radius: 10px;
            margin: 6px 0;
        }

        .file-line:hover {
            background-color: #e6f0ff;
        }

        a {
            text-decoration: none;
        }

        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 7px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
        }

        button:hover {
            background-color: #3e8e41;
        }

        summary::-webkit-details-marker {
            display: none;
        }

        summary:before {
            content: "▶ ";
            font-size: 1rem;
        }

        details[open] summary:before {
            content: " ";
        }
    </style>
</head>
<body>
    <div class="container">
        <a class="logout-btn" href="{{ url_for('logout') }}">Logout</a>
        <h1>VAPT Reports</h1>
        {% for device in devices %}
        <div class="device">
            <details>
                <summary><strong>{{ device }}</strong></summary>
                <ul>
                    {% for timestamp in devices[device] %}
                    <li>
                        <details>
                            <summary>{{ timestamp }}</summary>
                            <ul>
                                {% for file in devices[device][timestamp] %}
                                <li class="file-line">
                                    <span>{{ file }}</span>
                                    <a href="/download/{{ device }}/{{ timestamp }}/{{ file }}" download>
                                        <button>Download</button>
                                    </a>
                                </li>
                                {% endfor %}
                            </ul>
                        </details>
                    </li>
                    {% endfor %}
                </ul>
            </details>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

# ========== Authentication Route ==========
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Change as needed
        if username == 'admin' and password == 'admin123':
            session.permanent = True
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    return render_template_string(LOGIN_TEMPLATE, error=error)

# ========== Dashboard ==========
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    devices = {}
    for device in sorted(os.listdir(VAPT_DIR)):
        device_path = os.path.join(VAPT_DIR, device)
        if os.path.isdir(device_path):
            timestamps = {}
            for ts in sorted(os.listdir(device_path), reverse=True):
                ts_path = os.path.join(device_path, ts)
                if os.path.isdir(ts_path):
                    timestamps[ts] = sorted(os.listdir(ts_path))
            devices[device] = timestamps
    return render_template_string(MAIN_TEMPLATE, devices=devices)

# ========== File Download ==========
@app.route('/download/<device>/<timestamp>/<filename>')
def download_file(device, timestamp, filename):
    path = os.path.join(VAPT_DIR, device, timestamp)
    return send_from_directory(path, filename, as_attachment=True)

# ========== Logout ==========
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ========== Start Server ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
