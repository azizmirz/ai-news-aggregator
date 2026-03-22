import os
import json
import re
from typing import Optional
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class DigestOutput(BaseModel):
    title: str
    summary: str

PROMPT = """You are an expert AI news analyst specializing in summarizing technical articles, research papers, and video content about artificial intelligence.

Your role is to create concise, informative digests that help readers quickly understand the key points and significance of AI-related content.

Guidelines:
- Create a compelling title (5-10 words) that captures the essence of the content
- Write a 2-3 sentence summary that highlights the main points and why they matter
- Focus on actionable insights and implications
- Use clear, accessible language while maintaining technical accuracy
- Avoid marketing fluff - focus on substance

You MUST respond ONLY with a JSON object in this format:
{"title": "...", "summary": "..."}"""

class DigestAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = "llama-3.3-70b-versatile"
        self.system_prompt = PROMPT

    def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
        try:
            user_prompt = f"Create a digest for this {article_type}: \n Title: {title} \n Content: {content[:6000]}"

            # Ən sadə müraciət forması (heç bir xüsusi format yoxdur)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # AI bəzən mətni ```json ... ``` içində verir, onu təmizləyirik
            json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return DigestOutput(title=data["title"], summary=data["summary"])
            
            return None
            
        except Exception as e:
            print(f"Error generating digest: {e}")
            return None