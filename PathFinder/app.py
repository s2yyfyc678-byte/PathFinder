import os
import pandas as pd
from recommendation_engine import CareerRecommendationEngine
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#############################################################
# FLASK CONFIGURATION
#############################################################

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.environ.get("SECRET_KEY", "CHANGE_THIS_TO_A_RANDOM_SECRET_KEY")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_path = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "career_database.db"))
if db_path.startswith("sqlite:///"):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#############################################################
# DATASET LOCATIONS
#############################################################

DATASET_FOLDER = os.path.join(BASE_DIR, "datasets")
os.makedirs(DATASET_FOLDER, exist_ok=True)

CAREER_DATASET = os.path.join(
    DATASET_FOLDER,
    "comprehensive_career_dataset_mongolia_2026.xlsx"
)

UNIVERSITY_DATASET = os.path.join(
    DATASET_FOLDER,
    "university_and_career_300plus.xlsx"
)

UNIVERSITY_DATASET_2 = os.path.join(
    DATASET_FOLDER,
    "university_dataset_extended_100.xlsx"
)

UNIVERSITY_DATASET_3 = os.path.join(
    DATASET_FOLDER,
    "university_detailed_300plus_v2.xlsx"
)

#############################################################
# LOAD EXCEL FILES
#############################################################

career_df = pd.DataFrame()
uni_df = pd.DataFrame()
uni2_df = pd.DataFrame()
uni3_df = pd.DataFrame()

try:

    if os.path.exists(CAREER_DATASET):
        career_df = pd.read_excel(CAREER_DATASET)
        print("Career dataset loaded.")
    else:
        print("Career dataset file not found; continuing with empty data.")

except Exception as e:

    print(f"Career dataset load skipped: {e}")

try:

    if os.path.exists(UNIVERSITY_DATASET):
        uni_df = pd.read_excel(UNIVERSITY_DATASET)
        print("University dataset 1 loaded.")
    else:
        print("University dataset 1 file not found; continuing with empty data.")

except Exception as e:

    print(f"University dataset 1 load skipped: {e}")

try:

    if os.path.exists(UNIVERSITY_DATASET_2):
        uni2_df = pd.read_excel(UNIVERSITY_DATASET_2)
        print("University dataset 2 loaded.")
    else:
        print("University dataset 2 file not found; continuing with empty data.")

except Exception as e:

    print(f"University dataset 2 load skipped: {e}")

try:

    if os.path.exists(UNIVERSITY_DATASET_3):
        uni3_df = pd.read_excel(UNIVERSITY_DATASET_3)
        print("University dataset 3 loaded.")
    else:
        print("University dataset 3 file not found; continuing with empty data.")

except Exception as e:

    print(f"University dataset 3 load skipped: {e}")

#############################################################
# DATABASE MODELS
#############################################################

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(300))

class SavedCareer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    career_name = db.Column(db.String(200))

#############################################################
# CREATE DATABASE
#############################################################

with app.app_context():

    db.create_all()

#############################################################
# HOME
#############################################################

@app.route("/")

def home():

    return render_template("home.html")

#############################################################
# LOGIN
#############################################################

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email).first()

        if user and user.password:
            stored_password = user.password or ""
            password_ok = False
            try:
                password_ok = check_password_hash(stored_password, password)
            except Exception:
                password_ok = False
            if not password_ok and stored_password == password:
                password_ok = True

            if password_ok:
                session["user"] = user.id
                return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Incorrect Email or Password."
        )

    return render_template("login.html")

#############################################################
# REGISTER
#############################################################

@app.route("/register", methods=["GET", "POST"])

