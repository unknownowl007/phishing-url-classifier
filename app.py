from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ==========================================
# 1. FRONTEND PAGE ROUTES (HTML Templates)
# ==========================================

@app.route('/')
def home_ui():
    """Renders the main Phishing URL Scanner UI."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Renders the detailed About page."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Renders the Contact Us page."""
    return render_template('contact.html')


# ==========================================
# 2. DYNAMIC & GET LEARNING ROUTES
# ==========================================

@app.route('/home')
def home():
    return 'Welcome to my first Flask app!'


@app.route('/user/<username>')
def show_user_profile(username):
    """Captures dynamic string variables from the URL path."""
    return f"Hello, {username}! Welcome back to your dashboard."


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Captures dynamic integer variables from the URL path."""
    return f"Displaying blog post #{post_id} (type: {type(post_id).__name__})"


@app.route('/search')
def search():
    """Reads URL query parameters: /search?q=flask&page=1"""
    query = request.args.get('q', default='Nothing', type=str)
    page = request.args.get('page', default=1, type=int)

    return jsonify({
        "searchterm": query,
        "page_number": page,
        "result_found": 15
    })


# ==========================================
# 3. BACKEND REST API ENDPOINTS
# ==========================================

@app.route('/api/login', methods=['POST'])
def login():
    """Handles POST login requests with JSON validation."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == 'password123':
        return jsonify({
            "status": "success",
            "message": "Login successful!",
            "user_id": 101
        }), 200
    else:
        return jsonify({
            "status": "failed",
            "error": "Invalid credentials."
        }), 401


@app.route('/api/url-check', methods=['POST'])
def url_check():
    """Processes URL scanning payloads from the JS frontend."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    url = data.get('url', '').strip()

    if not url:
        return jsonify({"error": "Please provide a valid URL string."}), 400

    # Feature extraction logic
    has_https = url.startswith("https://")
    length = len(url)
    suspicious_keywords = ["login", "verify", "bank", "update", "account", "secure", "free"]
    keyword_matches = [word for word in suspicious_keywords if word in url.lower()]

    # Calculate dynamic risk score
    risk_score = 0.15
    if not has_https:
        risk_score += 0.35
    if length > 50:
        risk_score += 0.20
    if keyword_matches:
        risk_score += 0.30

    risk_score = min(risk_score, 0.99)
    is_phishing = risk_score > 0.50

    return jsonify({
        "target_url": url,
        "status": "scanned",
        "is_phishing": is_phishing,
        "risk_score": round(risk_score * 100, 1),
        "verdict": "Suspicious / Phishing" if is_phishing else "Safe / Legitimate",
        "details": {
            "has_https": has_https,
            "url_length": length,
            "detected_keywords": keyword_matches
        }
    }), 200


# ==========================================
# 4. GLOBAL ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def handle_404(error):
    """Catches invalid endpoints or missing resources and returns clean JSON."""
    return jsonify({
        "error": "The requested endpoint or resource was not found on this server.",
        "status": 404
    }), 404


@app.errorhandler(405)
def handle_405(error):
    """Catches wrong HTTP methods (e.g., sending GET to a POST-only route)."""
    return jsonify({
        "error": "The HTTP method used is not allowed on this endpoint.",
        "status": 405
    }), 405


# ==========================================
# 5. SERVER RUNNER
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)