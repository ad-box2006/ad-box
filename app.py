import streamlit as st
import os
import json
import hashlib
import re
import io
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import time
import base64
def get_encoded_logo():
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None
if "show_splash" not in st.session_state:
    st.session_state.show_splash = True
    st.session_state.splash_start_time = time.time()
SPLASH_DURATION = 3
def show_splash():
    with open("logo.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""     
        <style>
        html, body, .stApp, .AppHost {{
            height: 100%;
            margin: 0;
            padding: 0;
            background-color: #071F2A;
        }}
        .logo-container {{
            background-color: #071F2A;
            display: inline-block;
            padding: 2px;
            border-radius: 8px;
        }}
        @keyframes pulseZoom {{
            0% {{
                transform: scale(1);
                opacity: 1;
            }}
            50% {{
                transform: scale(1.4);
                 opacity: 0.85;
            }}
            100% {{
                transform: scale(1);
                 opacity: 1;
            }}
        }}
        .pulse-zoom {{
            animation-name: pulseZoom;
            animation-duration: 2.5s;
            animation-iteration-count: infinite;
            animation-timing-function: ease-in-out;
            animation-fill-mode: forwards;
            will-change: transform, opacity;                      
            filter: saturate(1.1) contrast(1.05);
            box-shadow: none;
        }}
        
        </style>
        <div style="display:flex; justify-content:center; align-items:center; height:80vh; flex-direction:column;">
            <img src="data:image/png;base64,{encoded_logo}" class="pulse-zoom" style="width:100px; height:100px;" />
            <h2 style="color:#2563EB; font-family: 'Inter' sans-serif; margin-top: 2px; padding-left: 12px;">Ad-Box</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
if st.session_state.show_splash:
    show_splash()
    elapsed = time.time() - st.session_state.splash_start_time
    if elapsed > SPLASH_DURATION:
        st.session_state.show_splash = False
        st.rerun()
    else:
        time.sleep(0.1)
        st.rerun()
    st.stop()

def get_cached_social_icon(filename, target_size):
    main_folder_path = filename
    asset_folder_path = os.path.join("assets", filename)
    if os.path.exists(main_folder_path):
        final_path = main_folder_path
    elif os.path.exists(asset_folder_path):
        final_path = asset_folder_path
    else:
        return None
    try:
        icon_img = Image.open(final_path).convert("RGBA")
        return icon_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    except:
        return None
@st.cache_data(show_spinner=False)
def simple_image_cache(file_bytes):
    if file_bytes is None:
        return None
    try:
            
        img = Image.open(io.BytesIO(file_bytes))
        MAX_PREVIEW_WIDTH = 1080
        if img.width > MAX_PREVIEW_WIDTH:
            scale_ratio = MAX_PREVIEW_WIDTH / float(img.width)
            target_height = int(float(img.height) * float(scale_ratio))
            img = img.resize((MAX_PREVIEW_WIDTH, target_height), Image.Resampling.BILINEAR)
        return img.convert("RGB")
    except:
        return None
if "ad-box_active_canvas" not in st.session_state:
    st.session_state["ad-box_active_canvas"] = None
processed_layer = st.session_state["ad-box_active_canvas"]
   ##############################################
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = False

if st.session_state.logged_in:
    st.set_page_config(page_title="Ad-Box - Dashboard", layout="wide")
else:
    st.set_page_config(page_title="Ad-Box - Welcome", layout="centered")
##################################################################################################################3
DB_FILE = "user_database_profiles.json"
@st.cache_data(show_spinner=False)
def load_local_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "demo_user": hashlib.sha256(str.encode("Admin@123")).hexdigest()
    }
def save_to_local_database(db_dict):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(db_dict, f, indent=4)
        return True
    except Exception:
        return False

                    
if "user_db" not in st.session_state:
    st.session_state.user_db = load_local_database()

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "Login"
        
if "ga_headline" not in st.session_state: st.session_state.ga_headline = ""
if "ga_font_scale" not in st.session_state: st.session_state.ga_font_scale = 32
if "ga_font_style" not in st.session_state: st.session_state.ga_font_style = "Sans-Serif (Clean)"
if "ga_text_pos" not in st.session_state: st.session_state.ga_text_pos = "Bottom Third"
if "ga_veil_opacity" not in st.session_state: st.session_state.ga_veil_opacity = 25
if "ga_filter_lut" not in st.session_state: st.session_state.ga_filter_lut = "Original (None)"
if "ga_blur" not in st.session_state: st.session_state.ga_blur = 0
if "ga_brightness" not in st.session_state: st.session_state.ga_brightness = 1.0
if "ga_contrast" not in st.session_state: st.session_state.ga_contrast = 1.0
if "ga_border_width" not in st.session_state: st.session_state.ga_border_width = 0
if "ga_border_mode" not in st.session_state: st.session_state.ga_border_mode = "Solid Match Token"
if "ga_custom_border_hex" not in st.session_state: st.session_state.ga_custom_border_hex = "#FFFFFF"
if "ga_text_pos_preset" not in st.session_state: st.session_state.ga_text_pos_preset = "Custom Manual Position"
#if "ga_text_color_mode" not in st.session_state: st.session_state.ga_text_color_mode = "Match Token Color"
if "ap_footer_font_scale" not in st.session_state: st.session_state.ap_footer_font_scale = 35    
if "mf_ratio" not in st.session_state: st.session_state.mf_ratio = "Original Ratio"
if "ap_enforce_strip" not in st.session_state: st.session_state.ap_enforce_strip = False
if "ap_watermark_text" not in st.session_state: st.session_state.ap_watermark_text = "CONFIDENTIAL BRAND ASSET"

if "ad_enable_cta" not in st.session_state: st.session_state.ad_enable_cta = False
if "ad_cta_label" not in st.session_state: st.session_state.ad_cta_label = "Shop Now"
if "ad_cta_x" not in st.session_state: st.session_state.ad_cta_x = 65
if "ad_cta_y" not in st.session_state: st.session_state.ad_cta_y = 80

if "ga_text_x_pct" not in st.session_state: st.session_state.ga_text_x_pct = 8
if "ga_text_y_pct" not in st.session_state: st.session_state.ga_text_y_pct = 76
if "tiktok_ui_toggle_widget" not in st.session_state: st.session_state.tiktok_ui_toggle_widget = False
if "insta_ui_toggle_widget" not in st.session_state: st.session_state.insta_ui_toggle_widget = False
if "enable_global_cta_toggle" not in st.session_state: st.session_state.enable_global_cta_toggle = False
########### ########################   ##########################################################################################################
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>|]", password):
        return False, "Password must contain at least one special character."
    return True, "Strong password!"

