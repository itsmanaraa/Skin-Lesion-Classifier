"""
Streamlit web application for skin lesion classification.
Provides a user-friendly interface for uploading images and viewing predictions.
"""
import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration - works for both local and Hugging Face Spaces
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Skin Lesion Classifier • AI Diagnostics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic purple theme
st.markdown("""
<style>
    /* Import futuristic font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Global theme */
    :root {
        --primary-purple: #8B5CF6;
        --secondary-purple: #6D28D9;
        --dark-purple: #4C1D95;
        --light-purple: #A78BFA;
        --accent-cyan: #06B6D4;
        --dark-bg: #0F0A1E;
        --card-bg: #1A1033;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0F0A1E 0%, #1A0B2E 50%, #16213E 100%);
    }
    
    /* Prevent layout shifts by forcing scrollbar */
    html {
        overflow-y: scroll;
    }
    
    /* Global reset for stability */
    * {
        animation: none !important;
        transition: none !important;
    }

    /* Headers - Solid color for stability */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: #A78BFA;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1rem;
        }
        .prediction-class {
            font-size: 2rem;
        }
    }
    
    .sub-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        color: #A78BFA;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Glassmorphism cards - Simplified for stability */
    .glass-card {
        background: rgba(26, 16, 51, 0.8);
        border-radius: 20px;
        border: 1px solid rgba(167, 139, 250, 0.2);
        padding: 2rem;
    }
    
    /* Prediction box - Simplified */
    .prediction-box {
        padding: 2.5rem;
        border-radius: 20px;
        background: #6D28D9;
        border: 2px solid #A78BFA;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .prediction-class {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    
    .prediction-confidence {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    .prediction-description {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        margin: 1rem 0;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Buttons - Removed transitions */
    .stButton>button {
        width: 100%;
        background: #6D28D9;
        color: white;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid #A78BFA;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        background: #8B5CF6;
        border-color: #EC4899;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0F0A1E;
        border-right: 1px solid rgba(167, 139, 250, 0.3);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: 'Orbitron', sans-serif;
        color: #A78BFA;
    }
    
    [data-testid="stSidebar"] p {
        font-family: 'Rajdhani', sans-serif;
        color: #D8B4FE;
    }
    
    /* Info boxes - Simplified */
    .info-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(167, 139, 250, 0.3);
        margin: 1rem 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 10px 10px 0 0;
        color: #A78BFA;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        border-color: #A78BFA;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(139, 92, 246, 0.1);
        border: 2px dashed #8B5CF6;
        border-radius: 15px;
        padding: 2rem;
    }
    
    /* Status indicators */
    .status-connected {
        color: #10B981;
        font-weight: 700;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .status-disconnected {
        color: #EF4444;
        font-weight: 700;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        background: rgba(139, 92, 246, 0.2);
        border-radius: 10px;
    }
    
    /* Subheaders */
    h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: #A78BFA !important;
    }
    
    /* Text colors */
    p, li, label {
        color: #D8B4FE;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(167, 139, 250, 0.3);
        border-radius: 10px;
    }
    
    /* Divider */
    hr {
        border-color: rgba(167, 139, 250, 0.3);
    }
</style>
""", unsafe_allow_html=True)


