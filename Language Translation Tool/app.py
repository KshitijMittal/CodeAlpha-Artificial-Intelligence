import streamlit as st
import streamlit.components.v1 as components
import json

from utils.languages import LANGUAGES
from utils.translator import translate_text


# Page Configuration
st.set_page_config(
    page_title="AI Language Translation Tool",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "source_text" not in st.session_state:
    st.session_state.source_text = ""

# Custom CSS — Clean & Minimalist
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: #fafafa;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }

    .header-section {
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e5e7eb;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .app-subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    .project-tag {
        display: inline-block;
        background: #f3f4f6;
        color: #4b5563;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.75rem;
        border: 1px solid #e5e7eb;
    }

    .section-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        padding: 0.875rem !important;
        font-size: 0.95rem !important;
        background: white !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }

    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        background: white !important;
        min-height: 42px !important;
    }

    .stSelectbox > div > div:hover {
        border-color: #9ca3af !important;
    }

    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: background 0.15s ease !important;
        box-shadow: none !important;
        height: 42px !important;
        width: 100%;
    }

    .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: none !important;
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2) !important;
    }

    .stTextArea label, .stSelectbox label {
        font-weight: 500 !important;
        color: #374151 !important;
        font-size: 0.875rem !important;
    }

    .stAlert {
        border-radius: 8px !important;
        border: none !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
    }

    .sidebar-heading {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
        margin-top: 1.5rem;
    }

    .sidebar-about {
        color: #4b5563;
        font-size: 0.875rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    .feature-row {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid #f3f4f6;
    }

    .feature-row:last-child {
        border-bottom: none;
    }

    .feature-icon-sm {
        font-size: 1.1rem;
        flex-shrink: 0;
    }

    .feature-text-title {
        font-weight: 500;
        color: #111827;
        font-size: 0.875rem;
        margin: 0;
    }

    .feature-text-desc {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 0.125rem;
    }

    .stats-row {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
    }

    .stat-block {
        display: flex;
        flex-direction: column;
    }

    .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827;
    }

    .stat-text {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 0.125rem;
    }

    .char-counter {
        text-align: right;
        color: #9ca3af;
        font-size: 0.75rem;
        margin-top: 0.375rem;
    }

    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #9ca3af;
        font-size: 0.8rem;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }

    [data-testid="column"] {
        padding: 0 0.5rem;
    }

    .secondary-btn button {
        background: white !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
    }

    .secondary-btn button:hover {
        background: #f9fafb !important;
        border-color: #9ca3af !important;
    }

    /* Remove iframe border for the copy component */
    iframe[title="streamlit_components_v1.html"] {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)


