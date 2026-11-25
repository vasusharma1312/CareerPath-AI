
import streamlit as st
import pandas as pd
import joblib
import os
import html
from datetime import datetime

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CareerPath AI | Career Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. SESSION STATE
# =====================================================

defaults = {
    "page": "Home",
    "light_mode": False,
    "results": None,
    "history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# 3. THEME
# =====================================================

light = st.session_state.light_mode

if light:
    BG = "#f5f4fc"
    PANEL = "#ffffff"
    TEXT = "#19192b"
    MUTED = "#74748b"
    BORDER = "#e5e2f0"
else:
    BG = "#10111c"
    PANEL = "#191b2a"
    TEXT = "#f5f5ff"
    MUTED = "#a3a5ba"
    BORDER = "#303247"

# =====================================================
# 4. CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {{
    background:
        radial-gradient(ellipse at 5% 5%, rgba(117,78,225,.17), transparent 40%),
        radial-gradient(ellipse at 95% 20%, rgba(0,190,160,.10), transparent 38%),
        {BG};
    font-family: 'Inter', sans-serif;
    color: {TEXT};
}}

.block-container {{
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

h1, h2, h3, h4 {{
    color: {TEXT} !important;
    font-family: 'Inter', sans-serif !important;
}}

p, label {{
    color: {MUTED};
}}

.nav-brand {{
    font-size: 22px;
    font-weight: 800;
    padding: 9px 0;
    color: {TEXT};
}}

.nav-brand span {{
    color: #a78bfa;
}}

.hero {{
    background:
        radial-gradient(circle at 0% 0%, rgba(135,85,235,.23), transparent 50%),
        radial-gradient(circle at 100% 20%, rgba(0,190,160,.12), transparent 42%),
        {PANEL};
    border: 1px solid rgba(155,125,255,.24);
    border-radius: 25px;
    padding: 58px 48px;
    margin: 24px 0 35px;
    min-height: 365px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.eyebrow {{
    color: #a78bfa;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 24px;
}}

.hero-title {{
    color: {TEXT};
    font-size: clamp(37px, 5vw, 58px);
    font-weight: 800;
    letter-spacing: -2.5px;
    line-height: 1.15;
}}

.gradient-text {{
    background: linear-gradient(100deg,#d58cdb,#a080ff,#718dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-description {{
    color: {MUTED};
    font-size: 15px;
    line-height: 1.9;
    max-width: 680px;
    margin-top: 20px;
}}

.section-title {{
    font-size: 23px;
    font-weight: 750;
    color: {TEXT};
    margin-top: 35px;
    margin-bottom: 8px;
}}

.section-subtitle {{
    color: {MUTED};
    font-size: 13px;
    margin-bottom: 22px;
}}

.info-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 17px;
    padding: 23px;
    min-height: 155px;
    margin-bottom: 15px;
}}

.info-card h3 {{
    font-size: 16px;
    margin: 12px 0 8px;
}}

.info-card p {{
    font-size: 13px;
    line-height: 1.7;
}}

.career-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 17px;
    padding: 20px;
    min-height: 205px;
    margin-bottom: 12px;
}}

.career-name {{
    color: {TEXT};
    font-weight: 750;
    font-size: 15px;
    min-height: 45px;
}}

.percentage {{
    float: right;
    border: 1px solid;
    border-radius: 20px;
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 800;
}}

.progress-bg {{
    background: {BORDER};
    height: 6px;
    border-radius: 20px;
    overflow: hidden;
    margin: 15px 0;
}}

.progress-fill {{
    height: 100%;
    border-radius: 20px;
}}

.card-detail {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: {MUTED};
    margin-top: 12px;
}}

.rank {{
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: 17px;
}}

.stButton > button {{
    border: 1px solid {BORDER};
    background: {PANEL};
    color: {TEXT};
    border-radius: 11px;
    min-height: 43px;
    font-weight: 650;
    transition: .2s;
}}

.stButton > button:hover {{
    border-color: #9b7bff;
    color: #a78bfa;
}}

.stButton > button[kind="primary"],
.stFormSubmitButton > button {{
    background: linear-gradient(110deg,#8058e8,#6254d9);
    color: white !important;
    border: none;
}}

.stFormSubmitButton > button {{
    min-height: 48px;
    border-radius: 11px;
    font-weight: 750;
}}

[data-testid="stForm"] {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 25px;
}}

