import hashlib

def hash_string(input_string, algorithm='sha256'):
    """Hashes a string using the specified algorithm.

    Args:
        input_string: The string to hash.
        algorithm: The hashing algorithm to use (e.g., 'md5', 'sha256', 'sha3_256').

    Returns:
        The hexadecimal representation of the hash, or None if the algorithm is invalid.
    """
    try:
        hasher = hashlib.new(algorithm)
    except ValueError:
        return None  # Invalid algorithm

    # Important: Encode the string to bytes before hashing
    input_bytes = input_string.encode('utf-8')  # Use UTF-8 encoding (most common)
    hasher.update(input_bytes)
    return hasher.hexdigest()