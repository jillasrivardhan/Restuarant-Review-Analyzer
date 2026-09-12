import streamlit as st
import requests
import json
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Restaurant Review Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    /* Cards */
    .info-card {
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.20);
        background: rgba(128,128,128,0.04);
        margin-bottom: 15px;
    }

    .positive-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(46, 160, 67, 0.25);
        background: rgba(46, 160, 67, 0.06);
    }

    .negative-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(220, 53, 69, 0.25);
        background: rgba(220, 53, 69, 0.06);
    }

    .history-card {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.20);
        margin-bottom: 12px;
    }

    .metric-title {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.15);
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

OLLAMA_URL = "http://localhost:11434"

# Models that can be shown as suggestions if Ollama is installed
SUGGESTED_MODELS = [
    "llama3.2",
    "llama3.1",
    "mistral",
    "gemma3",
    "phi4",
    "qwen2.5:3b"
]


# ============================================================
# SESSION STATE
# ============================================================

if "review_history" not in st.session_state:
    st.session_state.review_history = []


# ============================================================
# OLLAMA FUNCTIONS
# ============================================================

def check_ollama():
    """
    Check whether the local Ollama server is running.
    """
    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=3
        )

        if response.status_code == 200:
            return True, response.json()

        return False, None

    except requests.exceptions.RequestException:
        return False, None


def get_installed_models(data):
    """
    Extract installed model names from Ollama response.
    """
    if not data:
        return []

    models = data.get("models", [])

    model_names = []

    for model in models:
        name = model.get("name")

        if name:
            model_names.append(name)

    return model_names


def analyze_review(review, model_name):
    """
    Send review to Ollama and request structured JSON output.
    """

    prompt = f"""
You are a restaurant review analysis assistant.

Analyze ONLY the restaurant review provided below.

IMPORTANT RULES:
1. Do not invent information.
2. Do not add facts that are not present in the review.
3. Do not assume restaurant details that the reviewer did not mention.
4. Rating must be between 1 and 5.
5. If the reviewer does not provide an explicit rating,
   infer a reasonable rating only from the review sentiment.
6. Positive points must come directly from things the reviewer liked.
7. Negative points must come directly from things the reviewer disliked.
8. Return ONLY valid JSON.
9. Do not use Markdown.
10. Do not add explanations outside the JSON.

Required JSON format:

{{
    "sentiment": "Positive",
    "rating": 4,
    "top_positive_points": [
        "Food was delicious",
        "Friendly staff"
    ],
    "top_negative_points": [
        "Service was slow"
    ]
}}

Allowed sentiment values:
- Positive
- Neutral
- Negative
- Mixed

Restaurant Review:
\"\"\"
{review}
\"\"\"
"""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        if response.status_code != 200:
            return None, f"Ollama returned HTTP {response.status_code}"

        result = response.json()

        raw_response = result.get("response", "").strip()

        if not raw_response:
            return None, "The model returned an empty response."

        try:
            analysis = json.loads(raw_response)

        except json.JSONDecodeError:
            return None, "The model returned invalid JSON."

        # ----------------------------------------------------
        # Validate structure
        # ----------------------------------------------------

        sentiment = analysis.get("sentiment")
        rating = analysis.get("rating")
        positive = analysis.get("top_positive_points")
        negative = analysis.get("top_negative_points")

        allowed_sentiments = [
            "Positive",
            "Neutral",
            "Negative",
            "Mixed"
        ]

        if sentiment not in allowed_sentiments:
            sentiment = "Neutral"

        try:
            rating = float(rating)

            if rating < 1:
                rating = 1

            if rating > 5:
                rating = 5

            # Convert 4.0 -> 4
            if rating.is_integer():
                rating = int(rating)

        except (ValueError, TypeError):
            rating = 0

        if not isinstance(positive, list):
            positive = []

        if not isinstance(negative, list):
            negative = []

        # Clean list values
        positive = [
            str(item).strip()
            for item in positive
            if str(item).strip()
        ]

        negative = [
            str(item).strip()
            for item in negative
            if str(item).strip()
        ]

        return {
            "sentiment": sentiment,
            "rating": rating,
            "top_positive_points": positive[:5],
            "top_negative_points": negative[:5]
        }, None

    except requests.exceptions.Timeout:
        return None, "The request timed out. The model may be taking too long."

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to Ollama."

    except Exception as e:
        return None, str(e)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🍽️ Restaurant Review Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Turn customer reviews into clear, actionable insights using local AI.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Settings")

    st.markdown("### 🤖 Ollama")

    ollama_running, ollama_data = check_ollama()

    if ollama_running:

        st.success("Ollama is running")

        installed_models = get_installed_models(ollama_data)

        if installed_models:

            st.caption(
                f"{len(installed_models)} model(s) detected"
            )

            selected_model = st.selectbox(
                "Select AI Model",
                installed_models,
                index=0
            )

        else:

            st.warning("No Ollama models found.")

            selected_model = st.selectbox(
                "Suggested models",
                SUGGESTED_MODELS
            )

            st.info(
                "Pull a model first, for example:\n\n"
                "ollama pull llama3.2"
            )

    else:

        st.error("Ollama is not running")

        st.markdown(
            """
            **Start Ollama first.**

            Make sure Ollama is installed and running on your system.

            Then run:

            `ollama list`

            to verify your models.
            """
        )

        selected_model = None

    st.divider()

    st.markdown("### 📊 Analyzer")

    st.caption(
        "The analyzer extracts sentiment, rating, "
        "positive points and negative points."
    )

    st.divider()

    st.markdown("### 🛡️ Local AI")

    st.caption(
        "Your review is processed through your local "
        "Ollama instance rather than a cloud API."
    )


# ============================================================
# MAIN INPUT AREA
# ============================================================

