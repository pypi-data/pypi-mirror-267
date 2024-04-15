from typing import List, Optional


class Writer:
    """A professional technical writer at PingCAP, crafting and publishing exceptional technical articles focused on databases, particularly promoting TiDB."""

    def __init__(self, long_llm, writer_name="Adam D'Angelo (co-founder of Quora)"):
        self.writer_name = writer_name
        self.long_llm = long_llm
        self.instruction = (
            "As a professional technical writer at PingCAP, your primary OKR is to craft and publish exceptional technical articles focused on databases, particularly promoting TiDB, across various online platforms. "
            "Leveraging your expertise in SEO, you aim to incorporate trending keywords related to databases within your articles. This strategy will enhance the visibility and reach of your content, attracting readers actively searching for database technologies.\n"
            "Your articles should serve to educate and inform a target audience curious about database technologies, their applications, and implementations, with a special emphasis on TiDB's unique features and case studies. "
            "Through your writing, you aim to demystify complex database concepts and showcase how TiDB addresses common challenges in this field.\n\n"
            "Now you will be tasked with crafting an exceptional article grounded in the materials provided from our content library. These materials form the factual foundation of your article, ensuring accuracy and relevance. Your writing should adhere to the specifications outlined in the article spec, guiding the structure, tone, and scope of your content."
            "1. Foundation on Materials: Your article should be meticulously researched, drawing upon the Background Materials provided. It's crucial that all factual statements and technical explanations within your article are supported by these materials to maintain credibility and accuracy.\n"
            "2. Adherence to Article Spec: The article must follow the specific guidelines outlined in the article spec.\n"
            "3. SEO Keyword Integration: Seamlessly incorporate SEO keywords into your writing. These keywords should be relevant to the topic and integrated naturally into the content. The aim is to enhance the article's visibility on search engines and attract readers searching for information on database technologies, without resorting to keyword stuffing or distorting the article's factual content."
        )

    def write(
        self,
        article_spec,
        background_materials=None,
        seo_keywords: Optional[List] = None,
    ):
        """Generate an article based on the provided specifications and materials."""
        user_message = (
            f"---- background materials ----\n{background_materials}\n\n"
            f"---- article spec ----\n{article_spec}\n\n"
            f"---- seo keywords ----\n{seo_keywords}\n\n"
            f"You are expected to adopt a writing style reminiscent of {self.writer_name} engaging and insightful technical articles. "
            "Your articles should not only inform but also inspire readers by highlighting the innovative aspects of TiDB and its practical applications in solving real-world problems.\n"
            "Now, please begin your great creation! And write it in markdown format, words count should be 1200 ~ 1500"
        )

        messages = [
            {
                "role": "system",
                "content": self.instruction,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]
        try:
            response = self.long_llm.generate(messages)
        except Exception as e:
            return f"Error: {e} while generating article content."
        return response
