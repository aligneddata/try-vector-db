from abc import ABC, abstractmethod

class SplitterSimple(ABC):
    def __init__(self):
        super().__init__()
        
    def split(self, text: str, chunk_size: int, overlap=0):
        return chunk_text(text, chunk_size, overlap)


def chunk_text(text, chunk_size, overlap=0):
    """Breaks a large text into a list of smaller text chunks.

    Args:
        text: The input text (string).
        chunk_size: The desired size of each chunk (integer).
        overlap: The number of overlapping characters between chunks (integer).

    Returns:
        A list of string chunks. Returns an empty list if the input text is empty or chunk_size is invalid.
        Returns a list containing the original text if chunk_size is larger than the text length and overlap is 0.

    Raises:
        TypeError: If inputs are not of correct types.
        ValueError: If chunk_size or overlap are negative or if overlap is greater than chunk_size.
    """

    if not isinstance(text, str):
      raise TypeError("text must be a string")
    if not isinstance(chunk_size, int):
      raise TypeError("chunk_size must be an integer")
    if not isinstance(overlap, int):
      raise TypeError("overlap must be an integer")
    
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size and chunk_size > 0:
        raise ValueError("overlap must be less than chunk_size")

    if not text:  # Handle empty text input
        return []

    text_length = len(text)
    if chunk_size >= text_length and overlap == 0:
        return [text]

    chunks = []
    start = 0
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap  # Move the starting point for the next chunk

    return chunks
