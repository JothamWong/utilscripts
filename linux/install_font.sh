#!/bin/bash

if [[ "$1" == "--help" ]]; then
    echo "Usage: $(basename "$0") <font_directory> [--help]"
    echo ""
    echo "Install fonts from a directory to your local user fonts directory."
    echo ""
    echo "Arguments:"
    echo "  font_directory    Path to directory containing fonts"
    echo ""
    echo "Options:"
    echo "  --help           Show this help message and exit"
    exit 0
fi

if [[ $# -eq 0 ]]; then
    echo "Error: Font directory path is required."
    echo "Usage: $(basename "$0") <font_directory>"
    echo "Use --help for more information."
    exit 1
fi

FONT_DIR="$1"

if [[ ! -d "$FONT_DIR" ]]; then
    echo "Error: Directory '$FONT_DIR' does not exist."
    exit 1
fi

mkdir -p ~/.local/share/fonts

FONT_NAME=$(basename "$FONT_DIR")
INSTALL_DIR="$HOME/.local/share/fonts/$FONT_NAME"

rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

copy_fonts_from_subdir() {
    local subdir="$1"
    if [[ -d "$FONT_DIR/$subdir" ]]; then
        echo "Copying ${subdir}"
        cp "$FONT_DIR/$subdir"/* "$INSTALL_DIR/" 2>/dev/null
    fi
}

copy_fonts_directly() {
    echo "Copying fonts from main directory..."
    for ext in ttf otf woff woff2 TTF OTF WOFF WOFF2; do
        if ls "$FONT_DIR"/*.$ext 1> /dev/null 2>&1; then
            cp "$FONT_DIR"/*.$ext "$INSTALL_DIR/" 2>/dev/null
        fi
    done
}

echo "Copying subdir fonts"
copy_fonts_from_subdir "otf"
copy_fonts_from_subdir "ttf"
copy_fonts_from_subdir "variable"
copy_fonts_from_subdir "frozen"
copy_fonts_from_subdir "fonts"
copy_fonts_directly

echo "Fonts installed to: $INSTALL_DIR"
echo "Rebuilding font cache..."
fc-cache -f
echo "Font installation complete!"
