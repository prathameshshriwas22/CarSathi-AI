import streamlit as st
import pandas as pd
import joblib
import math


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Car Sathi AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = "car_price_prediction_pipeline.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    st.error(f"❌ Failed to load Car Sathi AI model: {e}")
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = 0

if "profile_type" not in st.session_state:
    st.session_state.profile_type = "Individual"

if "budget" not in st.session_state:
    st.session_state.budget = 700000

if "family_size" not in st.session_state:
    st.session_state.family_size = 5

if "priority" not in st.session_state:
    st.session_state.priority = "Balanced"

if "predicted_price" not in st.session_state:
    st.session_state.predicted_price = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 153, 255, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(138, 43, 226, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(0, 255, 200, 0.10),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #050816 0%,
                #0a1024 45%,
                #07131c 100%
            );

        color: #ffffff;
    }


    /* -------------------------------------------------------
       HIDE STREAMLIT DEFAULT ELEMENTS
    ------------------------------------------------------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* -------------------------------------------------------
       MAIN CONTAINER
    ------------------------------------------------------- */

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* -------------------------------------------------------
       HERO
    ------------------------------------------------------- */

    .hero {
        padding: 45px 40px;
        border-radius: 28px;
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.10),
                rgba(255,255,255,0.03)
            );

        border: 1px solid rgba(255,255,255,0.12);

        box-shadow:
            0 25px 70px rgba(0,0,0,0.45),
            inset 0 1px 0 rgba(255,255,255,0.10);

        backdrop-filter: blur(18px);

        margin-bottom: 30px;
    }


    .hero-title {
        font-size: 58px;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 8px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #5ee7ff,
                #a78bfa
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {
        font-size: 21px;
        color: #b9c7d9;
        max-width: 850px;
        line-height: 1.6;
    }


    /* -------------------------------------------------------
       GLASS CARDS
    ------------------------------------------------------- */

    .glass-card {
        padding: 25px;
        border-radius: 22px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.09),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.11);

        box-shadow:
            0 20px 50px rgba(0,0,0,0.30);

        backdrop-filter: blur(15px);

        margin-bottom: 20px;
    }


    .glass-card h3 {
        margin-top: 0;
    }


    /* -------------------------------------------------------
       AI BADGE
    ------------------------------------------------------- */

    .ai-badge {
        display: inline-block;

        padding: 8px 16px;

        border-radius: 30px;

        background:
            linear-gradient(
                90deg,
                rgba(0,200,255,0.20),
                rgba(150,80,255,0.20)
            );

        border: 1px solid rgba(100,220,255,0.25);

        color: #9cecff;

        font-weight: 600;

        margin-bottom: 15px;
    }


    /* -------------------------------------------------------
       PRICE CARD
    ------------------------------------------------------- */

    .price-card {
        padding: 35px;

        border-radius: 26px;

        background:
            linear-gradient(
                135deg,
                rgba(0,190,255,0.15),
                rgba(115,70,255,0.15)
            );

        border: 1px solid rgba(120,220,255,0.25);

        box-shadow:
            0 25px 70px rgba(0,0,0,0.45);
    }


    .price-label {
        color: #aebed0;
        font-size: 17px;
    }


    .price-value {
        font-size: 48px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 5px;
    }


    /* -------------------------------------------------------
       RECOMMENDATION
    ------------------------------------------------------- */

    .recommendation-card {
        padding: 25px;

        border-radius: 24px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.08),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.12);

        height: 100%;

        box-shadow:
            0 18px 50px rgba(0,0,0,0.30);
    }


    .rank {
        font-size: 14px;
        font-weight: 700;

        color: #8be9ff;

        text-transform: uppercase;

        letter-spacing: 1px;
    }


    .car-name {
        font-size: 24px;
        font-weight: 750;
        margin: 8px 0;
    }


    .car-description {
        color: #b7c5d6;
        line-height: 1.55;
    }


    /* -------------------------------------------------------
       SECTION
    ------------------------------------------------------- */

    .section-title {
        font-size: 30px;
        font-weight: 750;

        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* -------------------------------------------------------
       FOOTER
    ------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #7f8da0;
        padding: 35px 0;
        font-size: 14px;
    }


    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    .stButton > button {
        border-radius: 14px !important;
        min-height: 48px !important;
        font-weight: 650 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:800;
            padding:10px 0;
        ">
        🚗 Car Sathi AI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Your Smart Car Buying Companion")

    st.divider()

    st.markdown("### 🧭 Journey")

    steps = [
        "🏠 Welcome",
        "👤 Your Profile",
        "🚗 Car Requirements",
        "🤖 AI Analysis",
        "🏆 Recommendations"
    ]

    for i, step in enumerate(steps):

        if st.session_state.page == i:

            st.markdown(
                f"""
                <div style="
                    padding:10px;
                    border-radius:10px;
                    background:rgba(70,180,255,0.15);
                    border:1px solid rgba(70,180,255,0.25);
                    margin-bottom:6px;
                ">
                <b>{step}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    padding:8px;
                    color:#8998aa;
                ">
                {step}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.markdown("### 🤖 Model")

    st.write("Tuned Random Forest Regressor")

    st.metric(
        "R² Score",
        "0.9217"
    )

    st.caption(
        "12 vehicle attributes"
    )

    st.divider()

    st.caption(
        "Car Sathi AI • Smart Mobility Intelligence"
    )


# ============================================================
# PAGE 0 — WELCOME
# ============================================================

if st.session_state.page == 0:
    
    st.markdown(
    """
<div class="ai-badge">
    ✨ AI-POWERED CAR COMPANION
</div>

<div class="hero-title">
    Car Sathi AI
</div>

<div class="hero-subtitle">
    Find the right car for your lifestyle,
    understand its estimated value,
    and explore intelligent recommendations —
    all in one place.
</div>
""",
    unsafe_allow_html=True
)


    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="glass-card">

            <h3>👨‍👩‍👧‍👦 Family First</h3>

            <p>
            Tell Car Sathi about your family and
            discover practical vehicle options
            focused on comfort and space.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div class="glass-card">

            <h3>💰 Know Your Value</h3>

            <p>
            Get a machine-learning based estimate
            of the vehicle's resale value.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div class="glass-card">

            <h3>🤖 Smart Suggestions</h3>

            <p>
            Explore three vehicle suggestions
            based on your requirements and priorities.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")

    st.markdown(
        """
        <div class="glass-card">

        <h2>🚘 Let's Find Your Car Sathi</h2>

        <p style="color:#aebed0;">
        Whether you're searching for a family car,
        a city commuter, or your personal upgrade,
        Car Sathi will guide you through the journey.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "🚀 Start My Car Journey",
        type="primary",
        use_container_width=True
    ):

        st.session_state.page = 1
        st.rerun()


# ============================================================
# PAGE 1 — USER PROFILE
# ============================================================

elif st.session_state.page == 1:

    st.markdown(
        """
        <div class="hero">

        <div class="ai-badge">
        STEP 1 • ABOUT YOU
        </div>

        <div class="hero-title">
        Tell Car Sathi About You
        </div>

        <div class="hero-subtitle">
        A good car recommendation starts with
        understanding how you actually use a car.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    profile_type = st.radio(
        "Who are you buying the car for?",
        [
            "👤 Individual",
            "👨‍👩‍👧‍👦 Family",
            "💼 Business / Professional"
        ],
        horizontal=True
    )


    family_size = st.slider(
        "👨‍👩‍👧 Family / Passenger Size",
        min_value=1,
        max_value=10,
        value=5
    )


    budget = st.number_input(
        "💰 Approximate Budget (₹)",
        min_value=50000,
        max_value=10000000,
        value=700000,
        step=50000
    )


    priority = st.selectbox(
        "🎯 What matters most to you?",
        [
            "Balanced",
            "Mileage & Running Cost",
            "Family Comfort",
            "Performance",
            "Luxury & Features",
            "Low Maintenance"
        ]
    )


    st.write("")


    col1, col2 = st.columns(2)

    with col1:

        if st.button("⬅️ Back", use_container_width=True):

            st.session_state.page = 0
            st.rerun()


    with col2:

        if st.button(
            "Continue to Car Requirements ➡️",
            type="primary",
            use_container_width=True
        ):

            st.session_state.profile_type = profile_type
            st.session_state.family_size = family_size
            st.session_state.budget = budget
            st.session_state.priority = priority

            st.session_state.page = 2

            st.rerun()


# ============================================================
# PAGE 2 — CAR REQUIREMENTS
# ============================================================

elif st.session_state.page == 2:

    st.markdown(
        """
        <div class="hero">

        <div class="ai-badge">
        STEP 2 • VEHICLE PROFILE
        </div>

        <div class="hero-title">
        Build Your Ideal Car
        </div>

        <div class="hero-subtitle">
        Now tell Car Sathi what kind of vehicle
        you're looking for.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">🔧 Vehicle Specifications</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        year = st.number_input(
            "📅 Manufacturing Year",
            min_value=1994,
            max_value=2026,
            value=2018,
            step=1
        )


    with col2:

        km_driven = st.number_input(
            "🛣️ Kilometers Driven",
            min_value=1,
            max_value=3000000,
            value=50000,
            step=1000
        )


    col3, col4 = st.columns(2)


    with col3:

        mileage = st.number_input(
            "⛽ Mileage (km/l)",
            min_value=0.1,
            max_value=42.0,
            value=20.5,
            step=0.1
        )


    with col4:

        engine = st.number_input(
            "⚙️ Engine (CC)",
            min_value=624.0,
            max_value=3604.0,
            value=1498.0,
            step=1.0
        )


    col5, col6 = st.columns(2)


    with col5:

        max_power = st.number_input(
            "💪 Max Power (bhp)",
            min_value=32.8,
            max_value=400.0,
            value=110.0,
            step=1.0
        )


    with col6:

        torque_nm = st.number_input(
            "🔩 Torque (Nm)",
            min_value=47.0,
            max_value=1863.0,
            value=250.0,
            step=1.0
        )


    col7, col8 = st.columns(2)


    with col7:

        seats = st.number_input(
            "💺 Seats",
            min_value=2,
            max_value=14,
            value=5,
            step=1
        )


    with col8:

        car_age = st.number_input(
            "🕒 Car Age (Years)",
            min_value=0,
            max_value=32,
            value=8,
            step=1
        )


    st.markdown(
        '<div class="section-title">⛽ Vehicle Details</div>',
        unsafe_allow_html=True
    )


    col9, col10 = st.columns(2)


    with col9:

        fuel = st.selectbox(
            "Fuel Type",
            ["CNG", "Diesel", "LPG", "Petrol"],
            index=1
        )


    with col10:

        seller_type = st.selectbox(
            "Seller Type",
            [
                "Dealer",
                "Individual",
                "Trustmark Dealer"
            ],
            index=1
        )


    col11, col12 = st.columns(2)


    with col11:

        transmission = st.selectbox(
            "Transmission",
            ["Automatic", "Manual"],
            index=1
        )


    with col12:

        owner = st.selectbox(
            "Owner",
            [
                "First Owner",
                "Second Owner",
                "Third Owner",
                "Fourth & Above Owner",
                "Test Drive Car"
            ],
            index=0
        )


    input_data = pd.DataFrame({

        "year": [year],
        "km_driven": [km_driven],
        "fuel": [fuel],
        "seller_type": [seller_type],
        "transmission": [transmission],
        "owner": [owner],
        "mileage": [mileage],
        "engine": [engine],
        "max_power": [max_power],
        "seats": [seats],
        "torque_nm": [torque_nm],
        "car_age": [car_age]

    })


    st.write("")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "⬅️ Back to Profile",
            use_container_width=True
        ):

            st.session_state.page = 1
            st.rerun()


    with col2:

        if st.button(
            "🤖 Analyze My Car",
            type="primary",
            use_container_width=True
        ):

            validation_errors = []


            if km_driven <= 0:
                validation_errors.append(
                    "Kilometers driven must be greater than 0."
                )


            if mileage <= 0:
                validation_errors.append(
                    "Mileage must be greater than 0."
                )


            if engine <= 0:
                validation_errors.append(
                    "Engine must be greater than 0."
                )


            if max_power <= 0:
                validation_errors.append(
                    "Max power must be greater than 0."
                )


            if torque_nm <= 0:
                validation_errors.append(
                    "Torque must be greater than 0."
                )


            if seats < 2 or seats > 14:
                validation_errors.append(
                    "Seats must be between 2 and 14."
                )


            if validation_errors:

                for error in validation_errors:
                    st.error(f"⚠️ {error}")

            else:

                try:

                    with st.spinner(
                        "🤖 Car Sathi AI is analyzing your vehicle..."
                    ):

                        prediction = model.predict(
                            input_data
                        )[0]

                    st.session_state.predicted_price = round(
                        prediction
                    )

                    st.session_state.page = 3

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Prediction failed: {e}"
                    )


