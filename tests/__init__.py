# tests/__init__.py
# Test package marker.
#
# Some environments include an unrelated site-packages "tests" module.
# Adding this file ensures `python -m unittest -q tests/...` resolves to this
# repository's test modules.
