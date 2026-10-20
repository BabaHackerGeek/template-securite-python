import hashlib


def get_file_metadata(data: bytes) -> dict:
    """Pour avoir les infos de base d'un fichier depuis son contenu"""
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "md5": hashlib.md5(data).hexdigest(),
        "size": len(data),
    }