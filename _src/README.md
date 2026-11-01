# Site sources

The published pages (index.html, name.html, explore.html) are generated from these files.
The underscore folder name keeps GitHub Pages from publishing them.

- template.html – homepage template (all text, styles, scripts); `__WORKS__` is replaced with works data
- works.min.json – the catalogue of works (generated from catalogue.md by parse.py + build_data.py, then edited)
- explore.js / build_explore.py – the "Inside the constraint" page
- build.py – builds dist/index.html, dist/name.html, dist/explore.html

To rebuild: copy this folder to a working directory, create `dist/`, run `python3 build.py`,
then copy dist/*.html to the repository root.
