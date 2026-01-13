import re

def has_blocked_parts(msg: str) -> bool:
    patterns = [
        # Full IPv4
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',

        # Partial IPv4 (2–3 octets, allows trailing dot)
        r'\b(?:\d{1,3}\.){1,2}\d{0,3}\b',

        # Obfuscated IPv4 (192[.]168, 10(dot)0, etc.)
        r'\b(?:\d{1,3}\s*(?:\.|\[.\]|\(.\)|dot)\s*){1,3}\d{0,3}\b',

        # IPv6 (common forms)
        r'\b(?:[a-fA-F0-9]{1,4}:){2,7}[a-fA-F0-9]{1,4}\b',

        # URLs
        r'\bhttps?://\S+\b',
        r'\bwww\.\S+\b',

        # domains
        r'\b[a-zA-Z0-9-]+\.(?:de|com|net|org|io|gov|edu|co|uk|info|biz)\b',
 
        r'\b[iI]+\W*[pP]+\b'

        # Coordinates with N/S/E/W
        r'\b\d{1,2}(?:\.\d+)?°?\s*[NS]\s*,?\s*\d{1,3}(?:\.\d+)?°?\s*[EW]\b'
    ]

    combined_pattern = re.compile('|'.join(patterns), re.IGNORECASE)

    return bool(combined_pattern.search(msg))