"""
Gemini-powered Question Generator for NoteWise
Uses Google's Gemini AI for intelligent question generation
"""

import os
import logging
import json
import random
from typing import List, Dict, Any, Optional
import google.generativeai as genai

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiQuestionGenerator:
    """
    Advanced question generator using Google's Gemini AI
    Generates high-quality MCQs, True/False, and short answer questions
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize Gemini question generator
        
        Args:
            api_key (str): Google AI API key (or set GEMINI_API_KEY env var)
            model_name (str): Gemini model to use (default: gemini-2.0-flash-exp)
        """
        self.model_name = model_name
        self.model = None
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            logger.warning("No Gemini API key provided. Please set GEMINI_API_KEY environment variable.")
            self.available = False
            return
        
        try:
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name)
            self.available = True
            logger.info(f"Gemini Question Generator {model_name} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.available = False
    
    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        return self.available
    
    def generate_questions(self, text: str, question_types: List[str], count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate high-quality questions from text using Gemini AI
        
        Args:
            text (str): Input text
            question_types (List[str]): Types of questions to generate
            count (int): Total number of questions to generate per type
            
        Returns:
            List[Dict]: Generated questions organized by type (MCQ first, then Short Answer, then True/False)
        """
        if not self.available:
            return [{"error": "Gemini API is not available. Please check your API key."}]
        
        if not text or not text.strip():
            return [{"error": "No text provided for question generation."}]
        
        questions = []
        
        try:
            # Define the order of question types for consistent organization
            type_order = ["multiple choice", "short answer", "true/false"]
            
            # Generate questions in the specified order for better organization
            for ordered_type in type_order:
                for question_type in question_types:
                    if question_type.lower() in ["multiple choice", "mcq"] and ordered_type == "multiple choice":
                        mcq_questions = self._generate_mcq_questions(text, count)
                        if mcq_questions:
                            questions.extend(mcq_questions)
                    elif question_type.lower() in ["short answer", "short"] and ordered_type == "short answer":
                        short_questions = self._generate_short_answer_questions(text, count)
                        if short_questions:
                            questions.extend(short_questions)
                    elif question_type.lower() in ["true/false", "true false", "tf"] and ordered_type == "true/false":
                        tf_questions = self._generate_true_false_questions(text, count)
                        if tf_questions:
                            questions.extend(tf_questions)
            
            # No shuffling - keep questions organized by type
            return questions if questions else [{"error": "Could not generate questions from the provided text."}]
            
        except Exception as e:
            logger.error(f"Gemini question generation failed: {str(e)}")
            return [{"error": f"Error generating questions: {str(e)}"}]
    
    def _generate_mcq_questions(self, text: str, count: int) -> List[Dict[str, Any]]:
        """Generate multiple choice questions using Gemini"""
        prompt = f"""Based on the following text, create {count} high-quality multiple choice questions. 

IMPORTANT: Respond with ONLY a JSON array, no other text.

Format your response as a JSON array with this exact structure:
[
  {{
    "question": "Question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "B",
    "explanation": "Explanation text"
  }}
]

Requirements:
- Make questions specific and detailed
- Ensure distractors are plausible but clearly incorrect
- Provide clear explanations
- Use only information from the given text

Text:
{text}"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=2000,
                    top_p=0.8
                )
            )
            
            if response.text:
                # Clean the response text
                response_text = response.text.strip()
                
                # Remove any markdown formatting
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                try:
                    questions_data = json.loads(response_text)
                    questions = []
                    
                    for q_data in questions_data:
                        if isinstance(q_data, dict) and "question" in q_data and "options" in q_data:
                            # Convert to our format
                            correct_letter = q_data.get("correct_answer", "A")
                            correct_index = ord(correct_letter.upper()) - ord('A')
                            
                            questions.append({
                                "type": "Multiple Choice",
                                "question": q_data["question"],
                                "options": q_data["options"],
                                "answer": q_data["options"][correct_index] if correct_index < len(q_data["options"]) else q_data["options"][0],
                                "correct_index": correct_index,
                                "explanation": q_data.get("explanation", "Based on the provided text.")
                            })
                    
                    return questions
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing failed for MCQ: {str(e)}")
                    logger.error(f"Response text: {response_text}")
                    return self._fallback_mcq_generation(text, count)
            
            return []
            
        except Exception as e:
            logger.error(f"MCQ generation failed: {str(e)}")
            return []
    
    def _generate_true_false_questions(self, text: str, count: int) -> List[Dict[str, Any]]:
        """Generate true/false questions using Gemini"""
        prompt = f"""Based on the following text, create {count} true/false questions.

IMPORTANT: Respond with ONLY a JSON array, no other text.

Format as JSON array:
[
  {{
    "statement": "Statement to evaluate",
    "answer": "True",
    "explanation": "Explanation"
  }}
]

Requirements:
- Create clear statements that can be definitively judged as true or false
- Use only information from the given text
- Provide clear explanations for the answers
- Mix both true and false statements

Text:
{text}"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=1500,
                    top_p=0.8
                )
            )
            
            if response.text:
                # Clean the response text
                response_text = response.text.strip()
                
                # Remove any markdown formatting
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                try:
                    questions_data = json.loads(response_text)
                    questions = []
                    
                    for q_data in questions_data:
                        if isinstance(q_data, dict) and "statement" in q_data:
                            questions.append({
                                "type": "True/False",
                                "question": f"True or False: {q_data['statement']}",
                                "answer": q_data.get("answer", "True"),
                                "explanation": q_data.get("explanation", "Based on the provided text.")
                            })
                    
                    return questions
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing failed for T/F: {str(e)}")
                    logger.error(f"Response text: {response_text}")
                    return self._fallback_tf_generation(text, count)
            
            return []
            
        except Exception as e:
            logger.error(f"True/False generation failed: {str(e)}")
            return []
    
    def _generate_short_answer_questions(self, text: str, count: int) -> List[Dict[str, Any]]:
        """Generate short answer questions using Gemini"""
        prompt = f"""Based on the following text, create {count} short answer questions.

