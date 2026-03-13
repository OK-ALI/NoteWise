"""
NoteWise - Smart Study Assistant
Main entry point for the Streamlit application with Gemini AI integration
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app.dashboard import main as dashboard_main

def check_gemini_setup():
    """Check if Gemini API is properly configured"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key in ['your_gemini_api_key_here', 'REPLACE_WITH_YOUR_ACTUAL_GEMINI_API_KEY']:
        st.error("🔑 **Gemini API Key Required**")
        st.markdown("""
        To use NoteWise with full AI capabilities, you need to:
        1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Add it to your `.env` file as: `GEMINI_API_KEY=your_actual_key_here`
        3. Restart the application
        """)
        st.stop()
    return True

if __name__ == "__main__":
    # Configure Streamlit page
    st.set_page_config(
        page_title="NoteWise - Smart Study Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': """
            # NoteWise 2.0 🧠
            
            **Smart Study Assistant powered by Google Gemini AI**
            
            ### Features:
            - 🤖 **Gemini Vision**: Superior text extraction from images and handwritten notes
            - 📝 **Gemini Pro**: High-quality text summarization  
            - ❓ **Gemini Pro**: Intelligent question generation
            - 📄 **Multi-format**: Support for PDFs, PowerPoint presentations, images, and text files
            
            ### Version: 2.0.0
            Built with Streamlit and Google Generative AI
            """
        }
    )
    
    # Check Gemini setup before starting
    check_gemini_setup()
    
    # Run the main dashboard
    try:
        dashboard_main()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.markdown("💡 Try refreshing the page or check your API key configuration.")
