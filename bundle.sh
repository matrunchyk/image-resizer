#!/bin/bash

# Set up environment variables
APP_NAME="ImageProcessor"
DIST_DIR="dist"
BUILD_DIR="build"
SPEC_FILE="gui.spec"
BACKGROUND_IMAGE="background.png"

# Ensure the virtual environment is activated
source venv/bin/activate

# Clean previous builds
echo "Cleaning up previous builds..."
rm -rf $DIST_DIR $BUILD_DIR

# Ensure PyInstaller is installed
pip install --upgrade pyinstaller

# Install create-dmg if not already installed
if ! command -v create-dmg &> /dev/null
then
    echo "create-dmg could not be found, installing..."
    brew install create-dmg
fi

# Run PyInstaller
echo "Building the application with PyInstaller..."
pyinstaller --clean --noconfirm --log-level=DEBUG $SPEC_FILE

# Check if the build was successful
if [ ! -d "$DIST_DIR/$APP_NAME.app" ]; then
  echo "Error: Application bundle was not created successfully."
  exit 1
fi

echo "Application bundle created successfully."

# Sign the application
echo "Signing the application..."
codesign --deep --force --verbose --sign - "$DIST_DIR/$APP_NAME.app"

# Clean up extra files in the dist directory
rm -rf "$DIST_DIR/$APP_NAME"

# Verify the application
echo "Verifying the application..."
spctl --assess --verbose=4 --type execute "$DIST_DIR/$APP_NAME.app"

# Create a .background folder and copy the background image
BACKGROUND_DIR="$DIST_DIR/.background"
mkdir -p "$BACKGROUND_DIR"
cp "$BACKGROUND_IMAGE" "$BACKGROUND_DIR"

# Optional: Create a DMG file for distribution
echo "Creating DMG file..."
DMG_NAME="${APP_NAME}.dmg"
create-dmg \
  --volname "$APP_NAME" \
  --window-pos 200 120 \
  --window-size 800 600 \
  --icon-size 100 \
  --app-drop-link 600 285 \
  --icon "$APP_NAME.app" 200 285 \
  --icon "Applications" 600 285 \
  --background "$BACKGROUND_IMAGE" \
  "$DIST_DIR/$DMG_NAME" \
  "$DIST_DIR/"

if [ -f "$DIST_DIR/$DMG_NAME" ]; then
  echo "DMG file created successfully: $DIST_DIR/$DMG_NAME"
else
  echo "Error: Failed to create DMG file."
  exit 1
fi

echo "Bundle process completed successfully."

