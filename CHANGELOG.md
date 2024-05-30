## 0.2.2 (2024-05-30)

### Refactor

- **scryfall/fetch**: Implement new request funcs

## 0.2.1 (2024-05-29)

### Fix

- **mtgjson/enums**: Change incorrect MTGJSON url

### Refactor

- **vectors/fetch**: Separate caching and request funcs, remove deprecated `update_vectors_manifest`
- **scryfall**: Small schema changes, remove deprecated type "SetTypes", add core imports to __init__
- **scryfall/fetch**: Use "cache_" naming for download funcs, "get_" for JSON data loading funcs. Add new request funcs
- **schema**: Treat missing lists as an empty list
- **mtgjson/fetch**: Use "cache_" for saving JSON files locally, use "get_" for loading as JSON object. Implement new request functions

## 0.2.0 (2024-05-17)

### Feat

- **mtgpics**: Introduce new data source: MTGPics.com
- **mtgjson**: Implement full schema spec from MTGJSON docs

### Refactor

- **mtg-vectors**: Make adjustments to MTG Vectors data source
- **scryfall**: Finish base schema definitions and enums for Scryfall data source
- **hexapi**: Integrate "unified" hexproof.io API source as hexapi module
- **scryfall**: Implement new enums, update fetch funcs, update Set schema
- **pyproject.toml**: Add commitizen config

## 0.1.0 (2024-05-02)

### Refactor

- **hexproof**: Import core functionality from the `hexproof.io` repository
