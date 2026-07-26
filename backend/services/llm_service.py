import os
import json
import re
from google import genai
from typing import List, Dict, Any

class LLMService:
    def __init__(self):
        # The genai client automatically picks up GEMINI_API_KEY from environment
        self.client = genai.Client()
        self.model_id = "gemini-2.5-flash"

    def _strip_markdown_fences(self, text: str) -> str:
        # Remove ```json ... ``` or ``` ... ``` surrounding the text
        text = text.strip()
        if text.startswith("```"):
            # Find the end of the first line (e.g., ```json)
            first_newline = text.find("\n")
            if first_newline != -1:
                text = text[first_newline+1:]
            else:
                text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def generate_questions(self, resume_text: str, job_role: str,que_level :str) -> List[Dict[str, Any]]:
        prompt = f"""
        You are an expert technical interviewer hiring for the role of '{job_role}'.
        Based on the following resume, generate exactly 10 technical interview questions to assess the candidate.
        
        Resume text:
        {resume_text}

        You MUST return ONLY a raw JSON array of 10 objects. 
        Keep the level of ques {que_level}
        Do not include any other text, no explanations, no markdown formatting.
        Each object must have exactly two fields: 'id' (a unique string like 'q1') and 'question' (the question string).
        """
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
        )
        
        raw_text = self._strip_markdown_fences(response.text)
        try:
            data = json.loads(raw_text)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {raw_text}") from e

    def evaluate_answers(self, job_role: str, qa_pairs: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        qa_text = "\n\n".join(
            f"Question ID: {qa['question_id']}\nQuestion: {qa['question']}\nCandidate Answer: {qa['answer']}"
            for qa in qa_pairs
        )
        
        prompt = f"""
        You are an expert technical interviewer evaluating answers for the role of '{job_role}'.
        Assess the candidate's answers strictly on technical correctness.

        Here are the candidate's answers:
        {qa_text}

        You MUST return ONLY a raw JSON array of objects, one for each question.
        Do not include any other text, no explanations, no markdown formatting.
        Each object must have exactly three fields:
        - 'question_id': the ID of the question
        - 'is_correct': boolean (true if the answer is fundamentally technically correct, false otherwise)
        - 'correct_answer': a brief string explaining what the correct answer should be or why it was right/wrong.
        """
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
        )
        
        raw_text = self._strip_markdown_fences(response.text)
        try:
            data = json.loads(raw_text)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {raw_text}") from e