IMPORTANT: Respond with ONLY a JSON array, no other text.

Format as JSON array:
[
  {{
    "question": "Question text?",
    "answer": "Short answer",
    "explanation": "Explanation"
  }}
]

Requirements:
- Create clear, specific questions that require brief answers
- Provide concise model answers (2-4 words or short phrases)
- Use only information from the given text
- Focus on key facts, names, dates, or concepts

Text:
{text}"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,
                    max_output_tokens=1200,
                    top_p=0.8
                )
            )
            
            if response.text:
                # Clean the response text
                response_text = response.text.strip()
                
                # Remove any markdown formatting
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
                
                try:
                    questions_data = json.loads(response_text)
                    questions = []
                    
                    for q_data in questions_data:
                        if isinstance(q_data, dict) and "question" in q_data:
                            questions.append({
                                "type": "Short Answer",
                                "question": q_data["question"],
                                "answer": q_data.get("answer", "Answer not provided"),
                                "explanation": q_data.get("explanation", "Based on the provided text.")
                            })
                    
                    return questions
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing failed for Short Answer: {str(e)}")
                    logger.error(f"Response text: {response_text}")
                    return self._fallback_short_generation(text, count)
            
            return []
            
        except Exception as e:
            logger.error(f"Short answer generation failed: {str(e)}")
            return []
    
    def _fallback_mcq_generation(self, text: str, count: int) -> List[Dict[str, Any]]:
        """Fallback method for MCQ generation when JSON parsing fails"""
        prompt = f"""Create {count} multiple choice questions from this text. Use simple format:

Q1: Question?
A) Option 1
B) Option 2  
C) Option 3
D) Option 4
Answer: B

Text: {text[:500]}..."""
        
        try:
            response = self.model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.5))
            if response.text:
                return [{
                    "type": "Multiple Choice",
                    "question": "What is the main topic discussed?",
                    "options": ["Topic A", "Topic B", "Topic C", "Topic D"],
                    "answer": "Topic A",
                    "explanation": "Based on the text content."
                }]
        except:
            pass
        return []
    
    def _fallback_tf_generation(self, text: str, count: int) -> List[Dict[str, Any]]:
        """Fallback method for T/F generation when JSON parsing fails"""
        return [{
            "type": "True/False",
            "question": "True or False: The text contains important information",
            "answer": "True",
            "explanation": "Based on the provided content."
        }]
    
    def _fallback_short_generation(self, text: str, count: int) -> List[Dict[str, Any]]:
        """Fallback method for short answer generation when JSON parsing fails"""
        return [{
            "type": "Short Answer",
            "question": "What is the main topic of this text?",
            "answer": "Main topic",
            "explanation": "Based on the text content."
        }]
        return questions
