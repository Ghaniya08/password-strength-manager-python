import streamlit as st
import random
import string
import re
st.set_page_config(
    page_title="Password Manager",
    page_icon="🔐",
    layout="centered"
)
theme = 'light'
try:
    if st.get_option("theme.base") == "dark":
        theme = 'dark'
except:
    pass
st.markdown(f"""
<style>
    /* Common styles */
    .main-header {{
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        color: {("#1E3A8A" if theme == 'light' else "#90CAF9")};
    }}
    .tab-subheader {{
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        color: {("#2563EB" if theme == 'light' else "#64B5F6")};
    }}
    .password-display {{
        font-family: monospace;
        padding: 10px;
        background-color: {("#F3F4F6" if theme == 'light' else "#1E1E1E")};
        border-radius: 5px;
        border-left: 5px solid {("#2563EB" if theme == 'light' else "#64B5F6")};
        font-size: 1.2rem;
        color: {("#000000" if theme == 'light' else "#FFFFFF")};
    }}
    .result-container {{
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Light mode styles */
    .strong {{
        background-color: {("#ECFDF5" if theme == 'light' else "#0F3D2E")};
        border-left: 5px solid #10B981;
        color: {("#065F46" if theme == 'light' else "#ECFDF5")};
    }}
    .moderate {{
        background-color: {("#FFFBEB" if theme == 'light' else "#3D3000")};
        border-left: 5px solid #F59E0B;
        color: {("#92400E" if theme == 'light' else "#FFFBEB")};
    }}
    .weak {{
        background-color: {("#FEF2F2" if theme == 'light' else "#3D0000")};
        border-left: 5px solid #EF4444;
        color: {("#B91C1C" if theme == 'light' else "#FEF2F2")};
    }}
    .suggestion-item {{
        padding: 8px;
        background-color: {("#F3F4F6" if theme == 'light' else "#2D3748")};
        border-radius: 4px;
        margin: 5px 0;
        color: {("#1F2937" if theme == 'light' else "#E5E7EB")};
    }}
    .footer {{
        text-align: center;
        margin-top: 2rem;
        color: {("#6B7280" if theme == 'light' else "#9CA3AF")};
        font-size: 0.8rem;
    }}
</style>
""", unsafe_allow_html=True)

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make it at least 8 characters long.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include at least one number.")

    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Use at least one special character (!@#$%^&*).")

    if score == 5:
        return "🟢 Strong", "Your password meets all security requirements!", feedback, "strong"
    elif score >= 3:
        return "🟡 Moderate", "Your password is average. Consider improving it.", feedback, "moderate"
    else:
        return "🔴 Weak", "Your password needs improvement:", feedback, "weak"

def generate_password(length=12, use_digits=True, use_symbols=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Header
st.markdown('<div class="main-header">🔐 Password Manager</div>', unsafe_allow_html=True)
st.markdown("Enhance your online security with strong passwords")

# Tabs with icons
tab1, tab2 = st.tabs(["🔍 Check Password", "🔑 Generate Password"])

with tab1:
    st.markdown('<div class="tab-subheader">Check Your Password Strength</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            password = st.text_input("Enter password:", type="password", key="check_password")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            check_button = st.button("Check", use_container_width=True)
    
    if password:
        strength, message, feedback, strength_class = check_password_strength(password)
        
        st.markdown(f"""
        <div class="result-container {strength_class}">
            <h3>{strength}</h3>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if feedback:
            with st.container():
                st.subheader("Suggestions:")
                for tip in feedback:
                    st.markdown(f'<div class="suggestion-item">✓ {tip}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-subheader">Generate a Strong Password</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            length = st.slider("Password length", 6, 32, 12)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            use_digits = st.checkbox("Include digits (123...)", True)
            use_symbols = st.checkbox("Include symbols (!@#...)", True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate_button = st.button("Generate Secure Password", type="primary", use_container_width=True)
    
    if generate_button:
        strong_password = generate_password(length, use_digits, use_symbols)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-container strong">
            <h3>🔐 Your New Password</h3>
            <div class="password-display">{strong_password}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Password Details"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Length", f"{len(strong_password)} chars")
            col2.metric("Complexity", "High" if use_symbols and use_digits and length >= 12 else "Medium")
            col3.metric("Est. Strength", "Strong" if use_symbols and use_digits and length >= 12 else "Good")
            
            st.info("Tip: Store this password in a secure password manager. Never share it with anyone.")

# Footer
st.markdown("""
<div class="footer">
    <p>Secure Password Manager v1.0 | Stay Safe Online | <a href="https://github.com/Ghaniya08">Made By Ghaniya Khan</a> </p>
</div>
""", unsafe_allow_html=True)
