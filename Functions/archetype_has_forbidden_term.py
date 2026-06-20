from __future__ import annotations

from normalize_archetype import *

def archetype_has_forbidden_term(archetype,
                                 forbidden_terms = ('EffluentClean',)):
    archetype = normalize_archetype(archetype)

    forbidden_terms = [
        normalize_archetype(term)
        for term in forbidden_terms
    ]

    return any(term in archetype for term in forbidden_terms)
