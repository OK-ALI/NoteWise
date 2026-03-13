"""
Simple File-Based Storage for NoteWise
Lightweight JSON-based storage system
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

class SimpleStorage:
    """
    Simple file-based storage using JSON for NoteWise
    Stores user sessions, summaries, and questions locally
    """
    
    def __init__(self, storage_dir: str = "user_data"):
        """Initialize storage with specified directory"""
        self.storage_dir = storage_dir
        self.sessions_file = os.path.join(storage_dir, "sessions.json")
        self.summaries_file = os.path.join(storage_dir, "summaries.json")
        self.questions_file = os.path.join(storage_dir, "questions.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize storage files if they don't exist
        self._init_storage_files()
    
    def _init_storage_files(self):
        """Initialize JSON storage files"""
        for file_path in [self.sessions_file, self.summaries_file, self.questions_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    def _load_data(self, file_path: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, file_path: str, data: List[Dict]):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    # Session Management
    def create_session(self, user_id: str = "default") -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "status": "active"
        }
        
        sessions = self._load_data(self.sessions_file)
        sessions.append(session_data)
        self._save_data(self.sessions_file, sessions)
        
        return session_id
    
    def get_sessions(self, user_id: str = "default") -> List[Dict]:
        """Get all sessions for a user"""
        sessions = self._load_data(self.sessions_file)
        return [s for s in sessions if s.get("user_id") == user_id]
    
    # Summary Storage
    def save_summary(self, session_id: str, original_text: str, summary: str, 
                    summary_type: str = "standard") -> str:
        """Save a summary and return summary ID"""
        summary_id = str(uuid.uuid4())
        summary_data = {
            "summary_id": summary_id,
            "session_id": session_id,
            "original_text": original_text[:500] + "..." if len(original_text) > 500 else original_text,
            "summary": summary,
            "summary_type": summary_type,
            "created_at": datetime.now(),
            "word_count": len(summary.split())
        }
        
        summaries = self._load_data(self.summaries_file)
        summaries.append(summary_data)
        self._save_data(self.summaries_file, summaries)
        
        return summary_id
    
    def get_summaries(self, session_id: str) -> List[Dict]:
        """Get all summaries for a session"""
        summaries = self._load_data(self.summaries_file)
        return [s for s in summaries if s.get("session_id") == session_id]
    
    # Question Storage
    def save_questions(self, session_id: str, questions: List[Dict], 
                      question_type: str = "mixed") -> str:
        """Save questions and return question set ID"""
        question_set_id = str(uuid.uuid4())
        question_data = {
            "question_set_id": question_set_id,
            "session_id": session_id,
            "questions": questions,
            "question_type": question_type,
            "created_at": datetime.now(),
            "question_count": len(questions)
        }
        
        all_questions = self._load_data(self.questions_file)
        all_questions.append(question_data)
        self._save_data(self.questions_file, all_questions)
        
        return question_set_id
    
    def get_questions(self, session_id: str) -> List[Dict]:
        """Get all question sets for a session"""
        all_questions = self._load_data(self.questions_file)
        return [q for q in all_questions if q.get("session_id") == session_id]
    
    # Export Functions
    def export_summary_to_file(self, summary_id: str, export_path: str = "exports"):
        """Export a specific summary to a text file"""
        summaries = self._load_data(self.summaries_file)
        summary = next((s for s in summaries if s.get("summary_id") == summary_id), None)
        
        if not summary:
            raise ValueError(f"Summary {summary_id} not found")
        
        os.makedirs(export_path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.txt"
        filepath = os.path.join(export_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Summary - {summary['created_at']}\n\n")
            f.write(f"**Type:** {summary['summary_type']}\n")
            f.write(f"**Word Count:** {summary['word_count']}\n\n")
            f.write("## Summary\n\n")
            f.write(summary['summary'])
        
        return filepath
    
    def export_questions_to_file(self, question_set_id: str, export_path: str = "exports"):
        """Export questions to a formatted text file"""
        all_questions = self._load_data(self.questions_file)
        question_set = next((q for q in all_questions if q.get("question_set_id") == question_set_id), None)
        
        if not question_set:
            raise ValueError(f"Question set {question_set_id} not found")
        
        os.makedirs(export_path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"questions_{timestamp}.txt"
        filepath = os.path.join(export_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Questions - {question_set['created_at']}\n\n")
            f.write(f"**Type:** {question_set['question_type']}\n")
            f.write(f"**Total Questions:** {question_set['question_count']}\n\n")
            
            for i, q in enumerate(question_set['questions'], 1):
                f.write(f"## Question {i}\n\n")
                f.write(f"**{q.get('question', '')}**\n\n")
                
                if q.get('type') == 'mcq' and q.get('options'):
                    for opt_key, opt_value in q['options'].items():
                        f.write(f"{opt_key.upper()}) {opt_value}\n")
                    f.write(f"\n**Answer:** {q.get('answer', '')}\n\n")
                elif q.get('type') == 'true_false':
                    f.write(f"**Answer:** {q.get('answer', '')}\n\n")
                else:
                    f.write(f"**Suggested Answer:** {q.get('answer', '')}\n\n")
                
                if q.get('explanation'):
                    f.write(f"**Explanation:** {q['explanation']}\n\n")
                
                f.write("---\n\n")
        
        return filepath
    
    # Cleanup Functions
    def delete_old_sessions(self, days_old: int = 30):
        """Delete sessions older than specified days"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        # Clean sessions
        sessions = self._load_data(self.sessions_file)
        sessions = [s for s in sessions if datetime.fromisoformat(str(s['created_at'])) > cutoff_date]
        self._save_data(self.sessions_file, sessions)
        
        # Get remaining session IDs
        valid_session_ids = {s['session_id'] for s in sessions}
        
        # Clean summaries
        summaries = self._load_data(self.summaries_file)
        summaries = [s for s in summaries if s.get('session_id') in valid_session_ids]
        self._save_data(self.summaries_file, summaries)
        
        # Clean questions
        all_questions = self._load_data(self.questions_file)
        all_questions = [q for q in all_questions if q.get('session_id') in valid_session_ids]
        self._save_data(self.questions_file, all_questions)
