# Static Site Generator

This project is a **Static Site Generator** developed as part of the Boot.dev Back-End Developer Path. It converts `.md` files from the `contents` folder into complete HTML pages, using a predefined HTML template and outputs them to the `public` folder.

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Features](#features)

## Description

The Static Site Generator automates the process of converting Markdown files into HTML. The generator reads Markdown files from the `contents` folder, applies the `template.html` for layout and styling, and saves the generated HTML files in the `public` folder. You can run the program using `main.py` in the `src` folder or via `main.sh` in the root folder for convenience.

## Usage

1. Place Markdown (`.md`) files in the `contents` folder. Each file here will be processed and converted into an HTML file in the `public` folder.

2. Ensure `template.html` is available in the root folder. This file serves as the main layout and structure template for each generated HTML page.

3. Images can be placed in the `static/images` folder, and the `static` folder also contains the CSS file for styling.

4. Run the generator:

   - From the `src` folder:
     ```bash
     python src/main.py
     ```
   - From the root folder:
     ```bash
     ./main.sh
     ```

## Folder Structure

```
project-root/
│
├── content/               # Contains the Markdown (.md) files to be converted
├── public/                 # Output folder for the generated HTML files
├── src/                    # Source code for the generator
│   └── main.py             # Main Python script to run the generator
├── static/                 # Contains assets like CSS and images
│   ├── index.css           # CSS file for styling
│   └── images/             # Folder for images
├── template.html           # HTML template used for each page
└── main.sh                 # Script to run the generator from the root folder
```

## Features

- **Markdown to HTML Conversion**: Automatically converts `.md` files to HTML.
- **Template-Based Layout**: Uses `template.html` for consistent layout.
- **Static Assets**: Supports CSS and images for styling and media.
