import json


class Researcher:
    def __init__(self, oai_client, tidb_corpus_client):
        self.oai_client = oai_client
        self.tidb_corpus_client = tidb_corpus_client
        self.instruction = (
            "As a Researcher at PingCAP, your primary objective is to leverage article specifications and SEO keywords to generate queries aimed at locating relevant writing materials within our extensive content library. Your proficiency in technical research plays a vital role in amplifying the allure of our content to an audience keen on gaining insights into database technologies.\n"
            "The research methodology comprises:\n"
            "- Query Generation: Craft targeted queries grounded in the article specifications. These queries are key to discovering the most pertinent and compelling materials in our content library, ensuring that the resulting articles are both informative and engaging.\n"
            "- Focus on Relevance to SEO Keywords: Additionally, you are tasked with generating queries designed to locate materials that correspond to each SEO keywords. The objective here is to create content that not only educates but also maximizes reach and visibility through search engine optimization.\n"
            "- Topic-Specific Queries: Formulate queries for each subject outlined in the article specifications, don't miss any topics, aiding in the procurement of detailed materials for content creation. This systematic approach ensures that the articles are rich in information, accuracy, and are in tune with the interests and search behaviors of our readers.\n\n"
            "Your contribution is pivotal in the content creation pipeline, ensuring it is supported by thorough research and the newest advancements in database technology. The queries you generate will serve as a foundation for writing articles that are not only rich in information but also enjoy high visibility in search engine results, thus highlighting the distinctive features and practical applications of TiDB.\n"
            "The expected output from your research is a list of queries to facilitate the search for content that aligns with SEO keywords and supports the creation of impactful and engaging articles."
        )

    def search(self, article_spec, seo_keywords=[], max_tokens_count=100000):
        queries = self._create_queries(article_spec, seo_keywords)
        if len(queries) == 0:
            queries = article_spec.splitlines()
            queries.extend(seo_keywords)

        corpus = None
        for query in queries:
            corpus = self.tidb_corpus_client.search_relevant_documents(query, corpus)

        corpus = corpus.sort_values(by="relevance_score", ascending=False)
        corpus = corpus.drop_duplicates(subset="text")

        # Sort the DataFrame by 'relevance_score' in descending order to perform 'reverse' sorting.
        corpus = corpus.sort_values(by="relevance_score", ascending=False)
        if corpus["token_count"].sum() <= max_tokens_count:
            return corpus

        top_df = (
            corpus.groupby("query")
            .apply(lambda x: x.nlargest(2, "relevance_score"))
            .reset_index(level=0, drop=True)
        )
        total_token_count = top_df["token_count"].sum()

        if total_token_count < max_tokens_count:
            remaining_rows = corpus.loc[~corpus.index.isin(top_df.index)]
            additional_rows = remaining_rows.sort_values(
                by="relevance_score", ascending=False
            )
            for index, row in additional_rows.iterrows():
                top_df = top_df.append(row)
                total_token_count += row["token_count"]
                if total_token_count >= max_tokens_count:
                    break

        return top_df

    def _create_queries(self, article_spec, seo_keywords=[]):
        user_message = (
            f"---- article spec ----\n{article_spec}\n\n"
            f"---- seo keywords ----\n{seo_keywords}\n\n"
            "Now, please begin to creates your queries, output into a json List {queries:[....]}!"
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
        response = self.oai_client.generate(messages, with_json_response_format=True)
        queries = json.loads(response)
        if "queries" in queries:
            return queries["queries"]
        elif "query" in queries:
            return queries["query"]
        else:
            return []
