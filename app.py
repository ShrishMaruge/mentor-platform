from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

# ------------------ Data Paths ------------------
DATA_DIR = 'data'
MENTOR_FILE = os.path.join(DATA_DIR, 'mentors.json')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')
SESSION_FILE = os.path.join(DATA_DIR, 'sessions.json')
FAQ_FILE = os.path.join(DATA_DIR, 'faq.json')
EMERGENCY_FILE = os.path.join(DATA_DIR, 'emergency.json')

# ------------------ Utility Functions ------------------
def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def ensure_files():
    """Create default JSON files if not present."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(MENTOR_FILE):
        save_json(MENTOR_FILE, [
            {"name": "Amit Sharma", "location": "Delhi", "skills": ["business", "leadership", "career"], "rating": 4},
            {"name": "Priya Singh", "location": "Mumbai", "skills": ["tech", "coding", "startup"], "rating": 5}
        ])
    if not os.path.exists(PROGRESS_FILE):
        save_json(PROGRESS_FILE, [])
    if not os.path.exists(SESSION_FILE):
        save_json(SESSION_FILE, [])
    if not os.path.exists(FAQ_FILE):
        save_json(FAQ_FILE, [
            {"question": "mentor", "answer": "You can find mentors on the Find Mentor page."},
            {"question": "progress", "answer": "Your progress is available on the Progress page."},
            {"question": "help", "answer": "For emergencies, visit the Emergency page or call the helpline."}
        ])
    if not os.path.exists(EMERGENCY_FILE):
        save_json(EMERGENCY_FILE, [
            {"type": "Helpline", "contact": "1800-123-4567"},
            {"type": "Email Support", "contact": "support@mentorship.org"}
        ])

# ------------------ AI Mentor Matching ------------------
def match_mentors(skills, location, min_rating=0):
    mentors = load_json(MENTOR_FILE, [])
    matches = []

    for mentor in mentors:
        skill_score = len(set(s.lower() for s in skills) & set(ms.lower() for ms in mentor.get("skills", [])))
        location_score = 1 if location.lower() in mentor.get("location", "").lower() else 0
        rating_score = mentor.get("rating", 0) / 5
        score = (skill_score * 2) + location_score + rating_score

        if score > 0 and mentor.get("rating", 0) >= min_rating:
            mentor["match_score"] = round(score, 2)
            matches.append(mentor)

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches

# ------------------ Routes ------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mentor-match', methods=['GET', 'POST'])
def mentor_match():
    if request.method == 'POST':
        req = request.json
        skills = req.get('skills', [])
        location = req.get('location', '')
        rating = int(req.get('rating', 0))
        matches = match_mentors(skills, location, rating)
        return jsonify({"matches": matches})
    return render_template('mentor_match.html')

@app.route('/mentor/<name>')
def mentor_profile(name):
    mentors = load_json(MENTOR_FILE, [])
    mentor = next((m for m in mentors if m['name'].lower().replace(" ", "_") == name.lower()), None)
    if not mentor:
        return "Mentor not found", 404
    return render_template('mentor_profile.html', mentor=mentor)

@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if request.method == 'POST':
        data = request.json
        current_data = load_json(PROGRESS_FILE, [])
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_data.append(data)
        save_json(PROGRESS_FILE, current_data)
        return jsonify({"status": "saved"})
    return render_template('progress.html', data=load_json(PROGRESS_FILE, []))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        data = request.json
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sessions = load_json(SESSION_FILE, [])
        sessions.append(data)
        save_json(SESSION_FILE, sessions)
        return jsonify({"status": "scheduled"})
    return render_template('schedule.html')

@app.route('/scheduled-sessions')
def scheduled_sessions():
    sessions = load_json(SESSION_FILE, [])
    return render_template('scheduled_sessions.html', sessions=sessions)

@app.route('/emergency')
def emergency():
    resources = load_json(EMERGENCY_FILE, [
        {"type": "Helpline", "contact": "1800-123-4567"},
        {"type": "Email Support", "contact": "support@mentorship.org"}
    ])
    return render_template('emergency.html', resources=resources)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()
    faqs = load_json(FAQ_FILE, [])
    
    response = "I'm not sure how to answer that yet."
    for faq in faqs:
        if faq['question'].lower() in user_message:
            response = faq['answer']
            break
    return jsonify({"response": response})

# ------------------ API Endpoints ------------------
@app.route('/api/mentors')
def get_mentors():
    mentors = load_json(MENTOR_FILE, [])
    return jsonify(mentors)

@app.route('/api/sessions')
def get_sessions():
    sessions = load_json(SESSION_FILE, [])
    return jsonify(sessions)

# ------------------ Admin Dashboard ------------------
@app.route('/admin')
def admin_dashboard():
    mentors = load_json(MENTOR_FILE, [])
    sessions = load_json(SESSION_FILE, [])
    progress = load_json(PROGRESS_FILE, [])
    return render_template('admin_dashboard.html', 
                           mentors=mentors, 
                           sessions=sessions,
                           progress=progress)

@app.route('/admin/add-mentor', methods=['POST'])
def add_mentor():
    data = request.json
    mentors = load_json(MENTOR_FILE, [])
    new_mentor = {
        "name": data.get("name"),
        "skills": data.get("skills", []),
        "location": data.get("location"),
        "rating": float(data.get("rating", 0))
    }
    mentors.append(new_mentor)
    save_json(MENTOR_FILE, mentors)
    return jsonify({"status": "success", "message": "Mentor added successfully!"})

@app.route('/admin/delete-mentor/<string:name>', methods=['DELETE'])
def delete_mentor(name):
    mentors = load_json(MENTOR_FILE, [])
    mentors = [m for m in mentors if m["name"].lower() != name.lower()]
    save_json(MENTOR_FILE, mentors)
    return jsonify({"status": "success", "message": f"Mentor {name} deleted!"})

@app.route('/api/delete-session/<int:index>', methods=['DELETE'])
def delete_session(index):
    sessions = load_json(SESSION_FILE, [])
    if 0 <= index < len(sessions):
        deleted = sessions.pop(index)
        save_json(SESSION_FILE, sessions)
        return jsonify({"status": "success", "deleted": deleted})
    return jsonify({"status": "error", "message": "Invalid session index"}), 400

@app.route('/admin/add-mentor-form')
def add_mentor_form():
    return render_template('add_mentor.html')


# ------------------ Main ------------------
if __name__ == '__main__':
    ensure_files()
    app.run(debug=True)
