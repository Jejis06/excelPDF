@echo off
REM Simple build script for Utility Bills application on Windows
REM Usage: build.bat [platform] [options]

echo 🔧 Utility Bills Build Helper
echo ==============================

REM Default to current platform if no argument provided
set PLATFORM=%1
if "%PLATFORM%"=="" set PLATFORM=current

if "%PLATFORM%"=="windows" (
    echo 🪟 Building for Windows...
    python build_executable.py windows --onefile --clean
    goto :end
)

if "%PLATFORM%"=="macos" (
    echo 🍎 Building for macOS...
    python build_executable.py macos --onefile --clean
    goto :end
)

if "%PLATFORM%"=="debug" (
    echo 🐛 Building debug version...
    python build_executable.py current --debug --clean
    goto :end
)

if "%PLATFORM%"=="current" (
    echo 💻 Building for current platform...
    python build_executable.py current --onefile --clean
    goto :end
)

if "%PLATFORM%"=="help" (
    echo Available options:
    echo   build.bat windows    - Build for Windows
    echo   build.bat macos      - Build for macOS
    echo   build.bat current    - Build for current platform
    echo   build.bat debug      - Build debug version
    echo   build.bat help       - Show this help
    echo.
    echo For more options, use:
    echo   python build_executable.py --help
    goto :end
)

echo ❌ Unknown platform: %PLATFORM%
echo Use: build.bat help for available options
exit /b 1

:end
echo.
echo Build completed!
pause 