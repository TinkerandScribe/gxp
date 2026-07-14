"""Starter — naive split, no casefold/punct."""
import string


def count_words(text: str) -> dict[str, int]:
    """
    Count words in text after splitting on whitespace, case-folding, and stripping
    leading/trailing ASCII punctuation.
    
    Args:
        text: The input string to process.
        
    Returns:
        A dictionary mapping normalized words to their counts.
    """
    counts = {}
    # Split on any whitespace
    tokens = text.split()
    
    for token in tokens:
        # Case-fold the token
        folded_token = token.casefold()
        
        # Strip leading and trailing ASCII punctuation repeatedly
        # We need to strip from both ends until no more punctuation is found at the edges
        while folded_token and (folded_token[0] in string.punctuation or 
                               folded_token[-1] in string.punctuation):
            if folded_token[0] in string.punctuation:
                folded_token = folded_token[1:]
            if folded_token and folded_token[-1] in string.punctuation:
                folded_token = folded_token[:-1]
        
        # Drop empty tokens
        if not folded_token:
            continue
            
        counts[folded_token] = counts.get(folded_token, 0) + 1
        
    return counts
