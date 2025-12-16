"""
Plant Disease Classification UI - Streamlit Interface Module
Handles the user interface and user interactions.
"""

import streamlit as st
from PIL import Image
from typing import List, Dict, Optional


class PlantDiseaseUI:
    """
    Streamlit UI class for the Plant Disease Classification application.
    
    This class handles all UI rendering and user interactions,
    separate from the model inference logic.
    """
    
    # Supported plants with emojis
    SUPPORTED_PLANTS = [
        "🍎 Apple", "🫐 Blueberry", "🍒 Cherry", "🌽 Corn",
        "🍇 Grape", "🍊 Orange", "🍑 Peach", "🫑 Pepper",
        "🥔 Potato", "🫐 Raspberry", "🫘 Soybean", "🎃 Squash",
        "🍓 Strawberry", "🍅 Tomato"
    ]
    
    # Prevention and Medication information for ALL 38 disease classes
    PREVENTION_AND_MEDICATION = {
        "Apple": {
            "Apple scab": {
                "prevention": [
                    "Remove and destroy fallen leaves in autumn",
                    "Prune trees to improve air circulation",
                    "Plant resistant apple varieties (Liberty, Freedom, Enterprise)",
                    "Avoid overhead irrigation"
                ],
                "medication": [
                    "Captan fungicide spray",
                    "Myclobutanil (Immunox)",
                    "Sulfur-based fungicides",
                    "Apply fungicide at bud break, repeat every 7-10 days"
                ]
            },
            "Black rot": {
                "prevention": [
                    "Remove mummified fruits and cankers",
                    "Prune dead or diseased branches",
                    "Maintain good tree hygiene",
                    "Ensure proper spacing between trees"
                ],
                "medication": [
                    "Captan or Mancozeb fungicides",
                    "Thiophanate-methyl",
                    "Apply during bloom through summer",
                    "Copper-based fungicides as preventive"
                ]
            },
            "Cedar apple rust": {
                "prevention": [
                    "Remove nearby juniper/cedar trees (alternate host)",
                    "Plant rust-resistant varieties (Redfree, Liberty)",
                    "Improve air circulation around trees",
                    "Scout for galls on junipers in early spring"
                ],
                "medication": [
                    "Myclobutanil fungicide",
                    "Triadimefon (Bayleton)",
                    "Apply at pink bud stage",
                    "Repeat every 7-10 days until petal fall"
                ]
            }
        },
        "Cherry (including sour)": {
            "Powdery mildew": {
                "prevention": [
                    "Ensure good air circulation",
                    "Avoid excessive nitrogen fertilization",
                    "Prune to open tree canopy",
                    "Plant resistant varieties when available"
                ],
                "medication": [
                    "Sulfur-based fungicides",
                    "Myclobutanil applications",
                    "Potassium bicarbonate sprays",
                    "Apply at first sign of white powdery growth"
                ]
            }
        },
        "Corn (maize)": {
            "Cercospora leaf spot Gray leaf spot": {
                "prevention": [
                    "Plant resistant hybrids",
                    "Rotate crops with non-host plants",
                    "Manage crop residue through tillage",
                    "Ensure adequate plant spacing"
                ],
                "medication": [
                    "Strobilurin fungicides (Quadris, Headline)",
                    "Triazole fungicides (Tilt, Propimax)",
                    "Apply at tasseling if threshold reached",
                    "Scout fields regularly for early detection"
                ]
            },
            "Common rust": {
                "prevention": [
                    "Plant resistant varieties",
                    "Early planting to avoid peak infection period",
                    "Monitor fields regularly",
                    "Avoid late planting in endemic areas"
                ],
                "medication": [
                    "Azoxystrobin fungicide",
                    "Propiconazole",
                    "Apply when pustules first appear on leaves",
                    "Treatment usually not economical unless severe"
                ]
            },
            "Northern Leaf Blight": {
                "prevention": [
                    "Use resistant hybrids (Ht1, Ht2, Ht3 genes)",
                    "Rotate with non-host crops",
                    "Till crop residue to reduce inoculum",
                    "Avoid continuous corn planting"
                ],
                "medication": [
                    "Strobilurin fungicides",
                    "Triazole fungicides",
                    "Apply at VT-R1 growth stage",
                    "Threshold: 50% of plants with lesions on third leaf"
                ]
            }
        },
        "Grape": {
            "Black rot": {
                "prevention": [
                    "Remove mummified berries and infected canes",
                    "Prune for good air circulation",
                    "Remove wild grapes nearby",
                    "Keep vineyard floor clean"
                ],
                "medication": [
                    "Myclobutanil fungicide",
                    "Mancozeb sprays",
                    "Captan applications",
                    "Apply from bud break to veraison"
                ]
            },
            "Esca (Black Measles)": {
                "prevention": [
                    "Avoid large pruning wounds",
                    "Protect pruning cuts with wound sealant",
                    "Remove and destroy infected vines",
                    "Practice balanced irrigation"
                ],
                "medication": [
                    "No effective chemical control available",
                    "Trunk surgery for mild cases",
                    "Sodium arsenite (where legally permitted)",
                    "Focus on prevention and vine replacement"
                ]
            },
            "Leaf blight (Isariopsis Leaf Spot)": {
                "prevention": [
                    "Ensure good air circulation",
                    "Avoid overhead irrigation",
                    "Remove infected leaves promptly",
                    "Maintain balanced nutrition"
                ],
                "medication": [
                    "Mancozeb fungicide",
                    "Copper-based sprays",
                    "Captan applications",
                    "Apply at first sign of infection"
                ]
            }
        },
        "Orange": {
            "Haunglongbing (Citrus greening)": {
                "prevention": [
                    "Control Asian citrus psyllid vectors",
                    "Use certified disease-free nursery stock",
                    "Remove infected trees promptly",
                    "Regular scouting for psyllids"
                ],
                "medication": [
                    "No cure available - prevention is key",
                    "Imidacloprid for psyllid control",
                    "Foliar nutrition to extend tree life",
                    "Remove and destroy infected trees"
                ]
            }
        },
        "Peach": {
            "Bacterial spot": {
                "prevention": [
                    "Plant resistant varieties (Redhaven, Biscoe)",
                    "Avoid overhead irrigation",
                    "Maintain proper tree spacing",
                    "Prune to improve air circulation"
                ],
                "medication": [
                    "Copper hydroxide sprays (dormant season)",
                    "Oxytetracycline (Mycoshield)",
                    "Apply copper at leaf fall and before bud break",
                    "Avoid copper after petal fall (phytotoxicity)"
                ]
            }
        },
        "Pepper, bell": {
            "Bacterial spot": {
                "prevention": [
                    "Use certified disease-free seeds",
                    "Hot water seed treatment (125°F for 30 min)",
                    "Rotate crops every 2-3 years",
                    "Avoid overhead irrigation"
                ],
                "medication": [
                    "Copper hydroxide sprays",
                    "Copper + Mancozeb combination",
                    "Acibenzolar-S-methyl (Actigard)",
                    "Apply before symptoms appear"
                ]
            }
        },
        "Potato": {
            "Early blight": {
                "prevention": [
                    "Use certified disease-free seed potatoes",
                    "Rotate crops every 3-4 years",
                    "Avoid overhead irrigation",
                    "Hill soil around plants"
                ],
                "medication": [
                    "Chlorothalonil sprays",
                    "Mancozeb fungicide",
                    "Azoxystrobin (Quadris)",
                    "Begin at first sign of disease"
                ]
            },
            "Late blight": {
                "prevention": [
                    "Plant resistant varieties",
                    "Destroy volunteer potatoes",
                    "Ensure good drainage",
                    "Monitor weather conditions (cool, wet)"
                ],
                "medication": [
                    "Metalaxyl-M + Mancozeb (Ridomil Gold MZ)",
                    "Cymoxanil fungicides",
                    "Fluazinam (Omega)",
                    "Apply preventively during wet weather"
                ]
            }
        },
        "Squash": {
            "Powdery mildew": {
                "prevention": [
                    "Plant resistant varieties",
                    "Ensure good air circulation",
                    "Avoid overcrowding plants",
                    "Water at base, not on leaves"
                ],
                "medication": [
                    "Sulfur-based fungicides",
                    "Potassium bicarbonate (Kaligreen)",
                    "Neem oil applications",
                    "Myclobutanil (Immunox)"
                ]
            }
        },
        "Strawberry": {
            "Leaf scorch": {
                "prevention": [
                    "Plant certified disease-free stock",
                    "Ensure good air circulation",
                    "Avoid overhead irrigation",
                    "Remove infected leaves promptly"
                ],
                "medication": [
                    "Copper-based fungicides",
                    "Captan sprays",
                    "Apply at first sign of symptoms",
                    "Renovate beds after harvest"
                ]
            }
        },
        "Tomato": {
            "Bacterial spot": {
                "prevention": [
                    "Use certified disease-free seeds",
                    "Rotate crops every 2-3 years",
                    "Avoid overhead watering",
                    "Remove infected plant debris"
                ],
                "medication": [
                    "Copper hydroxide sprays",
                    "Streptomycin (for severe cases)",
                    "Acibenzolar-S-methyl (Actigard)",
                    "Apply copper at first sign of disease"
                ]
            },
            "Early blight": {
                "prevention": [
                    "Mulch around plants to prevent soil splash",
                    "Water at base of plants",
                    "Remove lower leaves touching soil",
                    "Practice 3-year crop rotation"
                ],
                "medication": [
                    "Chlorothalonil (Daconil)",
                    "Mancozeb fungicide",
                    "Azoxystrobin (Quadris)",
                    "Apply preventively every 7-14 days"
                ]
            },
            "Late blight": {
                "prevention": [
                    "Plant resistant varieties",
                    "Ensure good air circulation",
                    "Avoid wetting foliage",
                    "Remove volunteer potato plants nearby"
                ],
                "medication": [
                    "Chlorothalonil preventive sprays",
                    "Mefenoxam + Mancozeb",
                    "Cymoxanil-based fungicides",
                    "Apply every 5-7 days during wet weather"
                ]
            },
            "Leaf Mold": {
                "prevention": [
                    "Improve greenhouse ventilation",
                    "Reduce humidity below 85%",
                    "Space plants adequately",
                    "Use resistant varieties (many available)"
                ],
                "medication": [
                    "Chlorothalonil sprays",
                    "Mancozeb applications",
                    "Improve air circulation first",
                    "Remove severely infected leaves"
                ]
            },
            "Septoria leaf spot": {
                "prevention": [
                    "Remove infected leaves promptly",
                    "Mulch to prevent soil splash",
                    "Avoid working with wet plants",
                    "Rotate crops annually"
                ],
                "medication": [
                    "Chlorothalonil fungicide",
                    "Copper-based sprays",
                    "Mancozeb",
                    "Begin treatment at first symptom"
                ]
            },
            "Spider mites Two-spotted spider mite": {
                "prevention": [
                    "Keep plants well-watered (mites prefer dry conditions)",
                    "Spray plants with water to dislodge mites",
                    "Introduce predatory mites (Phytoseiulus persimilis)",
                    "Avoid excessive nitrogen fertilization"
                ],
                "medication": [
                    "Insecticidal soap spray",
                    "Neem oil applications",
                    "Abamectin miticide (Avid)",
                    "Sulfur dusting (avoid in hot weather >90°F)"
                ]
            },
            "Target Spot": {
                "prevention": [
                    "Ensure good air circulation",
                    "Avoid overhead irrigation",
                    "Remove lower leaves and suckers",
                    "Practice crop rotation"
                ],
                "medication": [
                    "Chlorothalonil fungicide",
                    "Azoxystrobin (Quadris)",
                    "Mancozeb applications",
                    "Apply at first sign of infection"
                ]
            },
            "Tomato Yellow Leaf Curl Virus": {
                "prevention": [
                    "Control whitefly vectors aggressively",
                    "Use reflective mulches",
                    "Plant resistant varieties (Ty genes)",
                    "Remove infected plants immediately"
                ],
                "medication": [
                    "No direct cure - vector management only",
                    "Imidacloprid for whitefly control",
                    "Yellow sticky traps for monitoring",
                    "Remove and destroy infected plants"
                ]
            },
            "Tomato mosaic virus": {
                "prevention": [
                    "Use virus-free seeds and transplants",
                    "Disinfect tools with 10% bleach solution",
                    "Wash hands before handling plants",
                    "Control aphid vectors"
                ],
                "medication": [
                    "No chemical cure available",
                    "Remove and destroy infected plants",
                    "Plant resistant varieties (Tm-2 gene)",
                    "Do not smoke near tomato plants"
                ]
            }
        }
    }
    
    def __init__(self):
        """Initialize the UI with page configuration."""
        self._configure_page()
        self._inject_custom_css()
    
    def _configure_page(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="🌿 Plant Disease Classifier",
            page_icon="🌿",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def _inject_custom_css(self):
        """Inject custom CSS for premium, modern styling with glassmorphism and animations."""
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
            
            /* Global Styles */
            * { font-family: 'Poppins', sans-serif; }
            
            /* Hide Streamlit Branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar { width: 8px; height: 8px; }
            ::-webkit-scrollbar-track { background: rgba(255,255,255,0.1); border-radius: 10px; }
            ::-webkit-scrollbar-thumb { 
                background: linear-gradient(135deg, #10b981, #059669);
                border-radius: 10px;
            }
            
            /* Animated Background - Deep Dark with Animation */
            .stApp {
                background: linear-gradient(-45deg, #000000, #0a0f1a, #0d1f1a, #0a1510);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Main Header - Premium Glassmorphism */
            .main-header {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                padding: 3rem 2rem;
                border-radius: 30px;
                margin-bottom: 2rem;
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                position: relative;
                overflow: hidden;
            }
            
            .main-header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
                animation: rotate 20s linear infinite;
            }
            
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .main-header h1 {
                color: #ffffff;
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                text-shadow: 0 4px 30px rgba(16, 185, 129, 0.5);
                position: relative;
                z-index: 1;
                letter-spacing: -1px;
            }
            
            .main-header p {
                color: rgba(167, 243, 208, 0.9);
                font-size: 1.2rem;
                margin: 0;
                position: relative;
                z-index: 1;
                font-weight: 300;
            }
            
            /* Floating Leaf Icon */
            .leaf-icon {
                font-size: 4rem;
                animation: float 3s ease-in-out infinite;
                display: inline-block;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-10px) rotate(5deg); }
            }
            
            /* Glass Card Styling */
            .glass-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-radius: 24px;
                padding: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .glass-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 60px rgba(16, 185, 129, 0.2);
                border-color: rgba(16, 185, 129, 0.3);
            }
            
            /* Result Card - Creative Glassmorphism without solid box */
            .result-card {
                background: transparent;
                border-radius: 0;
                padding: 2rem 0;
                box-shadow: none;
                border: none;
                position: relative;
                overflow: visible;
            }
            
            .result-card::before {
                content: '';
                position: absolute;
                left: 0;
                bottom: 0;
                width: 100%;
                height: 2px;
                background: linear-gradient(90deg, transparent, #10b981, #3b82f6, #8b5cf6, transparent);
                animation: borderGlow 3s ease-in-out infinite;
            }
            
            @keyframes borderGlow {
                0%, 100% { opacity: 0.5; }
                50% { opacity: 1; }
            }
            
            /* Healthy Badge - Animated Glow */
            .healthy-badge {
                background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);
                color: white;
                padding: 1rem 2rem;
                border-radius: 50px;
                font-size: 1.3rem;
                font-weight: 700;
                display: inline-block;
                box-shadow: 0 10px 40px rgba(16, 185, 129, 0.4);
                animation: healthyPulse 2s ease-in-out infinite;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            
            @keyframes healthyPulse {
                0%, 100% { transform: scale(1); box-shadow: 0 10px 40px rgba(16, 185, 129, 0.4); }
                50% { transform: scale(1.05); box-shadow: 0 15px 60px rgba(16, 185, 129, 0.6); }
            }
            
            /* Disease Badge - Warning Style */
            .disease-badge {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%);
                color: white;
                padding: 1rem 2rem;
                border-radius: 50px;
                font-size: 1.3rem;
                font-weight: 700;
                display: inline-block;
                box-shadow: 0 10px 40px rgba(239, 68, 68, 0.4);
                animation: diseaseShake 0.5s ease-in-out;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            @keyframes diseaseShake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            /* Info Card - Modern Style */
            .info-card {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
                border-left: 4px solid;
                border-image: linear-gradient(180deg, #3b82f6, #8b5cf6) 1;
                padding: 1.5rem;
                border-radius: 0 16px 16px 0;
                margin: 1rem 0;
                backdrop-filter: blur(10px);
            }
            
            .info-card h4 { color: #ffffff; margin-bottom: 1rem; font-weight: 600; }
            .info-card li { color: rgba(255, 255, 255, 0.85); margin-bottom: 0.5rem; }
            
            /* Progress Bar - Gradient */
            .stProgress > div > div > div > div {
                background: linear-gradient(90deg, #10b981, #3b82f6, #8b5cf6);
                border-radius: 10px;
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #000000, #0a0f1a) !important;
            }
            
            [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] li, 
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] label {
                color: #ffffff !important;
            }
            
            /* File Uploader Styling - Universal color override */
            [data-testid="stFileUploader"] * {
                color: #ccffdd !important; /* Very Light Neon Green */
            }

            /* Browse Files Button - Explicitly reset to default */
            [data-testid="stFileUploader"] button,
            [data-testid="stFileUploader"] button * {
                color: #31333F !important; /* Default dark text color for button */
            }

            /* File Uploader Container */
            [data-testid="stFileUploader"] section {
                background: rgba(255, 255, 255, 0.05);
                border: 2px dashed rgba(16, 185, 129, 0.5);
                border-radius: 20px;
                padding: 1.5rem;
                transition: all 0.3s ease;
            }

            [data-testid="stFileUploader"] section:hover {
                border-color: #10b981;
                background: rgba(16, 185, 129, 0.1);
                box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
            }
            

            
            /* Expander Styling */
            .streamlit-expanderHeader {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .streamlit-expanderContent {
                background: rgba(255, 255, 255, 0.03);
                border-radius: 0 0 12px 12px;
            }
            
            /* Text Colors */
            .stMarkdown p, .stMarkdown li, .stMarkdown span, .stText,
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }
            
            strong, b { color: #10b981 !important; }
            
            /* Success/Warning/Error Messages */
            .stSuccess {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.2));
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 12px;
            }
            
            .stWarning {
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.2));
                border: 1px solid rgba(245, 158, 11, 0.3);
                border-radius: 12px;
            }
            
            .stError {
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.2));
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 12px;
            }
            
            /* Celebration Card */
            .celebration-card {
                background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);
                padding: 2.5rem;
                border-radius: 30px;
                text-align: center;
                color: white;
                box-shadow: 0 20px 60px rgba(16, 185, 129, 0.4);
                position: relative;
                overflow: hidden;
            }
            
            .celebration-card::after {
                content: '🎉';
                position: absolute;
                font-size: 100px;
                opacity: 0.1;
                top: -20px;
                right: -20px;
                animation: celebrateSpin 10s linear infinite;
            }
            
            @keyframes celebrateSpin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            /* Treatment Card */
            .treatment-card {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            }
            
            .prevention-header {
                background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                padding: 1rem 1.5rem;
                border-radius: 15px;
                color: white;
                margin-bottom: 1rem;
                box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
            }
            
            .medication-header {
                background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
                padding: 1rem 1.5rem;
                border-radius: 15px;
                color: white;
                margin-bottom: 1rem;
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
            }
            
            /* Metric Cards */
            .metric-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 1.5rem;
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
            }
            
            .metric-card:hover {
                transform: scale(1.05);
                border-color: rgba(16, 185, 129, 0.5);
            }
            
            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #10b981, #3b82f6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            /* Image Container */
            .image-container {
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                border: 3px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Custom Footer */
            .custom-footer {
                text-align: center;
                padding: 3rem 2rem;
                color: rgba(255, 255, 255, 0.6);
                margin-top: 2rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Animated Dots Background */
            .dots-bg {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                pointer-events: none;
                z-index: -1;
                background-image: radial-gradient(rgba(16, 185, 129, 0.15) 1px, transparent 1px);
                background-size: 50px 50px;
            }
        </style>
        """, unsafe_allow_html=True)
    
    
    def render_header(self):
        """Render the main header section with animated elements."""
        st.markdown("""
        <div class="main-header">
            <div class="leaf-icon">🌿</div>
            <h1>Plant Disease Classifier</h1>
            <p>🔬 AI-Powered Plant Health Analysis • 98.55% Accuracy • 38 Disease Classes</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self, training_info: Dict, version_info: Optional[str] = None):
        """
        Render the sidebar with app info and training details.
        
        Args:
            training_info: Dictionary with training configuration
            version_info: Optional version string from version.txt
        """
        with st.sidebar:
            st.markdown("### 🌿 About This App")
            st.markdown("""
            This application uses a **deep learning model** trained on the 
            **Plant Village dataset** to identify plant diseases from leaf images.
            """)
            
            st.markdown("---")
            
            # Training Conditions Section
            st.markdown("### ⚙️ Training Conditions")
            
            with st.expander("📊 Model Architecture", expanded=True):
                st.markdown(f"""
                **Base Model:** {training_info.get('architecture', 'EfficientNetB3')} ({training_info.get('pretrained_weights', 'ImageNet')} pretrained)
                
                **Custom Layers:**
                ```
                EfficientNetB3 (frozen weights)
                └── BatchNormalization (axis=-1, momentum=0.99)
                    └── Dense(256, activation='relu')
                        ├── L2 regularization: 0.016
                        ├── L1 activity regularization: 0.006
                        └── L1 bias regularization: 0.006
                    └── Dropout(rate=0.45, seed=123)
                        └── Dense(38, activation='softmax')
                ```
                """)
            
            with st.expander("🎯 Training Parameters"):
                st.markdown(f"""
                | Parameter | Value |
                |-----------|-------|
                | **Optimizer** | {training_info.get('optimizer', 'Adamax')} |
                | **Learning Rate** | {training_info.get('learning_rate', 0.001)} |
                | **Loss Function** | {training_info.get('loss_function', 'Categorical Crossentropy')} |
                | **Input Size** | {training_info.get('input_size', '224 × 224 × 3')} |
                | **Classes** | {training_info.get('num_classes', 38)} |
                """)
            
            with st.expander("🔄 Data Augmentation"):
                st.markdown("""
                **Training:**
                - Horizontal Flip: ✅ Enabled
                - Shuffle: ✅ Enabled
                
                **Validation/Test:**
                - No augmentation applied
                - Test shuffle: ❌ Disabled
                
                **Image Processing:**
                - Color Mode: RGB
                - Target Size: 224 × 224
                - Preprocessing: Identity (no scaling)
                """)
            
            # Version Information
            if version_info:
                st.markdown("### 📦 Version Information")
                st.code(version_info, language="text")
            
            st.markdown("---")
            
            st.markdown("### 🌱 Supported Plants")
            for plant in self.SUPPORTED_PLANTS:
                st.markdown(f"- {plant}")
    
    def render_upload_section(self) -> Optional[Image.Image]:
        """
        Render the image upload section.
        
        Returns:
            PIL Image if uploaded, None otherwise
        """
        st.markdown("### 📤 Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose a leaf image...",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of a plant leaf for disease detection"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            return image
        
        return None
    
    def render_results(self, predictions: List[Dict]):
        """
        Render classification results.
        
        Args:
            predictions: List of prediction dictionaries from classifier
        """
        st.markdown("### 🔬 Analysis Results")
        
        if not predictions:
            st.warning("No predictions available")
            return
        
        # Top prediction
        top = predictions[0]
        
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # Plant name
        st.markdown(f"**Plant:** {top['plant_name']}")
        
        # Health status badge
        if top['is_healthy']:
            st.markdown('<span class="healthy-badge">✅ Healthy</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="disease-badge">⚠️ {top["condition"]}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Confidence
        st.markdown("**Confidence Level:**")
        confidence = top['confidence_percent']
        
        if confidence >= 80:
            st.success(f"🎯 {confidence:.1f}% confident")
        elif confidence >= 50:
            st.warning(f"🎯 {confidence:.1f}% confident")
        else:
            st.error(f"🎯 {confidence:.1f}% confident")
        
        st.progress(confidence / 100)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Top 5 predictions
        st.markdown("### 📊 Top 5 Predictions")
        
        for pred in predictions:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{pred['plant_name']}** - {pred['condition']}")
            with col_b:
                st.markdown(f"`{pred['confidence_percent']:.1f}%`")
            
            st.progress(pred['confidence_percent'] / 100)
    
    def render_placeholder(self):
        """Render placeholder when no image is uploaded."""
        st.info("👆 Upload an image to see the analysis results")
        
        st.markdown("""
        <div class="info-card">
            <h4>📝 Tips for best results:</h4>
            <ul>
                <li>Use clear, well-lit images</li>
                <li>Focus on a single leaf</li>
                <li>Avoid blurry or dark images</li>
                <li>Capture the affected area clearly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def render_prevention_and_medication(self, prediction: Dict = None):
        """
        Render prevention and medication for the specific detected disease.
        If healthy, show creative care tips and fun facts.
        
        Args:
            prediction: The top prediction dictionary from classifier
        """
        if prediction is None:
            return
        
        st.markdown("---")
        
        if prediction['is_healthy']:
            self._render_healthy_plant_info(prediction['plant_name'])
        else:
            self._render_disease_treatment(prediction['plant_name'], prediction['condition'])
    
    def _render_healthy_plant_info(self, plant_name: str):
        """Render creative content for healthy plants."""
        st.markdown("### 🎉 Great News! Your Plant is Healthy!")
        
        # Fun facts and care tips for healthy plants
        healthy_tips = {
            "Apple": {
                "emoji": "🍎",
                "fun_fact": "A single apple tree can produce up to 400 apples per season!",
                "care_tips": [
                    "Water deeply once a week during dry periods",
                    "Prune in late winter for better fruit production",
                    "Apply balanced fertilizer in early spring",
                    "Mulch around the base to retain moisture"
                ],
                "message": "Your apple tree is thriving! Keep up the great care."
            },
            "Tomato": {
                "emoji": "🍅",
                "fun_fact": "Tomatoes are technically a fruit, and there are over 10,000 varieties worldwide!",
                "care_tips": [
                    "Water consistently - tomatoes love 1-2 inches per week",
                    "Stake or cage plants for better air circulation",
                    "Remove suckers for larger fruits",
                    "Add calcium to prevent blossom end rot"
                ],
                "message": "Your tomato plant looks fantastic! Expect a bountiful harvest."
            },
            "Potato": {
                "emoji": "🥔",
                "fun_fact": "Potatoes were the first vegetable grown in space!",
                "care_tips": [
                    "Hill soil around plants as they grow",
                    "Water evenly to prevent scab",
                    "Stop watering 2 weeks before harvest",
                    "Store in cool, dark place after harvesting"
                ],
                "message": "Your potato plants are in excellent condition!"
            },
            "Grape": {
                "emoji": "🍇",
                "fun_fact": "A single grapevine can produce enough grapes for 5 bottles of wine!",
                "care_tips": [
                    "Prune heavily in late winter",
                    "Train vines on trellises for best production",
                    "Thin grape clusters for larger berries",
                    "Water deeply but infrequently"
                ],
                "message": "Your grapevine is healthy and ready to flourish!"
            },
            "Corn (maize)": {
                "emoji": "🌽",
                "fun_fact": "Corn is grown on every continent except Antarctica!",
                "care_tips": [
                    "Plant in blocks for better pollination",
                    "Water 1-2 inches per week",
                    "Side-dress with nitrogen when knee-high",
                    "Harvest when silks turn brown"
                ],
                "message": "Your corn is growing strong and healthy!"
            },
            "Pepper, bell": {
                "emoji": "🫑",
                "fun_fact": "Bell peppers have more vitamin C than oranges!",
                "care_tips": [
                    "Provide consistent moisture",
                    "Use stakes to support heavy fruit load",
                    "Mulch to keep roots cool",
                    "Harvest regularly to encourage more fruit"
                ],
                "message": "Your pepper plants are in perfect health!"
            },
            "Cherry (including sour)": {
                "emoji": "🍒",
                "fun_fact": "Cherry blossoms in Japan symbolize the fragility of life!",
                "care_tips": [
                    "Protect blossoms from late frost",
                    "Net trees to protect from birds",
                    "Prune after fruiting",
                    "Water deeply during dry spells"
                ],
                "message": "Your cherry tree is healthy and beautiful!"
            },
            "Strawberry": {
                "emoji": "🍓",
                "fun_fact": "Strawberries are the only fruit with seeds on the outside!",
                "care_tips": [
                    "Mulch with straw to prevent fruit rot",
                    "Remove runners for larger berries",
                    "Water in the morning to prevent disease",
                    "Renovate beds after 3 years"
                ],
                "message": "Your strawberry plants are thriving!"
            },
            "Blueberry": {
                "emoji": "🫐",
                "fun_fact": "Blueberries are one of the few fruits native to North America!",
                "care_tips": [
                    "Maintain acidic soil pH (4.5-5.5)",
                    "Mulch with pine bark or sawdust",
                    "Water 1-2 inches per week",
                    "Prune old canes annually"
                ],
                "message": "Your blueberry bush is thriving beautifully!"
            },
            "Orange": {
                "emoji": "🍊",
                "fun_fact": "Orange trees can live and produce fruit for over 100 years!",
                "care_tips": [
                    "Water deeply but allow soil to dry between watering",
                    "Fertilize with citrus-specific fertilizer",
                    "Protect from frost in winter",
                    "Prune to maintain shape and airflow"
                ],
                "message": "Your citrus tree is in excellent health!"
            },
            "Peach": {
                "emoji": "🍑",
                "fun_fact": "Peaches are related to almonds and are sometimes called 'Persian apples'!",
                "care_tips": [
                    "Prune heavily in late winter",
                    "Thin fruits for larger peaches",
                    "Apply dormant spray in winter",
                    "Water deeply during fruit development"
                ],
                "message": "Your peach tree looks wonderful!"
            },
            "Raspberry": {
                "emoji": "🫐",
                "fun_fact": "Raspberries are part of the rose family and each berry has 100-120 seeds!",
                "care_tips": [
                    "Provide support with trellises",
                    "Prune old canes after fruiting",
                    "Mulch to keep roots cool",
                    "Water consistently especially during fruiting"
                ],
                "message": "Your raspberry plants are flourishing!"
            },
            "Soybean": {
                "emoji": "🫘",
                "fun_fact": "Soybeans fix nitrogen from the air, improving soil fertility!",
                "care_tips": [
                    "Plant after soil warms to 60°F",
                    "Inoculate seeds for nitrogen fixation",
                    "Scout regularly for pests",
                    "Harvest when leaves drop and pods rattle"
                ],
                "message": "Your soybean crop is growing strong!"
            }
        }
        
        # Get tips for this plant or use default
        plant_key = plant_name.strip()
        tips = healthy_tips.get(plant_key, {
            "emoji": "🌿",
            "fun_fact": "Healthy plants can live for decades with proper care!",
            "care_tips": [
                "Water appropriately for the species",
                "Ensure proper sunlight exposure",
                "Use quality soil with good drainage",
                "Monitor regularly for early signs of stress"
            ],
            "message": "Your plant is in excellent health! Keep nurturing it."
        })
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        padding: 2rem; border-radius: 20px; text-align: center; color: white;">
                <h1 style="font-size: 4rem; margin: 0;">{tips['emoji']}</h1>
                <h3 style="margin: 0.5rem 0;">Congratulations!</h3>
                <p style="margin: 0; opacity: 0.9;">{tips['message']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**💡 Fun Fact:**")
            st.info(tips['fun_fact'])
        
        with col2:
            st.markdown("**🌱 Care Tips to Maintain Health:**")
            for tip in tips['care_tips']:
                st.markdown(f"✅ {tip}")
            
            st.markdown("---")
            st.markdown("**🌟 Keep Your Plant Healthy:**")
            st.markdown("""
            - Continue regular monitoring
            - Maintain consistent watering schedule  
            - Watch for any changes in leaf color
            - Enjoy your thriving plant! 🎊
            """)
    
    def _render_disease_treatment(self, plant_name: str, condition: str):
        """Render prevention and medication for the specific detected disease."""
        st.markdown(f"### 💊 Treatment for {condition}")
        st.markdown(f"*Recommended prevention and treatment for your {plant_name}*")
        
        # Clean condition name for matching
        condition_clean = condition.strip()
        
        # Find matching disease info
        disease_info = None
        for plant_key, diseases in self.PREVENTION_AND_MEDICATION.items():
            # Check if plant name matches (remove emoji for comparison)
            plant_clean = plant_key.replace("🍎", "").replace("🍅", "").replace("🥔", "").replace("🍇", "").replace("🌽", "").replace("🫑", "").strip()
            if plant_clean.lower() in plant_name.lower() or plant_name.lower() in plant_clean.lower():
                for disease_name, info in diseases.items():
                    if disease_name.lower() in condition_clean.lower() or condition_clean.lower() in disease_name.lower():
                        disease_info = info
                        break
            if disease_info:
                break
        
        if disease_info:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
                            padding: 1rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
                    <h4 style="margin: 0;">🛡️ Prevention</h4>
                </div>
                """, unsafe_allow_html=True)
                for tip in disease_info.get("prevention", []):
                    st.markdown(f"• {tip}")
            
            with col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); 
                            padding: 1rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
                    <h4 style="margin: 0;">💉 Treatment</h4>
                </div>
                """, unsafe_allow_html=True)
                for med in disease_info.get("medication", []):
                    st.markdown(f"• {med}")
            
            st.markdown("---")
            st.warning("⚠️ **Disclaimer:** Always follow product labels and local regulations when applying treatments. Consult an agricultural expert for severe cases.")
        else:
            st.info(f"Detailed treatment information for '{condition}' is being added. Please consult a local agricultural expert for specific recommendations.")
    
    def render_footer(self):
        """Render the footer section with modern styling."""
        st.markdown("""
        <div class="custom-footer">
            <p style="font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem;">
                🌿 <span style="background: linear-gradient(135deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Plant Disease Classifier</span>
            </p>
            <p style="font-size: 0.9rem; opacity: 0.8;">
                Powered by <strong>EfficientNetB3</strong> Deep Learning • 98.55% Accuracy • 38 Disease Classes
            </p>
            <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 1rem;">
                🔬 TensorFlow • 🐍 Python • 🎨 Streamlit • 🐳 Docker
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_error(self, message: str):
        """Render an error message."""
        st.error(f"❌ {message}")
