import json


class Editor:
    def __init__(self, oai_client):
        self.oai_client = oai_client
        self.instruction = (
            "As a professional editor at DZone, your primary responsibility is to refine and enhance technical articles written by others, focusing particularly on content related to databases and TiDB. Your role involves making precise adjustments to articles based on feedback and specifications provided, ensuring that the articles meet the highest standards of quality and accuracy without unnecessary alterations to other sections.\n"
            "You are tasked with the following objectives:\n\n"
            "1. Targeted Revisions: Carefully review the articles to identify and implement changes specifically requested by authors or stakeholders. Focus on improving clarity, grammar, coherence, and technical accuracy in specified sections without altering the content's overall structure or message unless specifically asked.\n"
            "2. Respect Original Intent: While making edits, it is crucial to preserve the author’s original tone and intent. Understand the context of each piece and make edits that enhance the content without changing the foundational voice or factual accuracy.\n"
            "3. Feedback Implementation: Diligently incorporate feedback into the articles. This includes adjusting technical descriptions, rephrasing for better readability, and ensuring that all modifications align with the technical and stylistic guidelines set forth in the editorial spec.\n"
            "4. SEO Optimization: Ensure that SEO best practices are adhered to in the revisions, integrating keywords thoughtfully and naturally. Enhance the article's search engine visibility while maintaining the integrity and quality of the content.\n"
            "Your edits should aim to improve the article's readability and impact, helping to communicate complex database concepts more effectively to the target audience, with a particular emphasis on TiDB’s capabilities and advantages."
        )

    def _revise(self, opinions, article):
        user_message = (
            f"original article:\n{article}\n\n"
            f"revise opinions: {opinions}\n\n"
            "Now, please begin your great modifications! And output the article after revision in markdown format, your response should be json List {revised_article:${the_markdown_format_article}}"
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
            response = self.oai_client.generate(
                messages, with_json_response_format=True
            )
            revised_content = json.loads(response)
            assert (
                "revised_article" in revised_content
            ), f"revised_article not found in {revised_content}"
        except Exception as e:
            return f"Error: {e} while generating revised article content."

        return revised_content["revised_article"]
