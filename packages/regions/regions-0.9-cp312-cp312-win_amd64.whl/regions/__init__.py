# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regions is Astropy coordinated package to provide tools for region
handling.
"""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
from ._astropy_init import *  # noqa: F401, F403

from ._utils.examples import *  # noqa: F401, F403
from .core import *  # noqa: F401, F403
from .io import *  # noqa: F401, F403
from .shapes import *  # noqa: F401, F403


# Set the bibtex entry to the article referenced in CITATION.rst.
def _get_bibtex():
    import os
    citation_file = os.path.join(os.path.dirname(__file__), 'CITATION.rst')

    with open(citation_file) as citation:
        refs = citation.read().split('@software')[1:]
        if len(refs) == 0:
            return ''
        bibtexreference = f'@software{refs[0]}'
    return bibtexreference


__citation__ = __bibtex__ = _get_bibtex()

del _get_bibtex
