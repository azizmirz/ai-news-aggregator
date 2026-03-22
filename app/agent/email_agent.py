import os
import re
import json
from datetime import datetime
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()


class EmailIntroduction(BaseModel):
    greeting: str = Field(description="Personalized greeting with user's name and date")
    introduction: str = Field(description="2-3 sentence overview of what's in the top 10 ranked articles")


class RankedArticleDetail(BaseModel):
    digest_id: str
    rank: int
    relevance_score: float
    title: str
    summary: str
    url: str
    article_type: str
    reasoning: Optional[str] = None


class EmailDigestResponse(BaseModel):
    introduction: EmailIntroduction
    articles: List[RankedArticleDetail]
    total_ranked: int
    top_n: int
    
    def to_markdown(self) -> str:
        markdown = f"{self.introduction.greeting}\n\n"
        markdown += f"{self.introduction.introduction}\n\n"
        markdown += "---\n\n"
        
        for article in self.articles:
            markdown += f"## {article.title}\n\n"
            markdown += f"{article.summary}\n\n"
            markdown += f"[Read more →]({article.url})\n\n"
            markdown += "---\n\n"
        
        return markdown


class EmailDigest(BaseModel):
    introduction: EmailIntroduction
    ranked_articles: List[dict] = Field(description="Top 10 ranked articles with their details")


EMAIL_PROMPT = """You are an expert email writer specializing in creating engaging, personalized AI news digests.

Your role is to write a warm, professional introduction for a daily AI news digest email that:
- Greets the user by name
- Includes the current date
- Provides a brief, engaging overview of what's coming in the top 10 ranked articles
- Highlights the most interesting or important themes
- Sets expectations for the content ahead

Keep it concise (2-3 sentences for the introduction), friendly, and professional."""


class EmailAgent:
    def __init__(self, user_profile: dict):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1", 
            api_key=os.getenv("GROQ_API_KEY")          
        )
        self.model = "llama-3.3-70b-versatile"         
        self.user_profile = user_profile

    def generate_introduction(self, ranked_articles: List) -> EmailIntroduction:
        if not ranked_articles:
            return EmailIntroduction(
                greeting=f"Hey {self.user_profile['name']}, here is your daily digest of AI news for {datetime.now().strftime('%B %d, %Y')}.",
                introduction="No articles were ranked today."
            )
        
        top_articles = ranked_articles[:10]
        article_summaries = "\n".join([
            f"{idx + 1}. {article.title if hasattr(article, 'title') else article.get('title', 'N/A')}"
            for idx, article in enumerate(top_articles)
        ])
        
        current_date = datetime.now().strftime('%B %d, %Y')
        user_prompt = f"""Create an email introduction for {self.user_profile['name']} for {current_date}.
        
        Articles:
        {article_summaries}

        Return ONLY a JSON object with "greeting" and "introduction" keys."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": EMAIL_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                data = json.loads(json_match.group())
                
                return EmailIntroduction(
                    greeting=data.get("greeting", f"Hey {self.user_profile['name']}, here is your daily digest!"),
                    introduction=data.get("introduction", "Here are the top AI news stories curated for you today.")
                )
            
            
            raise ValueError("No JSON found in response")

        except Exception as e:
            print(f"Error generating introduction, using default: {e}")
            return EmailIntroduction(
                greeting=f"Hey {self.user_profile['name']}, here is your daily digest for {current_date}.",
                introduction="Here are today's top-ranked AI articles based on your interests."
            )

    def create_email_digest(self, ranked_articles: List[dict], limit: int = 10) -> EmailDigest:
        top_articles = ranked_articles[:limit]
        introduction = self.generate_introduction(top_articles)
        
        return EmailDigest(
            introduction=introduction,
            ranked_articles=top_articles
        )
    
    def create_email_digest_response(self, ranked_articles: List[RankedArticleDetail], total_ranked: int, limit: int = 10) -> EmailDigestResponse:
        top_articles = ranked_articles[:limit]
        introduction = self.generate_introduction(top_articles)
        
        return EmailDigestResponse(
            introduction=introduction,
            articles=top_articles,
            total_ranked=total_ranked,
            top_n=limit
        )

