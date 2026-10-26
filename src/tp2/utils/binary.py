import lief


def parse_binary(path: str) -> dict:
    """Lit un exécutable PE ou ELF et renvoie ses imports, exports et sections."""
    binaire = lief.parse(path)
    if binaire is None:
        return {"imports": [], "exports": [], "sections": []}
    return {
        "imports": sorted({f.name for f in binaire.imported_functions if f.name}),
        "exports": sorted({f.name for f in binaire.exported_functions if f.name}),
        "sections": [s.name for s in binaire.sections],
    }