def render_translation_box(text: str, height: int = 210):
    """Render the translation output with an embedded copy button using components.html"""

    is_empty = not text or text.strip() == ""
    display_text = text if not is_empty else "Your translation will appear here"

    # Safely encode the text for JavaScript
    text_json = json.dumps(text if not is_empty else "")
    # Safely encode for HTML display
    display_html = (display_text
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))

    placeholder_class = "placeholder" if is_empty else ""
    disabled_attr = "disabled" if is_empty else ""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: transparent;
            padding: 0;
            margin: 0;
        }}
        .output-wrapper {{
            position: relative;
            width: 100%;
        }}
        .output-box {{
            background: white;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 14px 48px 14px 14px;
            min-height: 200px;
            font-size: 0.95rem;
            color: #111827;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.6;
        }}
        .output-box.placeholder {{
            background: #f9fafb;
            border: 1px dashed #d1d5db;
            color: #9ca3af;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }}
        .copy-icon-btn {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            width: 32px;
            height: 32px;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            padding: 0;
            color: #6b7280;
            outline: none;
        }}
        .copy-icon-btn:hover:not(:disabled) {{
            background: #f9fafb;
            border-color: #9ca3af;
            color: #374151;
        }}
        .copy-icon-btn:active:not(:disabled) {{
            transform: scale(0.95);
        }}
        .copy-icon-btn.copied {{
            color: #10b981;
            border-color: #10b981;
            background: #f0fdf4;
        }}
        .copy-icon-btn:disabled {{
            opacity: 0.4;
            cursor: not-allowed;
        }}
        .copy-icon-btn svg {{
            width: 16px;
            height: 16px;
            display: block;
        }}
    </style>
    </head>
    <body>
        <div class="output-wrapper">
            <div class="output-box {placeholder_class}">{display_html}</div>
            <button class="copy-icon-btn" id="copyBtn" {disabled_attr} title="Copy to clipboard">
                <span id="iconWrap">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                </span>
            </button>
        </div>

        <script>
            const textToCopy = {text_json};
            const btn = document.getElementById('copyBtn');
            const iconWrap = document.getElementById('iconWrap');

            const copyIcon = `
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
            `;

            const checkIcon = `
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            `;

            function fallbackCopy(text) {{
                const ta = document.createElement('textarea');
                ta.value = text;
                ta.style.position = 'fixed';
                ta.style.top = '0';
                ta.style.left = '0';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.focus();
                ta.select();
                try {{
                    document.execCommand('copy');
                }} catch (err) {{
                    console.error('Fallback copy failed:', err);
                }}
                document.body.removeChild(ta);
            }}

            function showCopied() {{
                iconWrap.innerHTML = checkIcon;
                btn.classList.add('copied');
                setTimeout(() => {{
                    iconWrap.innerHTML = copyIcon;
                    btn.classList.remove('copied');
                }}, 3000);
            }}

            if (btn && !btn.disabled) {{
                btn.addEventListener('click', function() {{
                    if (navigator.clipboard && window.isSecureContext) {{
                        navigator.clipboard.writeText(textToCopy).then(() => {{
                            showCopied();
                        }}).catch(() => {{
                            fallbackCopy(textToCopy);
                            showCopied();
                        }});
                    }} else {{
                        fallbackCopy(textToCopy);
                        showCopied();
                    }}
                }});
            }}
        </script>
    </body>
    </html>
    """

    components.html(html, height=height)


# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-heading">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-about">
        An AI-powered translation tool supporting multiple languages with instant results.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-heading">Features</div>', unsafe_allow_html=True)

    features = [
        ("⚡", "Fast Translation", "Instant AI-powered results"),
        ("🌍", "Multi-Language", f"Supports {len(LANGUAGES)} languages"),
        ("📋", "Easy Copy", "One-click clipboard"),
        ("🎯", "Accurate", "High-quality output"),
    ]

    for icon, title, desc in features:
        st.markdown(f"""
        <div class="feature-row">
            <div class="feature-icon-sm">{icon}</div>
            <div>
                <div class="feature-text-title">{title}</div>
                <div class="feature-text-desc">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("Clear All", use_container_width=True, key="clear_btn"):
        st.session_state.translated_text = ""
        st.session_state.source_text = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: #9ca3af; font-size: 0.75rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #f3f4f6;">
        CodeAlpha Internship Project
    </div>
    """, unsafe_allow_html=True)


# Header
st.markdown(f"""
<div class="header-section">
    <h1 class="app-title">🌎 AI Language Translator</h1>
    <p class="app-subtitle">Translate text into multiple languages instantly with AI.</p>
    <span class="project-tag">CodeAlpha Internship Project</span>
    <div class="stats-row">
        <div class="stat-block">
            <div class="stat-value">{len(LANGUAGES)}+</div>
            <div class="stat-text">Languages</div>
        </div>
        <div class="stat-block">
            <div class="stat-value">Instant</div>
            <div class="stat-text">Translation Speed</div>
        </div>
        <div class="stat-block">
            <div class="stat-value">Free</div>
            <div class="stat-text">No Cost</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Translation interface — Two columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-label">📝 Source Text</div>', unsafe_allow_html=True)

    input_text = st.text_area(
        "Enter text to translate",
        height=200,
        placeholder="Type or paste your text here...",
        label_visibility="collapsed",
        key="source_text"
    )

    char_count = len(input_text) if input_text else 0
    st.markdown(f'<div class="char-counter">{char_count} characters</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-label">🎯 Translation</div>', unsafe_allow_html=True)

    render_translation_box(st.session_state.translated_text)

    trans_count = len(st.session_state.translated_text) if st.session_state.translated_text else 0
    st.markdown(f'<div class="char-counter">{trans_count} characters</div>', unsafe_allow_html=True)


# Action bar — Language selector and translate button
st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

col_lang, col_btn = st.columns([3, 1], gap="medium")

with col_lang:
    st.markdown('<div class="section-label">🌐 Target Language</div>', unsafe_allow_html=True)
    target_language = st.selectbox(
        "Select target language",
        list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )

with col_btn:
    st.markdown('<div class="section-label">&nbsp;</div>', unsafe_allow_html=True)
    translate_clicked = st.button("Translate", use_container_width=True)


# Translation Logic
if translate_clicked:
    if not input_text or input_text.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                translated_text = translate_text(
                    input_text,
                    LANGUAGES[target_language]
                )
                st.session_state.translated_text = translated_text
                st.rerun()
            except Exception as e:
                st.error(f"Translation failed: {str(e)}")


# Footer
st.markdown("""
<div class="footer">
    Built with Streamlit · CodeAlpha Internship Project
</div>
""", unsafe_allow_html=True)