def check_api_health():
    """Check if the API is running and healthy."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_classes():
    """Get list of classes from API."""
    try:
        response = requests.get(f"{API_URL}/classes")
        if response.status_code == 200:
            return response.json()["classes"]
        return []
    except:
        return []


def predict_image(image_bytes):
    """Send image to API for prediction."""
    try:
        files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
        response = requests.post(f"{API_URL}/predict", files=files, timeout=30)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error: {response.json().get('detail', 'Unknown error')}"
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Please ensure the FastAPI server is running."
    except Exception as e:
        return None, f"Error: {str(e)}"


def main():
    # Header
    st.markdown('<div class="main-header">Skin Lesion Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Detection and Classification of Skin Lesions Using Deep Learning</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ABOUT")
        st.write("""
        This application uses a **ResNet18** model trained on the HAM10000 dataset 
        to classify skin lesions into 7 categories.
        """)
        
        st.header("HOW TO USE")
        st.write("""
        1. Upload a skin lesion image
        2. Wait for the prediction
        3. Review the results and confidence scores
        """)
        
        st.header("DISCLAIMER")
        st.warning("""
        This is a research tool and should **NOT** be used as a substitute for professional 
        medical diagnosis. Always consult with a qualified healthcare provider.
        """)
        
        # API Status
        st.header("API STATUS")
        if check_api_health():
            st.markdown('<p class="status-connected">CONNECTED</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-disconnected">DISCONNECTED</p>', unsafe_allow_html=True)
            st.info("Start the API with: `uvicorn api.app:app --reload`")
    
    # Main content
    tab1, tab2 = st.tabs(["CLASSIFY IMAGE", "CLASS INFORMATION"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Upload Image")
            uploaded_file = st.file_uploader(
                "Choose a skin lesion image",
                type=["jpg", "jpeg", "png"],
                help="Upload a clear image of the skin lesion"
            )
            
            if uploaded_file is not None:
                # Display uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", width=400)
                
                # Predict button
                if st.button("ANALYZE IMAGE", type="primary"):
                    with st.spinner("Analyzing image..."):
                        # Convert image to bytes
                        img_bytes = io.BytesIO()
                        # Ensure image is in RGB mode (handles RGBA, P, L, etc.)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        image.save(img_bytes, format='JPEG')
                        img_bytes.seek(0)
                        
                        # Get prediction
                        result, error = predict_image(img_bytes.getvalue())
                        
                        if error:
                            st.error(error)
                        else:
                            # Store result in session state
                            st.session_state['prediction_result'] = result
        
        with col2:
            st.subheader("Analysis Results")
            
            if 'prediction_result' in st.session_state:
                result = st.session_state['prediction_result']
                pred = result['prediction']
                
                # Display main prediction
                st.markdown(f"""
                <div class="prediction-box">
                    <div class="prediction-class">{pred['class'].upper()}</div>
                    <div class="prediction-description">{pred['description']}</div>
                    <div class="prediction-confidence">Confidence: {pred['percentage']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display all probabilities
                st.subheader("Confidence Scores")
                
                # Create DataFrame for plotting
                probs_data = result['all_probabilities']
                df = pd.DataFrame(probs_data)
                
                # Create enhanced bar chart with purple theme
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=df['confidence'],
                    y=df['class'],
                    orientation='h',
                    text=df['percentage'],
                    textposition='outside',
                    marker=dict(
                        color=df['confidence'],
                        colorscale=[
                            [0, '#6D28D9'],
                            [0.5, '#8B5CF6'],
                            [1, '#A78BFA']
                        ],
                        line=dict(color='#A78BFA', width=2)
                    ),
                    hovertemplate='<b>%{y}</b><br>Confidence: %{x:.2%}<extra></extra>'
                ))
                
                fig.update_layout(
                    title='Class Probabilities',
                    xaxis_title='Confidence',
                    yaxis_title='Class',
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(
                        family='Rajdhani',
                        size=14,
                        color='#A78BFA'
                    ),
                    xaxis=dict(
                        gridcolor='rgba(167, 139, 250, 0.2)',
                        showgrid=True
                    ),
                    yaxis=dict(
                        categoryorder='total ascending',
                        gridcolor='rgba(167, 139, 250, 0.2)'
                    ),
                    margin=dict(l=0, r=100, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed table
                with st.expander("DETAILED BREAKDOWN"):
                    display_df = df[['class', 'description', 'percentage']].copy()
                    display_df.columns = ['Class', 'Description', 'Confidence']
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("Upload an image and click 'ANALYZE IMAGE' to see results")
    
    with tab2:
        st.subheader("Skin Lesion Class Information")
        
        classes_info = [
            {
                "code": "AKIEC",
                "name": "Actinic Keratoses",
                "type": "Precancerous",
                "description": "Rough, scaly patches on the skin caused by sun damage. Can develop into skin cancer if untreated.",
                "severity": "MEDIUM RISK - Monitor Regularly"
            },
            {
                "code": "BCC",
                "name": "Basal Cell Carcinoma",
                "type": "Malignant",
                "description": "Most common type of skin cancer. Grows slowly and rarely spreads, but requires treatment.",
                "severity": "HIGH RISK - Immediate Attention"
            },
            {
                "code": "BKL",
                "name": "Benign Keratosis",
                "type": "Benign",
                "description": "Non-cancerous skin growths that appear with age. Generally harmless.",
                "severity": "LOW RISK - Benign"
            },
            {
                "code": "DF",
                "name": "Dermatofibroma",
                "type": "Benign",
                "description": "Firm, small bumps that typically appear on the legs. Non-cancerous and harmless.",
                "severity": "LOW RISK - Benign"
            },
            {
                "code": "MEL",
                "name": "Melanoma",
                "type": "Malignant",
                "description": "The most serious type of skin cancer. Can spread rapidly and requires immediate treatment.",
                "severity": "CRITICAL - Urgent Medical Attention"
            },
            {
                "code": "NV",
                "name": "Melanocytic Nevi",
                "type": "Benign",
                "description": "Common moles. Usually harmless but should be monitored for changes.",
                "severity": "LOW RISK - Monitor"
            },
            {
                "code": "VASC",
                "name": "Vascular Lesions",
                "type": "Benign",
                "description": "Lesions related to blood vessels, such as cherry angiomas. Usually benign.",
                "severity": "LOW RISK - Benign"
            }
        ]
        
        for cls in classes_info:
            with st.expander(f"**{cls['code']}** — {cls['name']}"):
                st.markdown(f"""
                **Type:** {cls['type']}  
                **Severity:** {cls['severity']}  
                **Description:** {cls['description']}
                """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #A78BFA; padding: 1rem; font-family: 'Rajdhani', sans-serif;">
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">Built with PyTorch • FastAPI • Streamlit</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Model: ResNet18 | Dataset: HAM10000 | Transfer Learning</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
