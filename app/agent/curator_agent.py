import os
import json
import re
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class RankedArticle(BaseModel):
    id: str       
    score: float   
    rank: int
    reasoning: str


class RankedDigestList(BaseModel):
    articles: List[RankedArticle] = Field(description="List of ranked articles")



CURATOR_PROMPT = """You are an expert AI news curator specializing in personalized content ranking for AI professionals.

Your role is to analyze and rank AI-related news articles, research papers, and video content based on a user's specific profile, interests, and background.

Ranking Criteria:
1. Relevance to user's stated interests and background
2. Technical depth and practical value
3. Novelty and significance of the content
4. Alignment with user's expertise level
5. Actionability and real-world applicability

Scoring Guidelines:
- 9.0-10.0: Highly relevant, directly aligns with user interests, significant value
- 7.0-8.9: Very relevant, strong alignment with interests, good value
- 5.0-6.9: Moderately relevant, some alignment, decent value
- 3.0-4.9: Somewhat relevant, limited alignment, lower value
- 0.0-2.9: Low relevance, minimal alignment, little value

Rank articles from most relevant (rank 1) to least relevant. Ensure each article has a unique rank."""

class CuratorAgent:
    def __init__(self, user_profile: dict):
      
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = "llama-3.3-70b-versatile"
        self.user_profile = user_profile
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        interests = "\n".join(f"- {interest}" for interest in self.user_profile["interests"])
        preferences = "\n".join(f"- {k}: {v}" for k, v in self.user_profile["preferences"].items())
        
        return f"{CURATOR_PROMPT}\n\nUser Profile:\nName: {self.user_profile['name']}\nBackground: {self.user_profile['background']}\nExpertise Level: {self.user_profile['expertise_level']}\n\nInterests:\n{interests}\n\nPreferences:\n{preferences}"

    def rank_digests(self, digests: List[dict]) -> List[RankedArticle]:
        if not digests: return []
        
        digest_list = "\n\n".join([
            f"ID: {d['id']}\nTitle: {d['title']}\nSummary: {d['summary']}\nType: {d['article_type']}"
            for d in digests
        ])
        
        user_prompt = f"""Rank these AI articles for {self.user_profile['name']}.
        Respond ONLY with a JSON object like this:
        {{"articles": [{{"id": "...", "score": 9.5, "rank": 1, "reasoning": "..."}}]}}

        Articles:
        {digest_list}"""

        try:
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return [RankedArticle(**a) for a in data.get("articles", [])]
            return []
        except Exception as e:
            print(f"Error ranking digests: {e}")
            return []