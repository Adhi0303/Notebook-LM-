from typing import List, Dict, Any

class TokenBatcher:
    def __init__(self, token_limit: int = 90000):
        self.token_limit = token_limit
        try:
            import tiktoken
            self.encoder = tiktoken.get_encoding("cl100k_base")
            self.use_tiktoken = True
        except ImportError:
            self.use_tiktoken = False

    def estimate_tokens(self, text: str) -> int:
        if self.use_tiktoken:
            return len(self.encoder.encode(text))
        else:
            # Fallback estimation if tiktoken is not installed
            return len(text) // 4

    def batch_documents(self, documents: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Splits a giant list of documents into 'Buckets' where the total 
        token count of each Bucket never exceeds the token_limit.
        """
        buckets = []
        current_bucket = []
        current_tokens = 0

        for doc in documents:
            text = doc.get("text", "")
            tokens = self.estimate_tokens(text)

            if current_tokens + tokens > self.token_limit and current_bucket:
                # The bucket is full! Save it and start a new one
                buckets.append(current_bucket)
                current_bucket = [doc]
                current_tokens = tokens
            else:
                # Add to the current bucket
                current_bucket.append(doc)
                current_tokens += tokens

        # Don't forget to add the final bucket!
        if current_bucket:
            buckets.append(current_bucket)

        return buckets