st.markdown("## 📝 Analyze a Review")

review = st.text_area(
    "Paste a restaurant review",
    placeholder=(
        "Example:\n\n"
        "The food was amazing and the staff were very friendly. "
        "The pasta was delicious, but the service was a little slow "
        "and the restaurant was quite crowded."
    ),
    height=180,
    label_visibility="collapsed"
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🔍 Analyze Review",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if not ollama_running:

        st.error(
            "❌ Ollama is not available. "
            "Please start Ollama and try again."
        )

    elif not selected_model:

        st.error(
            "❌ No Ollama model is available."
        )

    elif not review.strip():

        st.warning(
            "⚠️ Please enter a restaurant review first."
        )

    elif len(review.strip()) < 10:

        st.warning(
            "⚠️ Please enter a more detailed review."
        )

    else:

        with st.spinner(
            f"Analyzing review with {selected_model}..."
        ):

            analysis, error = analyze_review(
                review,
                selected_model
            )

        if error:

            st.error(f"❌ Analysis failed: {error}")

        else:

            # Add metadata
            analysis_record = {
                "id": len(st.session_state.review_history) + 1,
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "model": selected_model,
                "review": review.strip(),
                "analysis": analysis
            }

            st.session_state.review_history.insert(
                0,
                analysis_record
            )

            st.success("✅ Review analyzed successfully!")

            st.markdown("## 📊 Analysis Result")

            # ------------------------------------------------
            # Metrics
            # ------------------------------------------------

            col1, col2, col3 = st.columns(3)

            sentiment = analysis["sentiment"]
            rating = analysis["rating"]

            if sentiment == "Positive":
                sentiment_icon = "😊"

            elif sentiment == "Negative":
                sentiment_icon = "😞"

            elif sentiment == "Mixed":
                sentiment_icon = "😐"

            else:
                sentiment_icon = "😶"

            with col1:

                st.markdown(
                    f"""
                    <div class="info-card">
                        <div class="metric-title">
                            SENTIMENT
                        </div>
                        <div class="metric-value">
                            {sentiment_icon} {sentiment}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                stars = "⭐" * int(rating)

                st.markdown(
                    f"""
                    <div class="info-card">
                        <div class="metric-title">
                            RATING
                        </div>
                        <div class="metric-value">
                            {stars} {rating}/5
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:

                total_points = (
                    len(analysis["top_positive_points"])
                    + len(analysis["top_negative_points"])
                )

                st.markdown(
                    f"""
                    <div class="info-card">
                        <div class="metric-title">
                            KEY INSIGHTS
                        </div>
                        <div class="metric-value">
                            💡 {total_points}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ------------------------------------------------
            # Positive / Negative
            # ------------------------------------------------

            positive_col, negative_col = st.columns(2)

            with positive_col:

                st.markdown(
                    '<div class="positive-card">',
                    unsafe_allow_html=True
                )

                st.markdown("### 👍 What the Reviewer Liked")

                positive_points = analysis[
                    "top_positive_points"
                ]

                if positive_points:

                    for point in positive_points:
                        st.markdown(f"✅ {point}")

                else:

                    st.caption(
                        "No specific positive points identified."
                    )

                st.markdown("</div>", unsafe_allow_html=True)

            with negative_col:

                st.markdown(
                    '<div class="negative-card">',
                    unsafe_allow_html=True
                )

                st.markdown("### 👎 What the Reviewer Disliked")

                negative_points = analysis[
                    "top_negative_points"
                ]

                if negative_points:

                    for point in negative_points:
                        st.markdown(f"❌ {point}")

                else:

                    st.caption(
                        "No specific negative points identified."
                    )

                st.markdown("</div>", unsafe_allow_html=True)

            # ------------------------------------------------
            # Original Review
            # ------------------------------------------------

            st.markdown("### 💬 Original Review")

            st.info(review.strip())


# ============================================================
# REVIEW HISTORY
# ============================================================

st.divider()

st.markdown("## 📜 Previous Reviews")

history = st.session_state.review_history

if not history:

    st.info(
        "No previous reviews yet. "
        "Analyze a review and it will appear here."
    )

else:

    for item in history:

        analysis = item["analysis"]

        sentiment = analysis["sentiment"]
        rating = analysis["rating"]

        with st.expander(
            f"#{item['id']} • {sentiment} • "
            f"{rating}/5 ⭐ • {item['timestamp']}"
        ):

            st.markdown("### 💬 Review")

            st.write(item["review"])

            st.markdown("### 📊 Analysis")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"**Sentiment:** {sentiment}"
                )

            with col2:

                st.markdown(
                    f"**Rating:** {rating}/5 ⭐"
                )

            st.markdown("### 👍 Positive Points")

            if analysis["top_positive_points"]:

                for point in analysis["top_positive_points"]:
                    st.markdown(f"• {point}")

            else:

                st.caption("No positive points identified.")

            st.markdown("### 👎 Negative Points")

            if analysis["top_negative_points"]:

                for point in analysis["top_negative_points"]:
                    st.markdown(f"• {point}")

            else:

                st.caption("No negative points identified.")


# ============================================================
# DOWNLOAD SECTION
# ============================================================

if history:

    st.divider()

    st.markdown("## 📥 Export Reviews")

    export_data = json.dumps(
        history,
        indent=4,
        ensure_ascii=False
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        st.caption(
            f"{len(history)} analyzed review(s) ready for export."
        )

    with col2:

        st.download_button(
            label="⬇️ Download JSON",
            data=export_data,
            file_name="restaurant_reviews_analysis.json",
            mime="application/json",
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🍽️ Restaurant Review Analyzer • "
    "Powered by Streamlit + Ollama • "
    "Local AI"
)

