import hashlib
import math
from collections import Counter


def get_file_metadata(data: bytes) -> dict:
    """Pour avoir les infos de base d'un fichier depuis son contenu"""
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "md5": hashlib.md5(data).hexdigest(),
        "size": len(data),
    }

def entropy(data: bytes) -> float:
    """Entropie de Shannon d'un contenu (0 à 8), je me base sur slide 42 du cours."""
    if not data:
        return 0.0
    freq = Counter(data)
    return -sum((c / len(data)) * math.log2(c / len(data)) for c in freq.values())