def register():

    if request.method == "POST":

        fullname = (request.form.get("fullname") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        raw_password = request.form.get("password") or ""

        if not fullname or not email or not raw_password:
            return render_template(
                "register.html",
                error="Please fill in all fields."
            )

        check = User.query.filter_by(email=email).first()

        if check:
            return render_template(
                "register.html",
                error="Email already exists."
            )

        new_user = User(
            fullname=fullname,
            email=email,
            password=generate_password_hash(raw_password)
        )

        db.session.add(new_user)
        db.session.commit()
        session["user"] = new_user.id

        return redirect("/dashboard")

    return render_template("register.html")

#############################################################
# DASHBOARD
#############################################################

@app.route("/dashboard")

def dashboard():

    if "user" not in session:

        return redirect("/login")

    user = User.query.get(session["user"])

    return render_template(

        "dashboard.html",

        user=user

    )

#############################################################
# QUIZ PAGE
#############################################################

@app.route("/quiz")

def quiz():

    return render_template("quiz.html")


@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    # Accept form-encoded or JSON payloads
    payload = request.get_json(silent=True) or request.form or {}

    interests_raw = payload.get('interests', '')
    skills_raw = payload.get('skills', '')
    personality = payload.get('personality', '')
    values_raw = payload.get('values', '')

    # normalize lists
    if isinstance(interests_raw, str):
        interests = [i.strip() for i in interests_raw.split(',') if i.strip()]
    else:
        interests = [i.strip() for i in interests_raw]

    if isinstance(skills_raw, str):
        skills = [s.strip() for s in skills_raw.split(',') if s.strip()]
    else:
        skills = [s.strip() for s in skills_raw]

    if isinstance(values_raw, str):
        values = [v.strip() for v in values_raw.split(',') if v.strip()]
    else:
        values = [v.strip() for v in values_raw]

    # Try recommendation engine first
    engine = CareerRecommendationEngine()
    try:
        engine.load_data(CAREER_DATASET, UNIVERSITY_DATASET)
    except Exception:
        pass

    recs = engine.recommend(interests, personality or "", skills, values)

    # Fallback sample recommendations when dataset is absent
    if not recs:
        sample = [
            {"career": "Software Engineer", "compatibility": 92.4},
            {"career": "Data Analyst", "compatibility": 88.0},
            {"career": "Teacher", "compatibility": 81.2}
        ]
        recs = sample

    session['last_recommendations'] = recs
    session['last_quiz'] = {
        'interests': interests,
        'skills': skills,
        'personality': personality,
        'values': values
    }

    return redirect(url_for('results'))

#############################################################
# CHATBOT PAGE
#############################################################

@app.route("/chatbot")

def chatbot():

    return render_template("chatbot.html")

#############################################################
# RESULTS PAGE
#############################################################

@app.route("/results")

def results():

    return render_template("results.html")


#############################################################
# CHATBOT API
#############################################################

def detect_language(message, preferred_language=None):
    if preferred_language in {"en", "mn"}:
        return preferred_language

    if not message:
        return "en"

    lowered = message.lower()
    mongolian_markers = ["сайн", "мэнд", "танд", "юу", "ямар", "хэрхэн", "салбар", "сургууль", "мэргэжил", "ажил", "болон", "олон"]
    if any(token in lowered for token in mongolian_markers):
        return "mn"

    return "en"


def build_reply(message, language="en"):
    if not message or not message.strip():
        if language == "mn":
            return "Сайн байна уу! Би таныг мэргэжлийн зам, сургууль, болон суралцах төлөвлөгөөг хамтад нь шийдвэрлэхэд тусална."
        return "Hello! I can help you explore careers, universities, and study plans in a simple and friendly way."

    text = message.strip().lower()

    if any(token in text for token in ["hello", "hi", "сайн", "мэнд", "sain"]):
        if language == "mn":
            return "Сайн байна уу! Би танд мэргэжил сонгох, сургууль хайх, суралцах төлөвлөгөө гаргахад тусална. Та ямар салбар сонирхож байгаагаа хэлж өгнө үү."
        return "Hello! I can help you explore career options, pick a university, or plan your studies. Tell me what you enjoy and I will guide you."

    if any(token in text for token in ["career", "мэргэжил", "job", "салбар", "work"]):
        if language == "mn":
            return "Таны сонирхол, ур чадвар, болон үнэ цэнийн дагуу тохирох мэргэжлийг олоход туслахын тулд та юу хийх дуртай, ямар ажилд сайн байх, юу чухал болохыг хэлж өгнө үү."
        return "I can help you find a career that fits your interests, strengths, and values. Share what you enjoy, what you are good at, and what matters most to you."

    if any(token in text for token in ["university", "surguuli", "сургууль", "college", "school"]):
        if language == "mn":
            return "Сургууль сонгохдоо хөтөлбөр, багш, санхүүгийн дэмжлэг, амжилттай төгсөгчдийн зам, болон ажиллах боломжийг хамтад нь харгалзан үзэх нь чухал."
        return "When choosing a university, it helps to compare programs, teaching quality, cost, graduate outcomes, and career options."

    if any(token in text for token in ["salary", "цалин", "pay", "earn", "income"]):
        if language == "mn":
            return "Цалин нь улс орон, туршлага, боловсрол, салбар, болон ажлын төрөлөөс хамаарна. Хэрэв та сонирхож байгаа мэргэжлийн нэрийг хэлбэл би илүү тодорхой тайлбарлаж өгч чадна."
        return "Salary depends on your country, experience, education level, industry, and job role. If you share a specific career, I can make it more concrete."

    if any(token in text for token in ["study", "learn", "сурах", "суралцах", "exam", "шалгалт"]):
        if language == "mn":
            return "Суралцах төлөвлөгөөгөө тогтоохдоо өдөр тутмын зорилго, давталт, дадлага, амралтын цагийг тэнцвэржүүлж байвал үр дүнтэй."
        return "A good study plan balances daily goals, repetition, practice, and rest so you can improve steadily."

    if any(token in text for token in ["love", "like", "enjoy", "дуртай", "сонирхол"]):
        if language == "mn":
            return "Таны сонирхол таны дараагийн алхамыг ихээр тодорхойлдог. Та ямар зүйлд дуртай, ямар зүйлд санаа тавьдагийг хэлж өгнө үү."
        return "Your interests are a strong clue for your next steps. Tell me what you enjoy and what excites you."

    if any(token in text for token in ["future", "ирээдүй", "next", "step", "ahead"]):
        if language == "mn":
            return "Ирээдүйгээ төлөвлөхөд эхлээд сонирхол, ур чадвар, үнэ цэнийг тодорхойлж, дараа нь туршлага хуримтлуулах алхмуудыг төлөвлөх нь чухал."
        return "Planning your future works best when you identify your interests, strengths, values, and then build small next steps around them."

    if language == "mn":
        return "Би танд мэргэжил, сургууль, суралцах төлөвлөгөөний талаар туслахад бэлэн. Жишээ нь: “Миний сонирхол бол компьютер”, “Сургууль сонгохыг хүсэж байна”, “Цалин ямар байна?”"
    return "I can support questions about careers, education, study planning, and confidence. Try asking things like: 'I enjoy technology', 'I want help choosing a university', or 'What salary can I expect?'."


@app.route("/chat", methods=["POST"])
@app.route("/ask", methods=["POST"])
def ask():

    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    language = detect_language(message, payload.get("language"))
    answer = build_reply(message, language)

    return jsonify({
        "reply": answer,
        "response": answer,
        "language": language
    })

#############################################################
# RECOMMENDATION API
#############################################################

@app.route("/recommend", methods=["POST"])

def recommend():

    data = request.json

    interests = data.get("interests", [])

    personality = data.get("personality", "")

    skills = data.get("skills", [])

    values = data.get("values", [])

    recommendations = []

    if not career_df.empty:

        sample = career_df.head(3)

        for _, row in sample.iterrows():

            recommendations.append({

                "career": str(row.iloc[0]),

                 "compatibility": 95

            })

    return jsonify({

        "recommendations": recommendations

    })

#############################################################
# SAVE CAREER
#############################################################

@app.route("/savecareer", methods=["POST"])

def savecareer():

    if "user" not in session:

        return jsonify({

            "success": False

        })

    career = request.json["career"]

    saved = SavedCareer(

        user_id=session["user"],

        career_name=career

    )

    db.session.add(saved)

    db.session.commit()

    return jsonify({

        "success": True

    })

#############################################################
# LOGOUT
#############################################################

@app.route("/logout")

def logout():

    session.clear()

    return redirect("/")

#############################################################
# RUN
#############################################################

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
