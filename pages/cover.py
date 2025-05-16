import streamlit as st

st.set_page_config(page_title="DataLive.AI – Launchpad", layout="centered")

# ---------- CSS amélioré avec animation et effets de profondeur ----------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
        
        /* Dégradé animé */
        body {
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #3a1c71);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            height: 100vh;
            font-family: 'Space Grotesk', sans-serif;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Titre holographique */
        .big-title {
            font-size: 4.5rem;
            font-weight: 700;
            text-align: center;
            color: rgba(255, 255, 255, 0.95);
            text-shadow: 0 0 25px rgba(0, 230, 118, 0.4);
            margin: 1rem 0;
            line-height: 1.1;
            letter-spacing: -1.5px;
            transform: perspective(400px) rotateX(5deg);
        }

        .big-title:hover {
            animation: text-glow 1.5s ease-in-out infinite alternate;
        }

        @keyframes text-glow {
            from { text-shadow: 0 0 10px rgba(0, 230, 118, 0.3); }
            to { text-shadow: 0 0 30px rgba(0, 230, 118, 0.7); }
        }

        .subtitle {
            font-size: 1.4rem;
            text-align: center;
            color: rgba(224, 224, 224, 0.9);
            margin: 1.5rem 0 3rem;
            letter-spacing: 0.5px;
        }

        .logo {
            text-align: center;
            font-size: 1.8rem;
            color: #00e676;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin: 2rem 0;
            position: relative;
        }

        /* Bouton principal centré */
        .launch-button {
            font-size: 1.2rem;
            padding: 1rem 3.5rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #00e676 0%, #00bcd4 100%);
            color: #000;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0, 230, 118, 0.3);
            transition: all 0.4s ease;
        }

        .launch-button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 30px rgba(0, 230, 118, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

# ---------- UI améliorée ----------
st.markdown('<div class="big-title">Transform Data<br>Into Vision</div>', unsafe_allow_html=True)
st.markdown('<div class="logo">DATALIVE.AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Insights • Natural Language Queries<br>Auto-Visualization Engine</div>', unsafe_allow_html=True)

# ---------- Bouton centré ----------
st.markdown("""
<div style="display: flex; justify-content: center; margin-top: 2rem;">
    <form action="pages/data_import.py">
        <button class="launch-button" type="submit"> LAUNCH ANALYTICS</button>
    </form>
</div>
""", unsafe_allow_html=True)
