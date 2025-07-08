#!/bin/bash
# Simple build script for Utility Bills application
# Usage: ./build.sh [platform] [options]

echo "🔧 Utility Bills Build Helper"
echo "=============================="

# Make the build script executable if needed
chmod +x build_executable.py

# Default to current platform if no argument provided
PLATFORM=${1:-current}

case $PLATFORM in
    "windows")
        echo "🪟 Building for Windows..."
        python3 build_executable.py windows --onefile --clean
        ;;
    "macos")
        echo "🍎 Building for macOS..."
        python3 build_executable.py macos --onefile --clean
        ;;
    "debug")
        echo "🐛 Building debug version..."
        python3 build_executable.py current --debug --clean
        ;;
    "current")
        echo "💻 Building for current platform..."
        python3 build_executable.py current --onefile --clean
        ;;
    "help")
        echo "Available options:"
        echo "  ./build.sh windows    - Build for Windows"
        echo "  ./build.sh macos      - Build for macOS"
        echo "  ./build.sh current    - Build for current platform"
        echo "  ./build.sh debug      - Build debug version"
        echo "  ./build.sh help       - Show this help"
        echo ""
        echo "For more options, use:"
        echo "  python3 build_executable.py --help"
        ;;
    *)
        echo "❌ Unknown platform: $PLATFORM"
        echo "Use: ./build.sh help for available options"
        exit 1
        ;;
esac 