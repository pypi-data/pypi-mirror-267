import json
import pandas as pd
import requests
import sqlalchemy
import time
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

HTTP_MAX_RETRIES = 20
HTTP_RETRY_DELAY = 5


def get_namespace(uri):
    """Get the namespace of the URI."""
    if uri.startswith("https://docs.pingcap.com"):
        return "document"
    elif uri.startswith("https://ask.pingcap.com"):
        return "forum"
    elif uri.startswith("https://www.pingcap.com/blog"):
        return "blog"
    elif uri.startswith("https://www.pingcap.com/customers") or uri.startswith(
        "https://www.pingcap.com/case-study"
    ):
        return "case study"
    elif uri.startswith("https://www.pingcap.com/press-release"):
        return "press-release"
    elif uri.startswith("https://www.pingcap.com/article"):
        return "seo_article"
    elif uri.startswith("https://www.pingcap.com/event"):
        return "event"
    elif uri.startswith("https://www.pingcap.com"):
        return "official_website"
    else:
        return "others"


def search_by_semantic(query, top_k=5, namespaces=[]):
    """
    Query the similar chunks by semantic from tidb.ai.

    :return: The API response as a List object if successful, otherwise an error message.
    List of:
    - text_content
    - source_uri
    - source_name
    - relevance_score
    """
    url = "https://tidb.ai/api/v1/indexes/default/query"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "top_k": top_k,
        "text": query,
        "namespaces": namespaces,
    }

    max_retries = 20  # Maximum number of retries
    retry_delay = 5  # Delay between retries in seconds

    for attempt in range(HTTP_MAX_RETRIES):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # This will raise an HTTPError if the response was an error
            return response.json()  # Return the successful response as JSON
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 500 or err.response.status_code == 504:
                print(
                    f"Attempt {attempt + 1} of {max_retries}: HTTP {err.response.status_code} Server Error - {err.response}. Retrying in {retry_delay} seconds..."
                )
                time.sleep(retry_delay)
            else:
                # Properly raising an exception with a formatted message
                raise
        except requests.exceptions.RequestException:
            print(
                f"Attempt {attempt + 1} of {max_retries}: Request Error. Retrying in {retry_delay} seconds..."
            )
            time.sleep(HTTP_RETRY_DELAY)

    # If the loop completes without returning, raise an exception
    raise Exception(
        "Error: Max retries reached. The request failed to complete successfully."
    )


class TiDBCorpusClient:
    def __init__(self, tidb_connection_string):
        self.connection_string = tidb_connection_string
        self._bind = self._create_engine()

    def _create_engine(self) -> sqlalchemy.engine.Engine:
        """Create a sqlalchemy engine."""
        return sqlalchemy.create_engine(url=self.connection_string)

    def __del__(self) -> None:
        """Close the connection when the program is closed"""
        if isinstance(self._bind, sqlalchemy.engine.Connection):
            self._bind.close()

    def execute_query(self, query):
        """
        Execute a SQL query using a connection URL and return the results.
        :return: Query results as a DataFrame, or an error message.
        """
        try:
            # Ensure the connection string is used to create the engine
            results = pd.read_sql_query(query, con=self._bind)
            return results
        except Exception as e:
            return f"Error: {e}"

    def fetch_document(self, document_id):
        document_id_query = f"SELECT text FROM llamaindex_document_node where document_id = '{document_id}' order by indexed_at desc limit 1"
        return self.execute_query(document_id_query)

    def search_relevant_documents(self, question, corpus_df=None, top_k=5):
        if corpus_df is None:
            corpus_df = pd.DataFrame(
                columns=[
                    "namespace",
                    "source_name",
                    "source_uri",
                    "relevance_score",
                    "document_id",
                    "text",
                    "query",
                    "token_count",
                    "chunk_id",
                ]
            )

        relevant_chunks = search_by_semantic(question, top_k)
        relevant_chunks_df = pd.DataFrame(relevant_chunks)
        if relevant_chunks_df is None:
            return corpus_df

        relevant_chunks_df["namespace"] = relevant_chunks_df["document_uri"].apply(
            get_namespace
        )
        # Filter out seo_article entries
        relevant_chunks_df = relevant_chunks_df[
            relevant_chunks_df["namespace"] != "seo_article"
        ]

        for index, row in relevant_chunks_df.iterrows():
            namespace = row["namespace"]
            if namespace in ["forum", "document"]:
                # Use text_content directly for forum and document namespaces
                text = row["text"]
                new_row = pd.DataFrame(
                    [
                        {
                            "source_name": row["document_name"],
                            "source_uri": row["document_uri"],
                            "relevance_score": row["relevance_score"],
                            "document_id": row[
                                "document_id"
                            ],  # Document ID not fetched
                            "text": text,
                            "query": question,
                            "namespace": namespace,
                            "chunk_id": row["document_chunk_node_id"],
                            "token_count": len(enc.encode(text)),
                        }
                    ]
                )
                corpus_df = pd.concat([corpus_df, new_row], ignore_index=True)
            elif corpus_df[corpus_df["source_uri"] == row["document_uri"]].empty:
                try:
                    result_df = self.fetch_document(row["document_id"])
                    if not isinstance(result_df, pd.DataFrame):
                        raise ValueError(
                            f"failed to fetch document({row['document_id']}):{result_df}"
                        )
                except Exception:
                    print(f"failed to fetch document from {row['source_uri']}")
                    continue

                text = result_df.iloc[0]["text"]
                new_row = pd.DataFrame(
                    [
                        {
                            "source_name": row["document_name"],
                            "source_uri": row["document_uri"],
                            "relevance_score": row["relevance_score"],
                            "document_id": row[
                                "document_id"
                            ],  # Document ID not fetched
                            "text": text,
                            "query": question,
                            "namespace": namespace,
                            "chunk_id": row["document_chunk_node_id"],
                            "token_count": len(enc.encode(text)),
                        }
                    ]
                )
                corpus_df = pd.concat([corpus_df, new_row], ignore_index=True)

        return corpus_df
