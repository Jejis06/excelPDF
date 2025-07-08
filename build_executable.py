#!/usr/bin/env python3
"""
Build script for creating executable files for the Utility Bills application.
Supports both Windows and macOS platforms using PyInstaller.

Usage:
    python build_executable.py [platform] [options]
    
    platform: windows, macos, or current (default: current)
    options: --debug, --onefile, --windowed, --clean
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
from pathlib import Path

class BuildConfig:
    """Configuration for building executables"""
    
    def __init__(self):
        self.app_name = "UtilityBills"
        self.main_script = "app.py"
        self.icon_file = "icon.svg"  # Will be converted to .ico/.icns as needed
        self.version = "1.0.0"
        self.author = "Utility Bills Team"
        self.description = "Utility Bills PDF Generator and Email Sender"
        
        # Files to include
        self.data_files = [
            ("styles.qss", "."),
            ("icon.svg", "."),
            ("appLayout.ui", "."),
            ("requirements.txt", "."),
            ("README.md", "."),
        ]
        
        # Additional modules that might not be detected automatically
        self.hidden_imports = [
            "PyQt5.sip",
            "google.auth",
            "google.oauth2",
            "google_auth_httplib2",
            "google_auth_oauthlib",
            "openpyxl",
            "pdfkit",
            "requests",
            "email.mime.multipart",
            "email.mime.text",
            "email.mime.base",
            "smtplib",
        ]
        
        # Directories to exclude to reduce size
        self.excludes = [
            "tkinter",
            "unittest", 
            "test",
            "tests",
            "matplotlib",
            "numpy",
            "scipy",
        ]

class ExecutableBuilder:
    """Main builder class for creating executables"""
    
    def __init__(self, config):
        self.config = config
        self.current_platform = platform.system().lower()
        self.project_root = Path.cwd()
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = ["PyInstaller", "PyQt5"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.lower().replace("-", "_"))
                print(f"  ✅ {package} found")
            except ImportError:
                missing_packages.append(package)
                print(f"  ❌ {package} not found")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            for package in missing_packages:
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print("✅ All dependencies installed")
        
        return True
    
    def clean_previous_builds(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        directories_to_clean = [self.dist_dir, self.build_dir]
        files_to_clean = [
            self.project_root / f"{self.config.app_name}.spec",
            self.project_root / "app.spec"
        ]
        
        for directory in directories_to_clean:
            if directory.exists():
                shutil.rmtree(directory)
                print(f"  🗑️  Removed {directory}")
        
        for file_path in files_to_clean:
            if file_path.exists():
                file_path.unlink()
                print(f"  🗑️  Removed {file_path}")
    
    def prepare_icon(self, target_platform):
        """Prepare icon file for the target platform"""
        print(f"🎨 Preparing icon for {target_platform}...")
        
        icon_source = self.project_root / self.config.icon_file
        if not icon_source.exists():
            print(f"  ⚠️  Icon file {self.config.icon_file} not found, skipping icon")
            return None
        
        if target_platform == "windows":
            # For Windows, we need .ico format
            icon_target = self.project_root / "icon.ico"
            if not icon_target.exists():
                print(f"  ℹ️  Converting SVG to ICO format...")
                # Note: This requires additional tools like Pillow or manual conversion
                print(f"  ⚠️  Please convert {icon_source} to icon.ico manually")
                print(f"  💡 You can use online converters or: pip install Pillow")
                return str(icon_source)  # Use original for now
            return str(icon_target)
        
        elif target_platform == "macos":
            # For macOS, we need .icns format
            icon_target = self.project_root / "icon.icns"
            if not icon_target.exists():
                print(f"  ℹ️  Converting SVG to ICNS format...")
                # Note: This requires iconutil on macOS
                print(f"  ⚠️  Please convert {icon_source} to icon.icns manually")
                print(f"  💡 On macOS: sips -s format icns {icon_source} --out icon.icns")
                return str(icon_source)  # Use original for now
            return str(icon_target)
        
        return str(icon_source)
    
    def build_pyinstaller_command(self, target_platform, options):
        """Build the PyInstaller command"""
        print(f"⚙️  Building PyInstaller command for {target_platform}...")
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name", self.config.app_name,
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),
        ]
        
        # Add icon
        icon_path = self.prepare_icon(target_platform)
        if icon_path:
            cmd.extend(["--icon", icon_path])
        
        # Add data files
        for src, dest in self.config.data_files:
            src_path = self.project_root / src
            if src_path.exists():
                cmd.extend(["--add-data", f"{src_path}{os.pathsep}{dest}"])
        
        # Add hidden imports
        for module in self.config.hidden_imports:
            cmd.extend(["--hidden-import", module])
        
        # Add excludes
        for exclude in self.config.excludes:
            cmd.extend(["--exclude-module", exclude])
        
        # Platform-specific options
        if target_platform == "windows":
            cmd.append("--windowed")  # No console window
            if options.onefile:
                cmd.append("--onefile")
        elif target_platform == "macos":
            cmd.append("--windowed")  # Create .app bundle
            if options.onefile:
                cmd.append("--onefile")
        
        # Debug options
        if options.debug:
            cmd.append("--debug=all")
            cmd.append("--console")  # Show console for debugging
        else:
            cmd.append("--noconsole")
        
        # Clean option
        if options.clean:
            cmd.append("--clean")
        
        # Add version info (Windows)
        if target_platform == "windows":
            version_info = self.create_version_file()
            if version_info:
                cmd.extend(["--version-file", version_info])
        
        # Main script (must be last)
        cmd.append(str(self.project_root / self.config.main_script))
        
        return cmd
    
    def create_version_file(self):
        """Create Windows version file"""
        version_file = self.project_root / "version_info.txt"
        
        version_content = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.config.version.replace('.', ', ')}, 0),
    prodvers=({self.config.version.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{self.config.author}'),
        StringStruct(u'FileDescription', u'{self.config.description}'),
        StringStruct(u'FileVersion', u'{self.config.version}'),
        StringStruct(u'InternalName', u'{self.config.app_name}'),
        StringStruct(u'LegalCopyright', u'© {self.config.author}'),
        StringStruct(u'OriginalFilename', u'{self.config.app_name}.exe'),
        StringStruct(u'ProductName', u'{self.config.app_name}'),
        StringStruct(u'ProductVersion', u'{self.config.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
        
        try:
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            print(f"  📝 Created version file: {version_file}")
            return str(version_file)
        except Exception as e:
            print(f"  ⚠️  Could not create version file: {e}")
            return None
    
    def build_executable(self, target_platform, options):
        """Build the executable for the specified platform"""
        print(f"\n🚀 Building executable for {target_platform}...")
        print(f"   Platform: {target_platform}")
        print(f"   One file: {options.onefile}")
        print(f"   Debug: {options.debug}")
        print(f"   Clean: {options.clean}")
        
        # Check if we can build for the target platform
        if target_platform != self.current_platform and target_platform != "current":
            print(f"⚠️  Cross-platform building not fully supported.")
            print(f"   Current platform: {self.current_platform}")
            print(f"   Target platform: {target_platform}")
            print(f"   Proceeding with current platform settings...")
        
        # Build command
        cmd = self.build_pyinstaller_command(target_platform, options)
        
        print(f"\n🔨 Running PyInstaller...")
        print(f"Command: {' '.join(cmd)}")
        
        try:
            # Run PyInstaller
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            print("✅ Build completed successfully!")
            
            # Show build results
            self.show_build_results(target_platform, options)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed with exit code {e.returncode}")
            print(f"Error output:\n{e.stderr}")
            return False
        
        except Exception as e:
            print(f"❌ Build failed with error: {e}")
            return False
        
        return True
    
    def show_build_results(self, target_platform, options):
        """Show information about the built executable"""
        print(f"\n📊 Build Results:")
        
        if options.onefile:
            if target_platform == "windows":
                exe_path = self.dist_dir / f"{self.config.app_name}.exe"
            elif target_platform == "macos":
                exe_path = self.dist_dir / f"{self.config.app_name}"
            else:
                exe_path = self.dist_dir / f"{self.config.app_name}"
            
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"   📱 Single executable: {exe_path}")
                print(f"   📏 Size: {size_mb:.1f} MB")
        else:
            app_dir = self.dist_dir / self.config.app_name
            if app_dir.exists():
                # Calculate total size
                total_size = sum(f.stat().st_size for f in app_dir.rglob('*') if f.is_file())
                size_mb = total_size / (1024 * 1024)
                file_count = len(list(app_dir.rglob('*')))
                
                print(f"   📁 Application directory: {app_dir}")
                print(f"   📏 Total size: {size_mb:.1f} MB")
                print(f"   📄 Files: {file_count}")
                
                # Show main executable
                if target_platform == "windows":
                    main_exe = app_dir / f"{self.config.app_name}.exe"
                elif target_platform == "macos":
                    main_exe = app_dir / f"{self.config.app_name}.app"
                    if not main_exe.exists():
                        main_exe = app_dir / f"{self.config.app_name}"
                else:
                    main_exe = app_dir / f"{self.config.app_name}"
                
                if main_exe.exists():
                    print(f"   🎯 Main executable: {main_exe.name}")
        
        print(f"\n📋 Next Steps:")
        print(f"   1. Test the executable on the target platform")
        print(f"   2. Create installer/package if needed")
        print(f"   3. Distribute to users")
        
        if target_platform == "macos":
            print(f"\n🍎 macOS Notes:")
            print(f"   • Run: codesign --force --deep --sign - {self.dist_dir}/{self.config.app_name}.app")
            print(f"   • Users may need to allow in Security & Privacy settings")
        
        if target_platform == "windows":
            print(f"\n🪟 Windows Notes:")
            print(f"   • Consider code signing for distribution")
            print(f"   • Test on different Windows versions")

def main():
    parser = argparse.ArgumentParser(description="Build executable for Utility Bills application")
    parser.add_argument("platform", nargs="?", default="current", 
                       choices=["windows", "macos", "current"],
                       help="Target platform (default: current)")
    parser.add_argument("--debug", action="store_true", help="Build with debug information")
    parser.add_argument("--onefile", action="store_true", help="Create single executable file")
    parser.add_argument("--windowed", action="store_true", help="Create windowed application (no console)")
    parser.add_argument("--clean", action="store_true", help="Clean build cache before building")
    
    args = parser.parse_args()
    
    # Determine target platform
    if args.platform == "current":
        current_system = platform.system().lower()
        if current_system == "darwin":
            target_platform = "macos"
        elif current_system == "windows":
            target_platform = "windows"
        else:
            target_platform = "linux"
    else:
        target_platform = args.platform
    
    print(f"🔧 Utility Bills Executable Builder")
    print(f"   Version: 1.0.0")
    print(f"   Target Platform: {target_platform}")
    print("="*50)
    
    # Create configuration
    config = BuildConfig()
    builder = ExecutableBuilder(config)
    
    try:
        # Check dependencies
        builder.check_dependencies()
        
        # Clean previous builds if requested
        if args.clean:
            builder.clean_previous_builds()
        
        # Build executable
        success = builder.build_executable(target_platform, args)
        
        if success:
            print(f"\n🎉 Build completed successfully!")
            return 0
        else:
            print(f"\n💥 Build failed!")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⚠️  Build cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 