[data-testid="stMetric"] {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 17px;
}}

[data-testid="stExpander"] {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

hr {{
    border-color: {BORDER};
    margin: 25px 0;
}}

.footer {{
    text-align: center;
    color: {MUTED};
    padding: 30px 0;
    font-size: 12px;
}}

@media(max-width: 768px) {{
    .hero {{
        padding: 30px 22px;
        min-height: 300px;
    }}
    .hero-title {{
        font-size: 36px;
        letter-spacing: -1px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 5. LOAD MACHINE LEARNING MODEL
# =====================================================

MODEL_PATH = "model/career_model.joblib"
FEATURE_PATH = "model/features.joblib"

if not os.path.exists(MODEL_PATH):
    st.error("Model not found. Run python train_model.py first.")
    st.stop()

if not os.path.exists(FEATURE_PATH):
    st.error("Features file not found: model/features.joblib")
    st.stop()

try:
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURE_PATH)

    if isinstance(features, dict):
        features = features.get("features", list(features.keys()))

    features = list(features)

except Exception as error:
    st.error(f"Model loading failed: {error}")
    st.stop()

# =====================================================
# 6. CAREER INFORMATION
# =====================================================

career_info = {
    "Software Developer": {
        "icon": "💻",
        "description": "Build software, websites and applications.",
        "skills": ["Python", "Java", "Data Structures", "Git", "Problem Solving"],
        "roadmap": [
            "Learn Python or Java",
            "Study Data Structures and Algorithms",
            "Learn web development",
            "Build real-world projects",
            "Learn Git and GitHub",
            "Apply for internships"
        ]
    },

    "Data Scientist": {
        "icon": "📊",
        "description": "Discover useful information through data and machine learning.",
        "skills": ["Python", "Statistics", "Pandas", "SQL", "Machine Learning"],
        "roadmap": [
            "Learn Python fundamentals",
            "Study NumPy and Pandas",
            "Understand statistics",
            "Learn data visualization",
            "Study Machine Learning",
            "Build data science projects"
        ]
    },

    "Cybersecurity Analyst": {
        "icon": "🔐",
        "description": "Protect computer systems and digital information.",
        "skills": ["Networking", "Linux", "Cybersecurity", "Python", "Analysis"],
        "roadmap": [
            "Learn computer networking",
            "Understand Linux",
            "Study security fundamentals",
            "Practice in legal security labs",
            "Learn security monitoring",
            "Build security projects"
        ]
    },

    "UI/UX Designer": {
        "icon": "🎨",
        "description": "Create attractive and user-friendly digital experiences.",
        "skills": ["Figma", "Creativity", "Design", "Prototyping", "Research"],
        "roadmap": [
            "Learn design fundamentals",
            "Understand UI and UX",
            "Learn Figma",
            "Create wireframes",
            "Study user research",
            "Build a design portfolio"
        ]
    },

    "Business Analyst": {
        "icon": "📈",
        "description": "Understand business problems and support better decisions.",
        "skills": ["Communication", "Excel", "SQL", "Analysis", "Business"],
        "roadmap": [
            "Learn business fundamentals",
            "Improve communication",
            "Master Excel",
            "Learn SQL",
            "Study business intelligence",
            "Create case studies"
        ]
    },

    "Mechanical Engineer": {
        "icon": "⚙️",
        "description": "Design and improve mechanical systems and machines.",
        "skills": ["Mathematics", "Physics", "CAD", "Engineering", "Design"],
        "roadmap": [
            "Study mathematics and physics",
            "Learn engineering fundamentals",
            "Practice CAD software",
            "Study mechanical design",
            "Understand manufacturing",
            "Build engineering projects"
        ]
    }
}

# =====================================================
# 7. NAVIGATION
# =====================================================

n1, n2, n3, n4, n5 = st.columns([3, 1, 1.2, 1.3, 1.1])

with n1:
    st.markdown(
        '<div class="nav-brand">◉ CareerPath <span>AI</span></div>',
        unsafe_allow_html=True
    )

with n2:
    if st.button("⌂ Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

with n3:
    if st.button("✦ Assessment", use_container_width=True):
        st.session_state.page = "Assessment"
        st.rerun()

with n4:
    if st.button("▤ Sessions", use_container_width=True):
        st.session_state.page = "Sessions"
        st.rerun()

with n5:
    if st.button("☀ Light" if not light else "☾ Dark",
                 use_container_width=True):
        st.session_state.light_mode = not light
        st.rerun()

st.markdown("---")

# =====================================================
# 8. REUSABLE CAREER CARDS
# =====================================================

def display_career_cards(results):

    colors = ["#4ade80", "#9990ff", "#fbbf24"]
    columns = st.columns(3)

    for i, (_, row) in enumerate(results.iterrows()):

        career = str(row["Career"])
        probability = float(row["Probability"])
        color = colors[i % 3]

        info = career_info.get(career, {
            "icon": "🎯",
            "description": "Explore this career."
        })

        safe_career = html.escape(career)
        safe_icon = html.escape(info["icon"])

        with columns[i]:

            st.html(f"""
            <div class="career-card">

                <div class="career-name">
                    {safe_icon} {safe_career}

                    <span class="percentage"
                    style="color:{color};border-color:{color};">
                        {probability * 100:.1f}%
                    </span>
                </div>

                <div class="progress-bg">
                    <div class="progress-fill"
                    style="width:{probability * 100:.2f}%;
                    background:{color};">
                    </div>
                </div>

                <div class="card-detail">
                    <span>Model score</span>
                    <span>{probability * 100:.2f}%</span>
                </div>

                <div class="rank" style="color:{color};">
                    RANK # {i + 1}
                </div>

            </div>
            """)

# =====================================================
# 9. HOME PAGE
# =====================================================

if st.session_state.page == "Home":

    st.html("""
    <div class="hero">

        <div class="eyebrow">
            ✧ CAREER INTELLIGENCE STUDIO
        </div>

        <div class="hero-title">
            <span class="gradient-text">Clear Career Signals</span><br>
            Find Your Career Path
        </div>

        <div class="hero-description">
            A guided assessment that transforms your profile into
            ranked career recommendations with clear reasoning
            and immediate next steps.
        </div>

    </div>
    """)

    st.markdown(
        '<div class="section-title">Discover Your Possibilities</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Understand your strengths and explore career opportunities.</div>',
        unsafe_allow_html=True
    )

    if st.button("✦ Start Career Assessment", type="primary"):
        st.session_state.page = "Assessment"
        st.rerun()

    st.markdown("---")

    if st.session_state.results is not None:

        st.markdown(
            '<div class="section-title">Your Career Recommendations</div>',
            unsafe_allow_html=True
        )

        display_career_cards(st.session_state.results)

        for _, row in st.session_state.results.iterrows():

            career = row["Career"]
            info = career_info.get(career, {})

            with st.expander(
                f"{info.get('icon', '🎯')} Explore {career}"
            ):

                st.write(info.get("description", ""))

                st.markdown("**Skills to develop**")
                st.write(" · ".join(info.get("skills", [])))

                st.markdown("**Learning roadmap**")

                for i, step in enumerate(info.get("roadmap", []), 1):
                    st.write(f"{i}. {step}")

    else:

        st.markdown(
            '<div class="section-title">How It Works</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        steps = [
            ("01", "Your Profile", "Share your skills, interests and strengths."),
            ("02", "AI Analysis", "The Random Forest model evaluates your profile."),
            ("03", "Career Matches", "Explore ranked career suggestions and learning paths.")
        ]

        for col, (number, title, description) in zip([c1, c2, c3], steps):

            with col:

                st.html(f"""
                <div class="info-card">

                    <div style="color:#a78bfa;font-weight:800;">
                        STEP {number}
                    </div>

                    <h3>{title}</h3>

                    <p>{description}</p>

                </div>
                """)

        st.markdown(
            '<div class="section-title">Explore Career Areas</div>',
            unsafe_allow_html=True
        )

        career_columns = st.columns(3)

        for i, (career, info) in enumerate(career_info.items()):

            with career_columns[i % 3]:

                st.html(f"""
                <div class="info-card">
                    <h3>{info['icon']} {html.escape(career)}</h3>
                    <p>{html.escape(info['description'])}</p>
                </div>
                """)

# =====================================================
# 10. ASSESSMENT PAGE
# =====================================================

elif st.session_state.page == "Assessment":

    st.markdown(
        '<div class="eyebrow">✧ PERSONAL CAREER PROFILE</div>',
        unsafe_allow_html=True
    )

    st.title("Career Assessment")

    st.write(
        "Rate your skills and interests from 1 to 10. "
        "Answer honestly for a more meaningful demonstration."
    )

    st.markdown("---")

    # The input fields must match the trained feature names.

    default_values = {
        "python_skill": 5,
        "math_skill": 5,
        "communication_skill": 5,
        "creativity": 5,
        "problem_solving": 5,
        "analytical_thinking": 5,
        "design_interest": 5,
        "business_interest": 5
    }

    labels = {
        "python_skill": "Python Programming",
        "math_skill": "Mathematics",
        "communication_skill": "Communication",
        "creativity": "Creativity",
        "problem_solving": "Problem Solving",
        "analytical_thinking": "Analytical Thinking",
        "design_interest": "Design Interest",
        "business_interest": "Business Interest"
    }

    with st.form("career_assessment"):

        st.markdown("### Technical and Analytical Skills")

        left, right = st.columns(2)

        values = {}

        for i, feature in enumerate(features):

            if feature not in default_values:
                st.error(f"Unknown model feature: {feature}")
                st.stop()

            with (left if i % 2 == 0 else right):

                values[feature] = st.slider(
                    labels[feature],
                    min_value=1,
                    max_value=10,
                    value=default_values[feature],
                    key=f"assessment_{feature}"
                )

        st.markdown("---")

        submitted = st.form_submit_button(
            "✦ Generate My Career Matches",
            type="primary",
            use_container_width=True
        )

    if submitted:

        try:

            input_df = pd.DataFrame(
                [[values[f] for f in features]],
                columns=features
            )

            probabilities = model.predict_proba(input_df)[0]

            results = pd.DataFrame({
                "Career": model.classes_,
                "Probability": probabilities
            })

            results = results.sort_values(
                "Probability",
                ascending=False
            ).head(3).reset_index(drop=True)

            st.session_state.results = results

            st.session_state.history.insert(0, {
                "Date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "Top Career": results.iloc[0]["Career"],
                "Score": f"{results.iloc[0]['Probability'] * 100:.2f}%"
            })

            st.success("Your assessment is complete!")

            st.markdown("### Your Top Career Matches")

            display_career_cards(results)

            st.markdown("### Recommended Learning Roadmaps")

            for _, row in results.iterrows():

                career = row["Career"]
                info = career_info.get(career, {})

                with st.expander(
                    f"{info.get('icon', '🎯')} {career}"
                ):

                    st.write(info.get("description", ""))

                    st.markdown("**Skills to develop**")

                    st.write(" · ".join(info.get("skills", [])))

                    st.markdown("**Your learning roadmap**")

                    for i, step in enumerate(
                        info.get("roadmap", []), 1
                    ):
                        st.write(f"{i}. {step}")

            st.download_button(
                "⬇ Download Career Report",
                data=results.to_csv(index=False).encode("utf-8"),
                file_name="CareerPath_AI_Report.csv",
                mime="text/csv"
            )

            st.info(
                "This project uses synthetic demonstration data. "
                "Predictions are educational suggestions, not "
                "professional career advice."
            )

        except Exception as error:

            st.error(f"Prediction failed: {error}")

# =====================================================
# 11. SESSIONS PAGE
# =====================================================

elif st.session_state.page == "Sessions":

    st.markdown(
        '<div class="eyebrow">✧ YOUR ACTIVITY</div>',
        unsafe_allow_html=True
    )

    st.title("Assessment Sessions")

    st.write("Review your previous assessment results.")

    st.markdown("---")

    if st.session_state.history:

        history_df = pd.DataFrame(st.session_state.history)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Session History",
            data=history_df.to_csv(index=False).encode("utf-8"),
            file_name="CareerPath_Sessions.csv",
            mime="text/csv"
        )

    else:

        st.html("""
        <div class="info-card">
            <h3>◷ No sessions yet</h3>
            <p>Complete your first career assessment to see
            your history here.</p>
        </div>
        """)

        if st.button("Start First Assessment", type="primary"):
            st.session_state.page = "Assessment"
            st.rerun()

# =====================================================
# 12. FOOTER
# =====================================================

st.markdown("---")

st.html("""
<div class="footer">
    <div style="font-size:18px;font-weight:800;color:#a78bfa;">
        ◉ CareerPath AI
    </div>
    <br>
    Intelligent Career Discovery Platform
    <br><br>
    Built with Python · Streamlit · Scikit-learn
    <br>
    Machine Learning Major Project
</div>
""")
