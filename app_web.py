# ============================================
# AgniKristal 2.0 — Web App (Final Version)
# ============================================

import streamlit as st
from PIL import Image
import os

from agnikristal_main import predict_pair
from core.image_engine import generate_cocrystal_image

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "logo.png")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AgniKristal 2.0", layout="wide")

# ---------------- SIDEBAR ----------------
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=140)

st.sidebar.title("AgniKristal")
st.sidebar.write("R&D Cocrystal Engine")

st.sidebar.markdown("---")

st.sidebar.subheader("👨‍💻 Developer")
st.sidebar.write("Bonasi Rambabu")

st.sidebar.markdown("---")

st.sidebar.subheader("📜 Rights")
st.sidebar.write("© 2026 AgniKristal")
st.sidebar.write("All rights reserved")

st.sidebar.markdown("---")
st.sidebar.info("Predict co-crystal formation and visualize 3D interactions.")

# ---------------- HEADER ----------------
col1, col2 = st.columns([1.5, 4])

with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)

with col2:
    st.title("AgniKristal 2.0")
    st.caption("Version 2.0 | AI-powered Cocrystal Prediction & 3D Visualization")

st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.subheader("🧪 Input Details")

api_name = st.text_input("API Name", "Lafutidine")

api_smiles = st.text_input(
    "API SMILES",
    "CC1=NC(=NC(=N1)NCC2=CC=C(C=C2)S(=O)(=O)N)NCC3=CC=CC=C3"
)

cof_name = st.text_input("Coformer Name", "Gallic Acid")

cof_smiles = st.text_input(
    "Coformer SMILES",
    "C1=C(C(=C(C(=C1O)O)O)C(=O)O)"
)

# ---------------- RUN BUTTON ----------------
if st.button("🚀 Run Prediction"):

    result = predict_pair(api_name, api_smiles, cof_name, cof_smiles)

    if result:

        st.success("Prediction Completed Successfully")

        colA, colB = st.columns(2)

        # -------- LEFT: RESULTS --------
        with colA:
            st.subheader("📊 Prediction Summary")

            st.write(f"**API:** {result['api_name']}")
            st.write(f"**Coformer:** {result['coformer_name']}")

            st.write(f"**Probability:** {result['probability']}%")
            st.write(f"**Compatibility:** {result['compatibility']}")
            st.write(
                f"**Stability:** {result['stability_label']} ({result['stability_percent']}%)"
            )

            st.subheader("📌 Final Verdict")
            st.info(result["verdict"])

        # -------- RIGHT: IMAGE --------
        with colB:
            st.subheader("🧬 3D Visualization")

            generate_cocrystal_image(
                result["api_smiles"],
                result["coformer_smiles"],
                "cocrystal.png"
            )

            image_path = os.path.join(BASE_DIR, "cocrystal.png")

            if os.path.exists(image_path):
                img = Image.open(image_path)
                st.image(img, use_container_width=True)
            else:
                st.warning("Image not generated")

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; font-size: 14px; color: grey;'>
        © 2026 <b>AgniKristal 2.0</b> | Developed by <b>Bonasi Rambabu</b><br>
        All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)