# ============================================================
# PAGE 3 — AI ANALYSIS
# ============================================================

elif st.session_state.page == 3:

    predicted_price = st.session_state.predicted_price

    st.markdown(
        """
        <div class="hero">

        <div class="ai-badge">
        ✨ AI ANALYSIS COMPLETE
        </div>

        <div class="hero-title">
        Here's What Car Sathi Found
        </div>

        <div class="hero-subtitle">
        Your vehicle profile has been analyzed
        using the trained Random Forest model.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.balloons()


    st.markdown(
        f"""
        <div class="price-card">

        <div class="price-label">
        💰 Estimated Selling Price
        </div>

        <div class="price-value">
        ₹{predicted_price:,.0f}
        </div>

        <p style="color:#aebed0;">
        Estimated from historical vehicle data
        using Car Sathi AI's trained model.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🤖 Model",
            "Random Forest"
        )


    with col2:

        st.metric(
            "📊 R²",
            "0.9217"
        )


    with col3:

        st.metric(
            "🎯 Median Error",
            "₹46.6K"
        )


    st.write("")


    st.markdown(
        """
        <div class="glass-card">

        <h3>🧠 Car Sathi Insight</h3>

        <p style="color:#b7c5d6;">
        The prediction is an estimated market value,
        not a guaranteed selling price. Vehicle condition,
        location, service history, demand and other factors
        can affect the actual price.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "⬅️ Modify Vehicle",
            use_container_width=True
        ):

            st.session_state.page = 2
            st.rerun()


    with col2:

        if st.button(
            "🏆 Show My Car Suggestions",
            type="primary",
            use_container_width=True
        ):

            st.session_state.page = 4
            st.rerun()


# ============================================================
# PAGE 4 — RECOMMENDATIONS
# ============================================================

elif st.session_state.page == 4:

    budget = st.session_state.budget
    family_size = st.session_state.family_size
    priority = st.session_state.priority
    profile_type = st.session_state.profile_type


    st.markdown(
        """
        <div class="hero">

        <div class="ai-badge">
        🏆 PERSONALIZED CAR SUGGESTIONS
        </div>

        <div class="hero-title">
        Your Car Sathi Shortlist
        </div>

        <div class="hero-subtitle">
        Based on the preferences you shared,
        here are three vehicle categories/models
        to explore further.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SIMPLE RULE-BASED RECOMMENDATION ENGINE
    # --------------------------------------------------------

    recommendations = []


    if family_size >= 7 or "Family" in profile_type:

        recommendations = [

            {
                "rank": "01",
                "name": "Toyota Innova Crysta",
                "type": "Family MPV",
                "description":
                    "A spacious family-oriented option with "
                    "strong practicality, passenger capacity "
                    "and long-distance comfort.",
                "reason":
                    "Suitable for larger families and frequent "
                    "group travel.",
                "image":
                    "https://images.unsplash.com/photo-1551830820-330a71b99659?auto=format&fit=crop&w=1200&q=85"
            },

            {
                "rank": "02",
                "name": "Mahindra XUV500",
                "type": "Family SUV",
                "description":
                    "A practical SUV-style option with generous "
                    "space and a higher driving position.",
                "reason":
                    "Useful for family trips and mixed city/highway use.",
                "image":
                    "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1200&q=85"
            },

            {
                "rank": "03",
                "name": "Maruti Ertiga",
                "type": "Family MPV",
                "description":
                    "A practical people mover focused on everyday "
                    "family usability and running efficiency.",
                "reason":
                    "A practical choice when space and running cost "
                    "are important.",
                "image":
                    "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=1200&q=85"
            }

        ]

    else:

        recommendations = [

            {
                "rank": "01",
                "name": "Hyundai i20",
                "type": "Premium Hatchback",
                "description":
                    "A compact option suited to city driving "
                    "with a comfortable cabin and modern design.",
                "reason":
                    "Suitable for individual and urban usage.",
                "image":
                    "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=1200&q=85"
            },

            {
                "rank": "02",
                "name": "Maruti Baleno",
                "type": "Premium Hatchback",
                "description":
                    "A practical compact car focused on everyday "
                    "commuting and efficiency.",
                "reason":
                    "Good fit for regular city commuting.",
                "image":
                    "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=1200&q=85"
            },

            {
                "rank": "03",
                "name": "Honda City",
                "type": "Sedan",
                "description":
                    "A comfortable sedan option for users looking "
                    "for additional cabin and boot space.",
                "reason":
                    "Suitable for individual users and small families.",
                "image":
                    "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=85"
            }

        ]


    st.markdown(
        """
        <div class="section-title">
        🥇 Top 3 Suggestions
        </div>
        """,
        unsafe_allow_html=True
    )


    cols = st.columns(3)


    for col, car in zip(cols, recommendations):

        with col:

            st.markdown(
                f"""
                <div class="recommendation-card">

                <div class="rank">
                #{car["rank"]} RECOMMENDATION
                </div>

                <div class="car-name">
                {car["name"]}
                </div>

                <p style="color:#8be9ff;">
                {car["type"]}
                </p>

                <p class="car-description">
                {car["description"]}
                </p>

                <p class="car-description">
                <b>Why:</b> {car["reason"]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.image(
                car["image"],
                use_container_width=True
            )


    st.divider()


    selected = recommendations[0]


    st.markdown(
        """
        <div class="section-title">
        🚘 Car Sathi's Featured Suggestion
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns([1.25, 1])


    with col1:

        st.image(
            selected["image"],
            use_container_width=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="glass-card">

            <div class="ai-badge">
            CAR SATHI MATCH
            </div>

            <h2>
            {selected["name"]}
            </h2>

            <p style="color:#8be9ff;">
            {selected["type"]}
            </p>

            <p class="car-description">
            {selected["description"]}
            </p>

            <p class="car-description">
            <b>Why it appears here:</b>
            {selected["reason"]}
            </p>

            <p class="car-description">
            Your profile: {profile_type}
            </p>

            <p class="car-description">
            Passenger requirement: {family_size}
            </p>

            <p class="car-description">
            Priority: {priority}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.info(
        "💡 These suggestions are a prototype recommendation "
        "layer based on your stated preferences. They are not "
        "direct predictions from the Random Forest price model."
    )


    st.write("")


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "🔄 Start Again",
            use_container_width=True
        ):

            st.session_state.page = 0
            st.session_state.predicted_price = None

            st.rerun()


    with col2:

        if st.button(
            "💰 Analyze Another Vehicle",
            type="primary",
            use_container_width=True
        ):

            st.session_state.page = 2

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🚗 <b>Car Sathi AI</b>

    <br><br>

    Smart Used-Car Intelligence

    <br>

    Built with Python • Pandas • Scikit-learn • Streamlit

    <br><br>

    ⚠️ Estimated values and recommendations are for
    informational purposes and should not be treated
    as guaranteed market prices.

    </div>
    """,
    unsafe_allow_html=True
)