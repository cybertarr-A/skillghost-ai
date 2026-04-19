from groq import Groq
from app.config import settings


class GroqClient:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in environment variables")

        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a highly experienced expert. Be concise, sharp, and practical."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=800
            )

            content = response.choices[0].message.content

            # 🔥 STRONG CLEANING
            cleaned = (
                content
                .replace("\\n", "\n")
                .replace("\n\n", "\n")
                .replace("  ", " ")
                .strip()
            )

            return cleaned

        except Exception as e:
            return f"[SkillGhost ERROR] {str(e)}"