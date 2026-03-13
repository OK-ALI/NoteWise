"""
Gemini Vision-based Text Extractor for NoteWise
Uses Google's Gemini Pro Vision for intelligent text extraction from images and documents
"""

import os
import base64
import tempfile
from typing import Optional, Dict, Any
from PIL import Image
import pdfplumber
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class GeminiExtractor:
    """
    Text extractor using Gemini Pro Vision for superior text recognition
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini extractor
        
        Args:
            api_key (str, optional): Gemini API key. If not provided, will use environment variable
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key or self.api_key == 'your_gemini_api_key_here':
            raise ValueError("Valid Gemini API key is required. Set GEMINI_API_KEY environment variable.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the vision model
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self._test_connection()
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini model: {str(e)}")
    
    def _test_connection(self) -> bool:
        """Test if Gemini API is working"""
        try:
            # Simple test with text-only prompt
            response = self.model.generate_content("Hello")
            return True
        except Exception as e:
            raise Exception(f"Gemini API test failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Gemini extraction is available"""
        try:
            return self.api_key and self.model is not None
        except:
            return False
    
    def extract_text(self, file_path: str, extraction_type: str = "comprehensive") -> str:
        """
        Extract text from image, PDF, or text file using Gemini Vision
        
        Args:
            file_path (str): Path to the file
            extraction_type (str): Type of extraction ('comprehensive', 'structured', 'handwritten')
            
        Returns:
            str: Extracted text
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(file_path, extraction_type)
        elif file_extension == '.txt':
            return self._extract_from_text(file_path)
        elif file_extension in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']:
            return self._extract_from_image(file_path, extraction_type)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_text(self, text_path: str) -> str:
        """Extract text from text file"""
        try:
            with open(text_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    def _extract_from_pdf(self, pdf_path: str, extraction_type: str = "comprehensive") -> str:
        """
        Extract text from PDF using Gemini Vision for image-based pages
        """
        try:
            extracted_text = ""
            
            # First, try traditional text extraction
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        extracted_text += f"--- Page {page_num} ---\n{page_text}\n\n"
            
            # If we got good text extraction, return it
            if extracted_text.strip():
                return extracted_text.strip()
            
            # If no text or minimal text, use Gemini Vision on PDF pages
            print("No readable text found in PDF. Using Gemini Vision for image-based extraction...")
            return self._extract_pdf_with_vision(pdf_path, extraction_type)
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def _extract_pdf_with_vision(self, pdf_path: str, extraction_type: str) -> str:
        """
        Convert PDF pages to images and extract text using Gemini Vision
        """
        try:
            # For this implementation, we'll suggest using pdf2image library
            # For now, return a helpful message
            return """
            PDF appears to contain images or scanned content. 
            For best results with image-based PDFs, please:
            1. Convert PDF pages to images first (using pdf2image library)
            2. Upload the images individually for Gemini Vision extraction
            
            Alternative: Use the image upload feature in the dashboard after converting PDF to images.
            """
        except Exception as e:
            raise Exception(f"Error processing PDF with vision: {str(e)}")
    
    def _extract_from_image(self, image_path: str, extraction_type: str = "comprehensive") -> str:
        """
        Extract text from image using Gemini Vision
        """
        try:
            # Load and prepare the image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create appropriate prompt based on extraction type
            prompt = self._get_extraction_prompt(extraction_type)
            
            # Use Gemini Vision to extract text
            response = self.model.generate_content(
                [prompt, image],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "No text could be extracted from the image."
                
        except Exception as e:
            raise Exception(f"Error extracting text from image with Gemini: {str(e)}")
    
    def _get_extraction_prompt(self, extraction_type: str) -> str:
        """
        Get appropriate prompt for different extraction types
        """
        prompts = {
            "comprehensive": """
                Please extract ALL text from this image with high accuracy. Include:
                - All readable text, preserving original formatting where possible
                - Mathematical equations, formulas, and symbols
                - Headers, subheaders, bullet points, and numbered lists
                - Table contents if present
                - Handwritten notes if any
                - Any other textual content
                
                Maintain the logical structure and order of the content. If you see any unclear text, 
                make your best interpretation and indicate uncertainty with [unclear: possible_text].
            """,
            
            "structured": """
                Extract text from this image and organize it in a clear, structured format:
                - Use headers and subheaders appropriately
                - Maintain bullet points and numbering
                - Preserve tables in a readable format
                - Group related content together
                - Remove unnecessary whitespace but keep logical spacing
                
                Focus on creating clean, well-organized output suitable for study notes.
            """,
            
            "handwritten": """
                This image contains handwritten text. Please extract it with special attention to:
                - Careful interpretation of handwriting styles
                - Context clues to resolve ambiguous characters
                - Mathematical notation and symbols
                - Diagrams or sketches with labels
                - Cross-outs or corrections
                
                If any text is unclear, indicate with [unclear: best_guess]. 
                Focus on accuracy over completeness for handwritten content.
            """
        }
        
        return prompts.get(extraction_type, prompts["comprehensive"])
    
    def extract_with_analysis(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text and provide additional analysis
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            Dict: Contains extracted text, content type, and analysis
        """
        try:
            # First extract the text
            extracted_text = self.extract_text(file_path)
            
            # Then analyze the content
            analysis_prompt = """
            Analyze this extracted text and provide:
            1. Content type (lecture notes, textbook, handwritten notes, etc.)
            2. Main topics covered
            3. Difficulty level (beginner, intermediate, advanced)
            4. Key concepts or terms
            5. Any special formatting or structure noted
            
            Format your response as:
            Content Type: [type]
            Main Topics: [list of topics]
            Difficulty: [level]
            Key Concepts: [list of concepts]
            Structure Notes: [observations about formatting/structure]
            """
            
            analysis_response = self.model.generate_content(
                f"{analysis_prompt}\n\nText to analyze:\n{extracted_text[:2000]}..."  # Limit for analysis
            )
            
            return {
                "extracted_text": extracted_text,
                "analysis": analysis_response.text if analysis_response.text else "Analysis not available",
                "word_count": len(extracted_text.split()),
                "character_count": len(extracted_text),
                "file_path": file_path
            }
            
        except Exception as e:
            return {
                "extracted_text": "",
                "analysis": f"Error during analysis: {str(e)}",
                "word_count": 0,
                "character_count": 0,
                "file_path": file_path,
                "error": str(e)
            }
    
    def batch_extract(self, file_paths: list, extraction_type: str = "comprehensive") -> Dict[str, str]:
        """
        Extract text from multiple files
        
        Args:
            file_paths (list): List of file paths
            extraction_type (str): Type of extraction to use
            
        Returns:
            Dict: Mapping of file_path to extracted_text
        """
        results = {}
        
        for file_path in file_paths:
            try:
                results[file_path] = self.extract_text(file_path, extraction_type)
            except Exception as e:
                results[file_path] = f"Error extracting from {file_path}: {str(e)}"
        
        return results
