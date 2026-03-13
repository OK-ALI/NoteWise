"""
Gemini-powered Text Summarizer for NoteWise
Uses Google's Gemini AI for high-quality summarization
"""

import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiTextSummarizer:
    """
    Advanced text summarizer using Google's Gemini AI
    Provides superior summarization compared to local models
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize Gemini summarizer
        
        Args:
            api_key (str): Google AI API key (or set GEMINI_API_KEY env var)
            model_name (str): Gemini model to use (default: gemini-2.0-flash-exp)
        """
        self.model_name = model_name
        self.model = None
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            logger.warning("No Gemini API key provided. Please set GEMINI_API_KEY environment variable or pass api_key parameter.")
            self.available = False
            return
        
        try:
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name)
            self.available = True
            logger.info(f"Gemini {model_name} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.available = False
    
    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        return self.available
    
    def summarize(self, text: str, length: str = "medium", **kwargs) -> str:
        """
        Generate high-quality summary using Gemini AI
        
        Args:
            text (str): Input text to summarize
            length (str): Summary length ('short', 'medium', 'detailed')
            **kwargs: Additional parameters
            
        Returns:
            str: Generated summary
        """
        if not self.available:
            return "Gemini API is not available. Please check your API key."
        
        if not text or not text.strip():
            return "No text provided for summarization."
        
        try:
            # Create length-specific prompts
            length_instructions = self._get_length_instructions(length, text)
            
            # Construct the prompt
            prompt = f"""Please provide a {length} summary of the following text. {length_instructions}

Text to summarize:
{text}

Summary:"""
            
            # Generate with Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    temperature=0.3,  # Lower temperature for more focused summaries
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=self._get_max_tokens(length)
                )
            )
            
            if response.text:
                summary = response.text.strip()
                return self._postprocess_summary(summary)
            else:
                return "Failed to generate summary with Gemini."
                
        except Exception as e:
            logger.error(f"Gemini summarization failed: {str(e)}")
            return f"Error generating summary with Gemini: {str(e)}"
    
    def _get_length_instructions(self, length: str, text: str) -> str:
        """Get specific instructions based on desired length"""
        word_count = len(text.split())
        
        if length == "short":
            target_words = max(15, word_count // 15)
            return f"Keep it concise, approximately {target_words} words. Focus on the main points only."
        elif length == "detailed":
            target_words = max(80, word_count // 4)
            return f"Provide a comprehensive overview, approximately {target_words} words. Include key details and context."
        else:  # medium
            target_words = max(40, word_count // 8)
            return f"Provide a balanced summary, approximately {target_words} words. Include main points and important details."
    
    def _get_max_tokens(self, length: str) -> int:
        """Get maximum output tokens based on length"""
        token_limits = {
            'short': 100,
            'medium': 200,
            'detailed': 400
        }
        return token_limits.get(length, 200)
    
    def _postprocess_summary(self, summary: str) -> str:
        """Clean and improve the summary"""
        # Remove any markdown formatting
        summary = summary.replace('**', '').replace('*', '')
        
        # Remove any prompt echoing
        if summary.lower().startswith('summary:'):
            summary = summary[8:].strip()
        
        # Ensure proper sentence ending
        if summary and not summary.endswith('.'):
            summary += '.'
        
        # Remove extra whitespace
        summary = ' '.join(summary.split())
        
        return summary

    def generate_bullet_summary(self, text: str, num_points: int = 5) -> str:
        """
        Generate a bullet-point summary
        
        Args:
            text (str): Input text
            num_points (int): Number of bullet points
            
        Returns:
            str: Bullet-point summary
        """
        if not self.available:
            return "Gemini API is not available."
        
        prompt = f"""Create a bullet-point summary of the following text with exactly {num_points} key points. 
Format each point as a bullet point (•) and keep each point concise but informative.

Text:
{text}

Key Points:"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=300
                )
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "Failed to generate bullet summary."
                
        except Exception as e:
            logger.error(f"Bullet summary generation failed: {str(e)}")
            return f"Error: {str(e)}"

    def get_key_insights(self, text: str) -> str:
        """
        Extract key insights and takeaways from the text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Key insights
        """
        if not self.available:
            return "Gemini API is not available."
        
        prompt = f"""Analyze the following text and provide 3-5 key insights or takeaways. 
Focus on the most important concepts, implications, or actionable information.

Text:
{text}

Key Insights:"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,
                    max_output_tokens=250
                )
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "Failed to generate insights."
                
        except Exception as e:
            logger.error(f"Insights generation failed: {str(e)}")
            return f"Error: {str(e)}"