##########################################################################################################3
def inject_login_styles():
    st.markdown("""
        <style>
        html, body, .stApp, .AppHost [data-testid="stApp"] { background: radial-gradient(circle at top right, #0F172A, #020617) !important; }
        
        div[data-testid="element-container"] + div[data-testid="element-container"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        .stMain h1, stMain h2, stMain h3, stMain p, stMain label {
            color: #F8FAFC !important;
            font-family: 'Inter', sans-serif !important;
        }
        h1, [data-testid="stMarkdownContainer"] h1 {
            background: linear-gradient(to right, #3B82F6, #8B5CF6) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800 !important;
            letter-spacing: -0.05rem !important;
            
        }
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2563EB, #4F46E5) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            width: 100% !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #3B82F6, #6366F1) !important;
            color: #FFFFFF !important;
            border: none !important;
        }

        
        div.stButton > button[kind="secondary"] {
            background-color: rgba(255, 255, 255, 0.03) !important;
            color: #94A3B8 !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
            width: 100% !important;
        }
        div.stButton > button[kind="secondary"] :hover{
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #FFFFFF !important;
            border-color: #475569 !important;
        }
        div[data-baseweb="input"],
        div[data-baseweb="base-input"] {
            background-color: #0F172A !important;
            border: 1px solid #2563EB !important;
            border-radius: 10px !important;
        }
        
        div[data-baseweb="input"] input {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus,
        div[data-baseweb="input"] input:focus {
            -webkit-text-fill-color: #FFFFFF !important;
            -webkit-box-shadow: 0 0 0px 1000px #0F172A !important;
            transition: background-color 5000s ease-in-out 0s !important;
        }
        section[data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        button[data-testid="stSidebarCollapseButton"] {
            display: none !important;
            visibility: hidden !important;
            width: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
def inject_core_dashboard_styles():
    
    st.markdown(f"""
            <style>
            html, body, .stApp {{ background-color: #020617 !important; color: #F8FAFC !important; }}
            [data-testid="stHeader"] {{ background-color: rgba(2, 6, 23, 0.8) !important; backdrop-filter: blur(12px); border-bottom: 1px solid #1E293B !important; }}
            

            div[data-testid="stMainBlockContainer"] {{ 
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
                max-width: 98% !important;
            }}
            
            div[data-testid="stFileUploader"] section {{
                 border: none !important;
                 background-color: #0F172A !important;
                 border-radius: 12px !important;
                 padding: 20px !important;
            }}
            div[data-testid="stFileUploader"] label,  div[data-testid="stFileUploader"] p {{
                 color: #3B82F6 !important;
            
            }}
            div[data-testid="stHorizontalBlock"] {{
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                gap: 4rem !important;
                width: 100% !important;
                align-items: flex-start !important;
                margin-top: 0rem !important;
                padding-top: 0rem !important;
            }}
                
            div[data-testid="stHorizontalBlock"] > div:first-child {{
                top: 0.5rem !important;
                min-width: 48% !important;
                max-width: 48% !important;
                flex: 0 0 48% !important;
                position: sticky !important;
                max-height: calc(100vh - 6rem) !important;
                overflow-y: auto !important;
                overflow-x: hidden !important;
            }}
            div[data-testid="stHorizontalBlock"] > div:last-child {{
                flex: 0 0 48% !important;
                min-width: 48% !important;
                max-width: 48% !important;
                max-height: calc(100vh - 1.5rem) !important;
                overflow-y: auto !important;
                overflow-x: hidden !important;
            }}
            @media (max-width: 600px) {{
                div[data-testid="stHorizontalBlock"] {{
                    flex-direction: column !important;
                    gap: 1.5rem !important;
                }}
                div[data-testid="stHorizontalBlock"] > div:first-child,
                div[data-testid="stHorizontalBlock"] > div:last-child {{
                    flex: 0 0 100% !important;
                    min-width: 100% !important;
                    max-width: 100% !important;
                    max-height: none !important;
                    position: relative !important;
                }}
            }}    
            div[data-baseweb="input"],
            div[data-baseweb="base-input"],
            div[data-baseweb="select"],
            div[data-baseweb="select"] > div {{
                background-color: #0F172A !important;
                border: none !important;
                color: #FFFFFF !important;
                box-shadow: none !important;
            }}
            div[data-baseweb="input"] input,
            div[data-baseweb="select"] span,
            div[data-baseweb="select"] div {{
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
            }}
            .export-box-row {{
                display: flex !important;
                flex-direction: row !important;
                align-items: flex-end !important;
                gap: 12px !important;
                width: 100% !important;
                margin-top: 15px !important;
            }}
            .export-box-row > div {{
                flex: 1 !important;
            }}
            div[data-testid="stHorizontalBlock"] button[data-testid="baseButton-primary"],
            div[data-testid="stHorizontalBlock"] div.stDownloadButton button,
            div[data-testid="stHorizontalBlock"] button[data-testid="BaseButton-primary"] {{
                background: linear-gradient(135deg, #1E40AF, #2563EB) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
                height: 42px !important;
                width: 100% !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 12px rgba(29,78,216,0.3) !important;
            }}
            label[data-testid="stWidgetLabel"] p {{
                color: #CBD5E1 !important;
                font-weight: 500 !important;
            }}
            
            h3 {{
                color: #3B82F6 !important;
                border: none !important;
                margin-top: 30px !important;
                margin-bottom: 10px !important;
            }}
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                border: none !important;
                background-color: transparent !important;
                padding: 0px !important;
            }}
            section[data-testid="stSidebar"], div[data-testid="stSidebarContent"], [data-testid="stSidebar"] {{
                background-color: #0B111E !important;
                border-right: 1px solid #1E3A8A !important;
            }}
            [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {{
                color: #FFFFFF !important;
            }}
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
                color: #CBD5E1 !important;
            }}
            div[data-testid="stImage"] {{
               position: relative !important;
               overflow: visible !important;
               background-color: transparent;
            }}
            body:not(:has([data-testid="stFullscreenLightbox"])) div[data-testid="stImage"] button[data-testid="StyledFullScreenButton"] {{
                position: absolute !important;
                top: 15px !important;
                right: 15px !important;
                z-index: 99999999 !important;
                display: inline-flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                border-radius: 50% !important;
                padding: 8px !important;
                background-color: rgba(15, 23, 42, 0.8) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.6) !important;
                
            }}
            body:has([data-testid="stFullscreenLightbox"]) button[id="MainMenu"],
            body:has([data-testid="stFullscreenLightbox"]) [data-testid="stHeader"] {{
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                width: 0px !important;
                height: 0px !important;
            }}
            body:has([data-testid="stFullscreenLightbox"]) button[data-testid="StyledFullScreenButton"] {{
                position: fixed !important;
                top: 15px !important;
                right: 15px !important;
                background-color: rgba(15, 23, 42, 0.85) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 50% !important;
                display: inline-flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                z-index: 9999999999 !important;
                width: 40px !important;
                height: 40px !important;
            }}
            body:has([data-testid="stFullscreenLightbox"]) div[data-testid="stHorizontalBlock"] > div:last-child,
            body:has([data-testid="stFullscreenLightbox"]) [role="widget"],
            body:has([data-testid="stFullscreenLightbox"]) div[data-baseweb="slider"],
            body:has([data-testid="stFullscreenLightbox"]) div[class*="stSlider"],
            body:has([data-testid="stFullscreenLightbox"]) .stHorizontalBlock {{
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                height: 0px !important;
                width: 0px !important;
                overflow: hidden !important;
            }}
            
            div[data-testid="stFullscreenLightbox"] {{
                z-index: 9999999999 !important;
                background-color: #020617 !important;
                position: fixed !important;
                top: 0 !important; left: 0 !important; width: 100vw !important; height: 100vh !important;
                display: flex !important; align-items: center !important; justify-content: center !important;
            }}
            div[data-testid="stFullscreenLightbox"] img {{
                display: block !important; visibility: visible !important; opacity: 1 !important;
                max-width: 100vw !important; max-height: 100vh !important; margin: auto !important;
            }}
            [data-testid="stHeader"] {{
                background-color: transparent !important;
                background: none !important;
                backdrop-filter: none !important;
                border-bottom: none !important;
                box-shadow: none !important;
            }}
            
            </style>
            <script>
            window.addEventListener('beforeunload', function (e) {{
                e.preventDefault();
                e.returnValue = 'Unsaved changes will be lost! Make sure to export your image first.';
            }});
            </script>
    """, unsafe_allow_html=True)
        

if not st.session_state.logged_in:
    inject_login_styles()
    st.markdown("""
        <div style="text-align: center; margin-top: 5px; margin-bottom: 5px; width: 100%; display: block;">
            <h1 style="font-size: 48px; font-weight: 900; color: blue !important; margin: 0; padding: 0;">Ad-Box</h1>       
            <p style="text-align: center"; "color: blue !important"; font-size: 18px; margin-top: 4px;">Your Ad Studio Toolbox</p>
        </div>
    """, unsafe_allow_html=True)


    
    
    if st.session_state.auth_page == "Login":
    
        login_user = st.text_input("Username / Email", key="l_user", placeholder="Enter your details")
        login_password = st.text_input("password", type="password", key="l_password", placeholder="1234@adcraft")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Forgot Password?", type="secondary"):
                st.session_state.auth_page = "Forgot"
                st.rerun()
        with col2:
            if st.button("Create Account", type="secondary"):
                st.session_state.auth_page = "Register"
                st.rerun()       
            
        if st.button("Login to Ad-Box", type="primary"):  
            hashed_input = hash_password(login_password)
            if login_user in st.session_state.user_db and st.session_state.user_db[login_user] == hashed_input:
                st.session_state.logged_in = True
                st.session_state.current_user = login_user
                st.session_state.is_admin = (login_user == "demo_user")
                st.rerun()
            else:
                st.error("Incorrect password or email. Try again.")
                
############################################################################################################################
    elif st.session_state.auth_page == "Register":
        st.markdown("<h3 style='margin-bottom:0;'>Create Account</h3>", unsafe_allow_html=True)
        new_user = st.text_input("Choose a Username", key="r_user", placeholder="Brand identifier").strip()
        new_password = st.text_input("Choose a Password", type="password", key="r_password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", type="password", key="r_conf", placeholder="Repeat password")
                       
        if st.button("Back to Login", type="secondary"):
            st.session_state.auth_page = "Login"
            st.rerun()
        
        
        if st.button("Register Account", type="primary"):
            if not new_user:
                st.error("Username cannot be blank.")
            elif not new_password or not confirm_password:
                st.error("Passwords fields cannot be empty.")
            
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif new_user in st.session_state.user_db:
                st.error("Username already exists.")
            else:
                is_strong, strength_msg = check_password_strength(new_password)
                if is_strong:
                    st.session_state.user_db[new_user] = hash_password(new_password)
                    save_to_local_database(st.session_state.user_db)
                    st.success("Account registered successfully.")
                    st.session_state.auth_page = "Login"
                    st.rerun()            
                else:
                    st.error(strength_msg)
    elif st.session_state.auth_page == "Forgot":
        st.markdown("### Reset Password")
        st.text_input("Enter Your Registered Email")
        if st.button("Back to login", type="secondary"):
            st.session_state.auth_page = "Login"
            st.rerun()
else:
    inject_core_dashboard_styles()
    logo_data = get_encoded_logo()
    if logo_data:
        st.markdown(f"""
            <div style="position: fixed; top: 15px; left: 50px; z-index: 999999 !important; pointer-events: none !important;;">
                <img src="data:image/png;base64,{logo_data}" width="30" height="30">
            </div>
        """, unsafe_allow_html=True)
    st.sidebar.markdown("### Ad-Box Panel")
    st.sidebar.markdown("### FREE VERSION")
    st.sidebar.markdown(f"Welcome: **{st.session_state.current_user}**!", unsafe_allow_html=True)
    
#############################################################################################################3333    
    
    if st.sidebar.button("Reset SLiders To Sliders", use_container_width=True):
        st.session_state.ga_brightness = 1.0
        st.session_state.ga_contrast = 1.0
        st.session_state.ga_blur = 0
        st.session_state.ga_border_width = 0
        st.rerun()
        
    if st.sidebar.button("Log out", type="primary"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
    
    app_left_col, app_right_col = st.columns([4.5, 1.0], gap="large", vertical_alignment="top")
    
    with app_right_col:
        st.markdown(
            """
            <style>
            [data-testid="stColumn"]:nth-child(1) {
                position: relative !important;
                z-index: 100 !important;
                background-color: #020617 !important;
                padding-right: 20px !important;
                box-shadow: 15px !important;
            }
            .direct-features-scroller {
                max-height: 82vh !important;
                overflow-y: auto !important;
                overflow-x: hidden !important;
                width: 100% !important;
                position: relative !important;
                
            }
            .direct-features-scroller::-webkit-scrollbar {
                width: 6px !important;
            }
            .direct-features-scroller::-webkit-scrollbar-track {
                background: rgba(0,0,0,0) !important;
            }
            .direct-features-scroller::-webkit-scrollbar-thumb {
                border-radius: 10px !important;
                background:  #2563EB !important;
            }

            </style>
            <div class="direct-features-scroller">
            """,
            unsafe_allow_html=True
        )
                    
                
        st.markdown('<div class="workspace-right-controls">', unsafe_allow_html=True)
        if st.session_state.get("is_admin", False):
            tab1, tab2 = st.tabs(["Ad Editor Workspace", "Admin Profile Manager"])
        else:
            tab1, = st.tabs(["Ad Editor Workspace"])
            tab2 = None
        with tab1:
            st.write("### Step 1: Base Media Import")
            uploaded_file = st.file_uploader("Upload Product Asset (.png, jpg)", type=["png", "jpg", "jpg"])
            if "adcraft_render_trigger" not in st.session_state:
                st.session_state.adcraft_render_trigger = False
           
            st.write("### Design Controls")
            
            ad_dimension = st.selectbox("Select Ad Platform Layout", [
                "Original Ratio", "Instagram Widescreen (16:9)", "Instagram Square Feed (1:1)",
                "Instagram Stories & Reels (9:16)", "Pinterest & Google Shop (2:3 Vertical)",
                "Meta High-CTR Mobile Feed (4:5 Potrait)"
            ], key="mf_ratio")           
            ad_filter = st.selectbox("Select One-Click Look Enhancement", [
                "Original (No Filter)", "Vivid Pop (High Saturation)", "Cinematic Vintage (Warm Tone)",
                "Noir (Classic Black & White)", "Cyberpunk Neon (High Contrast / Blue Hue)",
                "UGC Raw Exposure (Authentic Smartphone Shot)"
            ], key="ad_filter_style")
            product_name_val = st.text_input("Your Product Name", value="Timberlands", key="product_name_widget")
                
            niche = st.selectbox("Target Audience Focus", [
                "Problem/Solution", "Impulse Buy Scarcity", "Pure Discount Deal"
            ])
                    
            if niche == "Problem/Solution":
                FREE_PRESET_HOOKS = [
                    "Stop wasting cash on therapy! Try the {product_name}",
                    "Your back pain ends today because of this tiny {product_name} hack...",
                    "The viral product Amazon tried to ban: {product_name}!",
                    "Doctors don't want you knowing about this {product_name} trick...",
                    "If you suffer from bad posture, stop scrolling and look at this {product_name}."
                ]
            elif niche == "Impulse Buy Scarcity":
                FREE_PRESET_HOOKS  = [
                    "Almost SOLD OUT: get your {product_name} now!",
                    "TikTok made me buy it, and honestly it's 100% worth it.",
                    "Only 14 units left of the {product_name} worldwide!",
                    "The price of {product_name} drops to R0 if you click before midnight...",
                    "Don't say we didn't warn you. The viral {product_name} is selling out fast."
                ]
            else:
                FREE_PRESET_HOOKS = [
                    "50% OFF Flash Sale on the {product_name} Bundle!",
                    "Don't scroll! Lowest price ever recorded for {product_name}.",
                    "Buy 1 Get 1 Free on all {product_name} packages today!",
                    "Clearance sale: Grab your {product_name} for pennies on the dollar.",
                    "Massive price drop on {product_name}. Limited time offer!"
                ]
            generate_button = st.button("Apply Changes & Generate Creative")
            if generate_button:
                st.session_state.adcraft_render_trigger = True
            
            selected_hook_template = st.selectbox("Select your ad hook template", options=FREE_PRESET_HOOKS, key="ad_hook_selection_widget")
            active_product_text = product_name_val.strip() if product_name_val else "Product"
            final_processed_hook_text = selected_hook_template.format(product_name=active_product_text) if FREE_PRESET_HOOKS else "Explore catalog collections today."
            st.session_state.ga_brightness = st.slider("Base Image Brightness Scale", 0.5, 2.0, 1.0)
            st.session_state.ga_contrast = st.slider("Base Image Contrast Scale", 0.5, 2.0, 1.1)
            st.session_state.ga_blur = st.slider("Layer Blur Filter Intensity", 0, 10, 0)
            st.session_state.ga_border_width = st.slider("Border Thickness Percent", 0, 15, 0)                
              
           
            st.write("### Step 3: Sticker Badges")
            
            scarcity_tag = st.checkbox("Show ' SELLING FAST - RESTOCKING SOON' Scarcity Footer Banner", value=True)
            scarcity_text = st.text_input("Customize Footer Text", value="SELLING FAST - RESTOCKING SOON", disabled=not scarcity_tag, key="custom_scarcity_text")
            discount_badge = st.checkbox("Stamp Promo Sticker", value=False)
            discount_text =  st.text_input("Sticker Text", value="50% OFF TODAY", disabled=not discount_badge, key="custom_discount_text")
            sticker_theme = st.selectbox(
                "Sticker High-CTR Color Combo",
                ["Urgent Flash (Neon Yellow / Black Text)", "Clearance Deal (Crimson Red / White Text)", "Minimalist Clean (Matte Black / White Text)"],
                disabled=not discount_badge,
                key="sticker_theme_select"
            )
            sticker_position = st.selectbox(
                "Sticker Smart Position",
                ["Top Left Corner", "Top Right Corner", "Center Canvas Focal Point"],
                disabled=not discount_badge,
                key="sticker_pos_select"
            )
            st.write("### Step 4: Native Social Previews")
            
            apply_tiktok_ui = st.checkbox("Overlay Transparent TikTok Native UI Layout Elements", key="tiktok_ui_toggle_widget")
            
            apply_ig_ui = st.checkbox("Overlay Instagram Feed UI Layout Elements", key="insta_ui_toggle_widget")
            brand_input_value = st.text_input("Enter creator name (without @)", value=st.session_state.get("brand_handle_input_widget", "creator"))
            st.session_state["brand_handle_input_widget"] = brand_input_value.strip()
            st.write("DEBUG: Creator name is:", brand_input_value)
            if apply_ig_ui:
                st.markdown("**Brand Profile**")
                with st.container(border=True):
                    st.file_uploader(
                        "Upload Brand Avatar",
                        type=["png", "jpg", "jpeg"],
                        key="user_profile_upload_widget"
                    )
            
            ad_enable_cta = st.checkbox("Stamp High-CTR Sponsored CTA Button", key="enable_global_cta_toggle")
            ad_cta_label = st.text_input("Button Text String", value="Shop Now", disabled=not ad_enable_cta, key="global_cta_text_field")
            
            if "16:9" in ad_dimension:
                canvas_w, canvas_h = 1920, 1080
            elif "1:1" in ad_dimension:
                canvas_w, canvas_h = 1080, 1080
            elif "9:16" in ad_dimension:
                canvas_w, canvas_h = 1080, 1920
            elif "2:3" in ad_dimension:
                canvas_w, canvas_h = 1080, 1620
            elif "4:5" in ad_dimension:
                canvas_w, canvas_h = 1080, 1350
            elif "Original Ratio" in ad_dimension and uploaded_file is not None and 'base_canvas' in locals() and base_canvas:
                
                canvas_w, canvas_h = base_canvas.size
            else:
                canvas_w, canvas_h = 1080, 1080
        
            if uploaded_file is None:
                processed_layer = Image.new("RGB", (canvas_w, canvas_h), "#111827")
                draw = ImageDraw.Draw(processed_layer)
                try: fallback_font = ImageFont.load_default(size=20)
                except: fallback_font = ImageFont.load_default()
                placeholder_text = f"Drop your ad product....."
                wrapped_placeholder = textwrap.wrap(placeholder_text, width=50 if canvas_w < canvas_h else 50)
                text_y = canvas_h // 2 - (len(wrapped_placeholder) * 25)
                for line in wrapped_placeholder:
                    try: text_w = draw.textlength(line, font=fallback_font)
                    except: text_w = len(line) * 14
                    text_x = (canvas_w - text_w) // 2
                    draw.text((text_x, text_y), line, fill="#FFFFFF", font=fallback_font)
                    text_y += int(canvas_h * 0.04)
                
            else:
                if 'base_canvas' in locals() and base_canvas:
                    processed_layer = base_canvas.copy()
                else:    
                    raw_file_bytes = uploaded_file.getvalue()
                    base_canvas = simple_image_cache(raw_file_bytes)
                    if base_canvas is not None:
                        processed_layer = base_canvas.copy()
                    else:
                        processed_layer = Image.new("RGB", (canvas_w, canvas_h), "#111827")
                        
                processed_layer = processed_layer.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
                st.session_state["ad-box_active_canvas"] = processed_layer
                if st.session_state.get("ga_brightness", 1.0) != 1.0:
                    processed_layer = ImageEnhance.Brightness(processed_layer).enhance(st.session_state.ga_brightness)        
                if st.session_state.get("ga_contrast", 1.0) != 1.0:
                    processed_layer = ImageEnhance.Contrast(processed_layer).enhance(st.session_state.ga_contrast)
                
                
                if "Vivid Pop" in ad_filter:
                    processed_layer = ImageEnhance.Color(processed_layer).enhance(1.6)
                    processed_layer = ImageEnhance.Contrast(processed_layer).enhance(1.1)
                elif "Cinematic Vintage" in ad_filter:
                    processed_layer = ImageEnhance.Color(processed_layer).enhance(0.85)
                    r, g, b = processed_layer.split()
                    r = r.point(lambda i: min(255, int(i * 1.08)))
                    b = b.point(lambda i: int(i * 0.90))
                    processed_layer = Image.merge("RGB", (r, g, b))
                elif "Noir" in ad_filter:
                    processed_layer = ImageOps.grayscale(processed_layer).convert("RGB")
                    processed_layer = ImageEnhance.Contrast(processed_layer).enhance(1.2)
                elif "Cyberpunk Neon" in ad_filter:
                    processed_layer = ImageEnhance.Color(processed_layer).enhance(1.6)
                    processed_layer = ImageEnhance.Contrast(processed_layer).enhance(1.3)
                    r, g, b = processed_layer.split()
                    b = b.point(lambda i: min(255, int(i * 1.25)))
                    r = r.point(lambda i: int(i * 0.95))
                    processed_layer = Image.merge("RGB", (r, g, b))
                elif "UGC Raw Exposure" in ad_filter:
                    processed_layer = ImageEnhance.Contrast(processed_layer).enhance(0.92)
                    processed_layer = ImageEnhance.Brightness(processed_layer).enhance(1.08)
                    processed_layer = ImageEnhance.Color(processed_layer).enhance(0.95)
              
                if st.session_state.get("ga_blur", 0) > 0:
                    processed_layer = processed_layer.filter(ImageFilter.GaussianBlur(st.session_state.ga_blur))
        
                if st.session_state.get("ga_border_width", 0) > 0:
                    border_pixels = int(max(processed_layer.width, processed_layer.height) * (st.session_state.ga_border_width / 100))           
                    border_fill_color = "#FFFFFF"            
                    processed_layer = ImageOps.expand(processed_layer, border=border_pixels, fill=border_fill_color)
                
                processed_layer = processed_layer.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
            
            draw = ImageDraw.Draw(processed_layer)
            w, h = processed_layer.size
            is_tall_ratio = h > w
            is_square_ratio = abs(w - h) < (max(w, h) * 0.05)
            btn_w = int(w * 0.88)
            btn_h = max(36, int(h * 0.052))
            btn_x1 = int((w - btn_w) / 2)
            is_social_ui_active = apply_ig_ui or apply_tiktok_ui
            if scarcity_tag:
                banner_height = int(h * 0.08) if h > 0 else 120
                if is_social_ui_active:
                    btn_y1 = h - banner_height - btn_h - 50
                else:
                    btn_y1 = h - banner_height - btn_h - 12
                #active_footer_ceiling = btn_y1
            else:
                banner_height = 0
                if is_social_ui_active:
                    btn_y1 = h - btn_h - 60
                else:
                    btn_y1 = h - btn_h - 60
            
            if ad_enable_cta:
                active_footer_ceiling = btn_y1
            else:
                if scarcity_tag:
                    active_footer_ceiling = h - banner_height - 25
                else:
                    active_footer_ceiling = h - 40 
                        
                
            try:
                font_headline = ImageFont.truetype("Arial.ttf", 36)
                font_badge = ImageFont.truetype("Arial.ttf", 24)
            except:
                font_headline = ImageFont.load_default()
                font_badge = ImageFont.load_default()
                
            if st.session_state.get("ga_headline", ""):
                wrapped_lines = textwrap.wrap(st.session_state.ga_headline, width=40)
                line_height = 40
                banner_height = 40 + (len(wrapped_lines) * line_height)
      
                overlay_layer = Image.new('RGBA', processed_layer.size, (0,0,0,0))
                overlay_draw = ImageDraw.Draw(overlay_layer)
                overlay_draw.rectangle([(0, 0), (canvas_w, banner_height)], fill=(0, 0, 0, 180))
                processed_layer = Image.alpha_composite(processed_layer.convert("RGBA"), overlay_layer).convert("RGB")
                 
                draw = ImageDraw.Draw(processed_layer)
                current_y = 30
                for line in wrapped_lines:
                    draw.text((30, current_y), line, fill="#FFFFFF", font=font_headline)
                    current_y += line_height
                
                
                    
            if apply_ig_ui:
                draw = ImageDraw.Draw(processed_layer)
                w, h = processed_layer.size
                
                profile_radius = max(16, int(w * 0.035))
                profile_x = int(w * 0.018)
                profile_y = int(h * 0.02)
                avatar_diameter = profile_radius * 2
                
                draw.ellipse([profile_x, profile_y, profile_x + avatar_diameter, profile_y + avatar_diameter], fill=(30, 41, 59))
                
                creator_handle_font_size = max(14, int(w * 0.037))
                try: creator_handle_font = ImageFont.truetype("arialbd.ttf", creator_handle_font_size)
                except:
                    try: creator_handle_font = ImageFont.truetype("arial.ttf", creator_handle_font_size)
                    except: creator_handle_font = ImageFont.load_default()
                    
                    
                brand_input_value = st.session_state.get("brand_handle_input_widget", "").strip()
                if not brand_input_value:
                    brand_input_value = "creator"
                display_handle = f"@{brand_input_value}"
                   
                profile_file = st.session_state.get("user_profile_upload_widget", None)
                if profile_file is not None:
                    try:
                        avatar_bytes = profile_file.getvalue()
                        raw_avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
                        min_edge = min(raw_avatar.size)
                        left_crop = (raw_avatar.width - min_edge) // 2
                        top_crop = (raw_avatar.height - min_edge) // 2
                        raw_avatar = raw_avatar.crop((left_crop, top_crop, left_crop + min_edge, top_crop + min_edge))
                        raw_avatar = raw_avatar.resize((avatar_diameter, avatar_diameter), Image.Resampling.LANCZOS)
                        
                        mask_layer = Image.new("L", (avatar_diameter, avatar_diameter), 0)
                        mask_draw =ImageDraw.Draw(mask_layer)
                        mask_draw.ellipse([0, 0, avatar_diameter, avatar_diameter], fill=255)
                        raw_avatar.putalpha(mask_layer)
                        processed_layer.paste(raw_avatar, (profile_x, profile_y), mask=raw_avatar)
                        draw = ImageDraw.Draw(processed_layer)
                    except:
                        profile_file = None
                        
                if profile_file is None:
                    avatar_letter = display_handle[1].upper() if len(display_handle) > 1 else "C"
                    try: avatar_font = ImageFont.truetype("arialbd.ttf", int(profile_radius * 1.1))
                    except: avatar_font = creator_handle_font
                    
                    av_text_x = profile_x + int(profile_radius * 0.65)
                    av_text_y = profile_y + int(profile_radius * 0.35)
                    draw.text((av_text_x + 1, av_text_y + 1), avatar_letter, fill=(0, 0, 0), font=avatar_font)
                    
                    draw.text((av_text_x, av_text_y), avatar_letter, fill=(255, 255, 255), font=avatar_font)
                
                metric_font_size = max(12, int(w * 0.026))
                try: metric_font = ImageFont.truetype("arial.ttf", metric_font_size)
                except: metric_font = ImageFont.load_default()
                
                caption_font_size = max(14, int(w * 0.028))
                try: caption_font = ImageFont.truetype("arialbd.ttf", caption_font_size)
                except:
                    try: caption_font = ImageFont.truetype("arial.ttf", caption_font_size)
                    except: caption_font = creator_handle_font
                    
                text_margin_x = int(w * 0.04) 
                is_landscape = w > h 
                custom_hook = final_processed_hook_text
                usable_pixel_width = int(w * 0.80)
                estimated_char_pixel_width = int(caption_font_size * 0.55)
                max_line_width = int(usable_pixel_width / estimated_char_pixel_width)
                max_line_width = max(25, max_line_width)
                
                wrapped_caption_lines = textwrap.wrap(final_processed_hook_text, width=max_line_width)
                total_caption_lines_count = len(wrapped_caption_lines)
                caption_line_height = int(caption_font_size * 1.5)
                caption_block_height = total_caption_lines_count * caption_line_height
                likes_row_height = 45 + int(metric_font_size * 1.25)
                current_caption_y = active_footer_ceiling - caption_block_height - likes_row_height - 45
                draw.text((text_margin_x, current_caption_y), f"{display_handle} ", fill="#FFFFFF", font=caption_font)
                
                verified_icon = get_cached_social_icon("verified_icon.png", int(caption_font_size * 1.3))
                if verified_icon:
                    bbox = draw.textbbox((0, 0), f"{display_handle} ", font=caption_font)
                    username_width = bbox[2] - bbox[0] 
                    badge_x = text_margin_x + username_width
                    badge_y = current_caption_y + (caption_font_size - verified_icon.height) // 2
                    processed_layer.paste(verified_icon, (badge_x, badge_y), mask=verified_icon)
                
                current_caption_y += caption_line_height
                for line_item in wrapped_caption_lines:  
                    draw.text((text_margin_x, current_caption_y), line_item, fill="#E5E7EB", font=caption_font)
                    current_caption_y += caption_line_height
                
                current_caption_y += 70
                try: likes_font = ImageFont.truetype("arial.ttf", metric_font_size)
                except: likes_font = creator_handle_font
                draw.text((text_margin_x, current_caption_y), "1,506 likes", fill="#0095F6", font=likes_font)      
                icon_size = max(14, int(w * 0.040))
                icon_y = active_footer_ceiling - 50 if (ad_enable_cta or apply_ig_ui) else h - 50
                target_icon_y = active_footer_ceiling - 70
                lx = int(w * 0.05)
                cx = lx + icon_size + int(w * 0.04)                                                 
                sx = cx + icon_size + int(w * 0.04)
                bx = w - int(w * 0.05) - icon_size
                    
                icon_mapping = [
                    ("ig_like (3) - Copy.png", lx),
                    ("ig_comment (2) - Copy.png", cx), 
                    ("ig_share - Copy.png", sx), 
                    ("ig_bookmark - Copy.png", bx),
                ]
                for filename, x_pos in icon_mapping:
                            
                    icon_img = get_cached_social_icon(filename, icon_size)
                    if icon_img:
          
                        processed_layer.paste(icon_img, (x_pos, target_icon_y), mask=icon_img)
                    else:
                        draw.ellipse([x_pos, target_icon_y, x_pos + icon_size, target_icon_y + icon_size], fill=(255, 255, 255))
               
                draw = ImageDraw.Draw(processed_layer)
            
            if ad_enable_cta:
                btn_y1 = active_footer_ceiling + 8
                btn_x2 = btn_x1 + btn_w
                btn_y2 = btn_y1 + btn_h
                cylinder_radius = btn_h // 2
                draw.rounded_rectangle([btn_x1, btn_y1, btn_x2, btn_y2], fill="#1E73EB", radius=cylinder_radius)
                cta_font_size = max(72, int(btn_h * 1.0))
                try: cta_font = ImageFont.truetype("ARIAL.TTF", cta_font_size)
                except: cta_font = ImageFont.load_default()
                cta_text_label = st.session_state.get("global_cta_text_field", "Shop Now")
                
                try:
                    bbox = draw.textbbox((0, 0), cta_text_label, font=cta_font)
                    cta_w = bbox[2] - bbox[0]
                    cta_h = bbox[3] - bbox[1]
                except:
                    cta_w = len(cta_text_label) * int(cta_font_size * 0.9)
                    cta_h = cta_font_size
                    
                cta_inside_x = btn_x1 + (btn_w - cta_w) // 2
                cta_inside_y = btn_y1 + (btn_h - cta_h) / 2 - 2
                
                draw.text((cta_inside_x + 1, cta_inside_y + 1), cta_text_label, fill=(0, 0, 0), font=cta_font)
                draw.text((cta_inside_x, cta_inside_y), cta_text_label, fill="#FFFFFF", font=cta_font)       
            if scarcity_tag:
                w, h = processed_layer.size
                banner_height = int(h * 0.08) if h > 0 else 120
                draw = ImageDraw.Draw(processed_layer)
                draw.rectangle([(0, h - banner_height), (w, h)], fill="#DC2626")
                font_size_badge = max(20, int(banner_height * 0.42)) if h > w else max(20, int(w * 0.035))
                try: font_badge = ImageFont.truetype("arialbd.ttf", font_size_badge)
                except: font_badge = ImageFont.load_default()
                      
                try:
                    badge_text_width = draw.textlength(scarcity_text, font=font_badge)
                    badge_text_height = font_size_badge
                except:
                    badge_text_width = len(scarcity_text) * int(font_size_badge * 0.55)
                    badge_text_height = font_size_badge
                banner_center_x = int((w - badge_text_width) / 2)
                banner_center_y = int(h - (banner_height / 2) - (badge_text_height / 2))
                draw.text((banner_center_x + 1, banner_center_y + 1), scarcity_text, fill=(0, 0, 0), font=font_badge)
                draw.text((banner_center_x, banner_center_y), scarcity_text, fill="#FFFFFF", font=font_badge)
            
            if apply_ig_ui:
                f_size = profile_font_size if 'profile_font_size' in locals() else max(14, int(w * 0.03))   
                sponsor_font_size = max(11, int(f_size * 0.8))
                try: sponsor_font = ImageFont.truetype("arial.ttf", sponsor_font_size)
                except: sponsor_font = ImageFont.load_default()
                profile_radius_calc = max(16, int(w * 0.035))
                profile_avatar_diameter = profile_radius_calc * 2
                       
                sponsor_text_x = int(w * 0.01) + profile_avatar_diameter + int(w * 0.02)
                sponsor_text_y = int(h * 0.0) + int((profile_avatar_diameter - creator_handle_font_size) / 2) + creator_handle_font_size - 4
                
                draw.text((sponsor_text_x + 1, sponsor_text_y + 1), "Sponsored", fill=(0, 0, 0), font=sponsor_font)
                draw.text((sponsor_text_x + 2, sponsor_text_y + 2), "Sponsored", fill=(0, 0, 0), font=sponsor_font)
                draw.text((sponsor_text_x, sponsor_text_y), "Sponsored", fill=(178, 178, 178), font=sponsor_font)
            else:
                ad_box_w = max(38, int(w * 0.065))
                ad_box_h = max(18, int(h * 0.038))
           
                ad_corner_x1 = int(w * 0.04)
                ad_corner_y1 = int(h * 0.04)
                badge_overlay = Image.new("RGBA", processed_layer.size, (0, 0, 0, 0))
                badge_draw = ImageDraw.Draw(badge_overlay)
                badge_draw.rounded_rectangle([ad_corner_x1, ad_corner_y1, ad_corner_x1 + ad_box_w, ad_corner_y1 + ad_box_h], fill=(15, 23, 42, 90), radius=4)
                ad_label_font_size = max(11, int(w * 0.024))
                try: ad_label_font = ImageFont.truetype("arialbd.ttf", ad_label_font_size)
                except: ad_label_font = ImageFont.load_default() 
             
                try: ad_text_w = draw.textlength("Ad", font=ad_label_font)
                except: ad_text_w = len("Ad") *  (ad_label_font_size * 0.5)
                ad_txt_x = ad_corner_x1 + int((ad_box_w - ad_text_w) / 2)
                ad_txt_y = ad_corner_y1 + int((ad_box_h - ad_label_font_size) / 2) - 1
                badge_draw.text((ad_txt_x, ad_txt_y), "Ad", fill=(255, 255, 255, 255), font=ad_label_font) 
                processed_layer.paste(badge_overlay, (0, 0), mask=badge_overlay)
                draw = ImageDraw.Draw(processed_layer)
                                
            if discount_badge:
                badge_draw = ImageDraw.Draw(processed_layer)
                w, h = processed_layer.size
                circle_radius = int((w + h) * 0.055) if w > 0 else 80
                circle_diameter = circle_radius * 2
                font_size_sticker = max(22, int(circle_radius * 0.38))
                try: font_sticker = ImageFont.truetype("arialbd.ttf", font_size_sticker)
                except:
                    try: font_sticker = ImageFont.truetype("arial.ttf", font_size_sticker)
                    except: font_sticker = badge_draw.load_default()
                if "Urgent Flash" in sticker_theme:
                    bg_color, txt_color = "#F59E0B", "#060B13"
                elif "Clearance Deal" in sticker_theme:
                    bg_color, txt_color = "#DC2626", "#FFFFFF"
                else:
                    bg_color, txt_color = "#0F172A", "#FFFFFF"
                if sticker_position == "Top Left Corner":
                    if apply_ig_ui or apply_tiktok_ui:
                        center_x = int(w * 0.03) + circle_radius 
                        center_y = int(h * 0.10) + circle_radius
                    else:
                        center_x = int(w * 0.01) + circle_radius 
                        center_y = int(h * 0.08) + circle_radius 
                elif sticker_position == "Top Right Corner":
                    if apply_ig_ui or apply_tiktok_ui:
                        center_x = w - circle_radius - int(w * 0.03)
                        center_y = int(h * 0.10) + circle_radius
                    else:
                        center_x = w - circle_radius - int(w * 0.01)
                        center_y = int(h * 0.08) + circle_radius
                else:
                    center_x = int(w / 2)
                    center_y = int(h / 2)
                cx1 = center_x - circle_radius
                cy1 = center_y - circle_radius
                cx2 = center_x + circle_radius
                cy2 = center_y + circle_radius
                badge_draw.ellipse([cx1, cy1, cx2, cy2], fill=bg_color)
                words_list = discount_text.split()
                if len(words_list) >= 3:
                    
                    lines_to_draw = [
                        " ".join(words_list[:2]),
                        " ".join(words_list[2:])
                    ]
                elif len(words_list) == 2:
                    lines_to_draw = [words_list[0], words_list[1]]
                else:
                    lines_to_draw = [discount_text]
                line_height_padding = int(font_size_sticker * 1.15)
                total_block_height = len(lines_to_draw) * line_height_padding
                start_render_y = center_y - (total_block_height // 2) + int(font_size_sticker * 0.1)
                for index_step, single_line in enumerate(lines_to_draw):
                    try: line_w = badge_draw.textlength(single_line, font=font_sticker)
                    except: line_w = len(single_line) * int(font_size_sticker * 0.55)
                    text_inside_x = center_x - int(line_w / 2)
                    text_inside_y = start_render_y + (index_step * line_height_padding)
                    badge_draw.text((text_inside_x, text_inside_y), single_line, fill=txt_color, font=font_sticker)
            if apply_tiktok_ui:
                tiktok_draw = ImageDraw.Draw(processed_layer)
                w, h = processed_layer.size
                scale_factor = (w + h) / 2
                ui_font_size = int(scale_factor * 0.027) if scale_factor > 0 else 27
                ui_font_size = max(ui_font_size, 16)
                icon_font_size = int(scale_factor * 0.029) if scale_factor > 0 else 29
                
                try:
                    ui_font = ImageFont.truetype("arial.ttf", ui_font_size)
                    ui_font_bold = ImageFont.truetype("arial.ttf", ui_font_size)
                except: 
                    ui_font = ImageFont.load_default() 
                    ui_font_bold = ImageFont.load_default()
                     
                is_square = abs(w - h) < (max(w, h) * 0.05)
                base_start_y = int(h * 0.35 if is_square else h * 0.42)
                icon_spacing = int(h * 0.11 if is_square else h * 0.13)
                disc_height_scale = 1.0
                icon_center_x = int(w * 0.94)
                
                heart_count = st.session_state.get("custom_heart", "50.2M")
                comment_count = st.session_state.get("custom_comment", "92.1k")
                save_count = st.session_state.get("custom_save", "10k")
                share_count = st.session_state.get("custom_share", "78.4k")
                tiktok_sidebar = [
                    ("icon_heart (2).png", heart_count),
                    ("icon_comment.png", comment_count),
                    ("icon_save-instagram.png", save_count),
                    ("icon_share (2).png", share_count)
                ]
                pfp_radius = int(w * 0.035)
                pfp_y = base_start_y - int(h * 0.10 if is_square else h * 0.12)
                profile_file = st.file_uploader("Upload Brand avatar", type=["png", "jpg", "jpeg"], key="tiktok_avatar_upload")
                if profile_file is not None:
                    try:
                        avatar_bytes = profile_file.getvalue()
                        raw_avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
                        min_edge = min(raw_avatar.size)
                        left_crop = (raw_avatar.width - min_edge) // 2
                        top_crop = (raw_avatar.height - min_edge) // 2
                        raw_avatar = raw_avatar.crop((left_crop, top_crop, left_crop + min_edge, top_crop + min_edge))
                        raw_avatar = raw_avatar.resize((pfp_radius * 2, pfp_radius * 2), Image.Resampling.LANCZOS)
                        
                        mask_layer = Image.new("L", (pfp_radius * 2, pfp_radius * 2), 0)
                        mask_draw =ImageDraw.Draw(mask_layer)
                        mask_draw.ellipse([0, 0, pfp_radius * 2, pfp_radius * 2], fill=255)
                        raw_avatar.putalpha(mask_layer)
                        processed_layer.paste(raw_avatar, (icon_center_x - pfp_radius, pfp_y - pfp_radius), mask=raw_avatar)
                    except:
                        
                        tiktok_draw.ellipse([(icon_center_x - pfp_radius, pfp_y - pfp_radius), (icon_center_x + pfp_radius, pfp_y + pfp_radius)], fill="#64748B", outline="#FFFFFF", width=2)
                else:
                    
                    tiktok_draw.ellipse([(icon_center_x - pfp_radius, pfp_y - pfp_radius), (icon_center_x + pfp_radius, pfp_y + pfp_radius)], fill="#64748B", outline="#FFFFFF", width=2)
                for i, (img_name, count_label) in enumerate(tiktok_sidebar):
                    current_icon_y = base_start_y + (i * icon_spacing)
                    disc_radius = int(w * 0.045)
                    
                    icon_target_size = int(disc_radius * 1.1)
                    icon_img = get_cached_social_icon(img_name, icon_target_size)
                    if icon_img:
                        if i == 0:
                            r, g, b, a = icon_img.split()
                            icon_img = Image.merge("RGBA", (a.point(lambda p: 254), a.point(lambda p: 44), a.point(lambda p: 85), a))                          
                        processed_layer.paste(icon_img, (icon_center_x - (icon_target_size // 2), current_icon_y - (icon_target_size // 2)), mask=icon_img)
                     
                    try: lbl_w = tiktok_draw.textlength(count_label, font=ui_font)
                    except: lbl_w = len(count_label) * (ui_font_size * 0.55)
                    lbl_x = icon_center_x - int(lbl_w / 2)
                    lbl_y = current_icon_y + icon_target_size // 2 + 4                                 
                    tiktok_draw.text((lbl_x, lbl_y), count_label, fill="#FFFFFF", font=ui_font)
                handle_input = st.text_input("Enter Tiktok Handle", value=st.session_state.get("current_user", "demo_user"))
                active_handle = f"@{handle_input.lstrip('@')}"
                text_margin_x = int(w * 0.04)
                is_landscape = w > h
                raw_caption_string = final_processed_hook_text
                if is_landscape:
                    max_line_width = max(22, int(w * 0.05))
                else:
                    max_line_width = max(22, int(w * 0.032))
                
                wrapped_caption_lines = textwrap.wrap(raw_caption_string, width=max_line_width)
                total_caption_lines_count = len(wrapped_caption_lines)
                lower_base_y = active_footer_ceiling - int(ui_font_size * (total_caption_lines_count + 1.8)) - 40
               
                tiktok_draw.text((text_margin_x, lower_base_y), active_handle, fill="#FFFFFF", font=ImageFont.truetype("arial.ttf", int(ui_font_size * 1.3)))
                verified_icon_size = int(ui_font_size * 1.6)
                verified_icon = get_cached_social_icon("verified_icon (2).png", verified_icon_size)
                if verified_icon:
                    bbox = tiktok_draw.textbbox((0, 0), active_handle, font=ImageFont.truetype("arial.ttf", int(ui_font_size * 1.3)))
                    username_width = bbox[2] - bbox[0] 
                    badge_x = text_margin_x + username_width + 5
                    badge_y = lower_base_y + (ui_font_size - verified_icon.height) // 2
                    processed_layer.paste(verified_icon, (badge_x, badge_y), mask=verified_icon)
                
                current_caption_y = lower_base_y + int(ui_font_size * 1.70)
                for line_item in wrapped_caption_lines:
                    
                    tiktok_draw.text((text_margin_x, current_caption_y), line_item, fill="#FFFFFF", font=ImageFont.truetype("arial.ttf", int(ui_font_size * 1.2)))
                    current_caption_y += int(ui_font_size * 1.20)
                if niche == "Problem/Solution":
                    dynamic_audio = " Original sound - Ecom Growth Hacks"
                elif niche == "Impulse Buy Scarcity":
                    dynamic_audio = " Trending Sound - Viral Product Audio (Locked)"
                else:
                    dynamic_audio = " Special Promo - Store Clearance Track"
               
                music_y = current_caption_y + int(ui_font_size * 0.7)
                icon_x = text_margin_x
                icon_size = int(ui_font_size * 1.2)
                try:
                    audio_icon = Image.open("icon_music.png").convert("RGBA")
                    audio_icon = audio_icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                    processed_layer.paste(audio_icon, (icon_x, music_y - icon_size // 4), mask=audio_icon)
                    text_x = icon_x + icon_size + 20
                except Exception:
                    
                    text_x = text_margin_x
                tiktok_draw.text((text_x, music_y), dynamic_audio, fill=(255, 255, 255, 191), font=ui_font)
            
        if tab2:
            with tab2:
                st.markdown("### Registered System Accounts")
                st.write("Manage active users authorized to use this workstation instance.")
                for register_name in list(st.session_state.user_db.keys()):
                    col_usr, col_act = st.columns([3, 1])
                    with col_usr:
                        st.code(f"User: {register_name}")
                    with col_act:
                        if register_name == "demo_user":
                            st.write("System Lock")
                        else:
                            if st.button("Delete Account", key=f"del_{register_name}", type="secondary"):
                                del st.session_state.user_db[register_name]
                                save_to_local_database(st.session_state.user_db)
                                st.success(f"Remove Account: {register_name}")
                                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        with app_left_col:
            st.markdown(
                """
                <style>
                div[data-testid="stHorizontalBlock"] button[data-testid="stBaseButton-primary"] {
                    background: linear-gradient(135deg, #1E40AF, #2563EB) !important;
                    color: #FFFFFF !important;
                    border: none !important;
                    border-radius: 10px !important;
                    box-shadow: 0px 4px 10px rgba(37, 99, 235, 0.2) !important;
                    font-weight: 600 !important;
                    max-width: 220px !important;
                }
                div[data-testid="stHorizontalBlock"] button[data-testid="stBaseButton-primary"]:hover {
                    background: linear-gradient(135deg, #2563EB, #3B82F6) !important;
                    box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.4) !important;
                    color: blue !important;
                }
                    
                </style>
            """, unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("### LIVE AD PREVIEW")
            if "processed_layer" in locals() and processed_layer is not None:
                st.image(processed_layer, width="stretch", output_format="PNG")
            elif "adcraft_active_canvas" in st.session_state and st.session_state["ad-box_active_canvas"] is not None:
                st.image(st.session_state["ad-box_active_canvas"], width="stretch", output_format="PNG")         
            else:
                st.info("Upload your product to generate your ad canvas preview.")
            st.markdown("### EXPORT MEDIA")
            st.markdown('<div class="export-box-row">', unsafe_allow_html=True)
            
            sub_col_left, sub_col_right = st.columns([0.9, 1.1], gap="small")
            with sub_col_left:
                export_format_selection = st.selectbox(
                    "Format Output presets",
                    ["PNG (High-Res)", "JPEG (Compressed)"],
                    label_visibility="collapsed",
                    key="export_format_selector_widget"
                )
            with sub_col_right:               
                export_buffer = io.BytesIO()
                if uploaded_file is not None:
                    if "PNG" in export_format_selection:
                        processed_layer.save(export_buffer, format="PNG")
                        mime_string_type = "image/png"
                        file_extension_tag = "png"
                    else:        
                        processed_layer.convert("RGB").save(export_buffer, format="JPEG", quality=95)
                        mime_string_type = "image/jpeg"
                        file_extension_tag = "jpg"
                else:
                    mime_string_type = "image/png"
                    file_extension_tag = "png"
                st.download_button(
                    label=f"Save .{file_extension_tag.upper()} Asset",
                    data=export_buffer.getvalue(),
                    file_name=f"adcraft_output.{file_extension_tag}",
                    mime=mime_string_type,
                    type="primary"
                          
                )
           
                    
                 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
         
         
         
         
        
    
    
    

            

        
        
