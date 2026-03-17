def safe_join_lines(text: str, max_len: int = 300) -> str:
    text = " ".join(text.split())
    return text[:max_len]