# Mentor Platform - Flask Application

An **AI-powered voice-first mentorship platform** designed for rural youth using low-end devices.  
This platform provides mentor matching, session scheduling, progress tracking, and multi-language support with a user-friendly interface.

---

## **Features**
- **AI Mentor Matching**: Match mentors based on skills, location, and ratings.
- **Session Scheduling**: Book mentorship sessions with date, time, and notes.
- **Progress Tracking**: Save and view mentorship progress entries.
- **Admin Dashboard**: Manage mentors, view sessions, and analytics.
- **Emergency Help**: Quick access to helplines and support.
- **Real-Time Chatbot**: FAQ-based chatbot for common queries.
- **Responsive UI**: Optimized for mobile and desktop devices.

---

## **Tech Stack**
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap, JavaScript
- **Database**: JSON-based storage
- **Charts & Analytics**: Chart.js
- **Deployment Ready**: Works with GitHub and cloud services (Heroku, Render, etc.)

---

## **Project Structure**

mentor-platform/
│
├── app.py # Flask app entry point
├── templates/ # HTML templates (Jinja2)
│ ├── base.html
│ ├── index.html
│ ├── schedule.html
│ ├── mentor_match.html
│ ├── admin_dashboard.html
│ └── ...
├── static/ # Static files (CSS, JS, Images)
│ ├── css/
│ ├── js/
│ └── img/
├── data/ # JSON files (mentors, sessions, etc.)
│ ├── mentors.json
│ ├── sessions.json
│ └── progress.json
└── README.md
