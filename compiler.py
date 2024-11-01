import os
import sys
import subprocess
import shutil
import platform
from PIL import Image

def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def generate_icon(system_name):
    icons_dir = resource_path(os.path.join('assets', 'icons'))
    icon_png = os.path.join(icons_dir, 'app.png')  # 512x512 PNG file

    if not os.path.exists(icon_png):
        print(f"Icon PNG file not found at {icon_png}")
        sys.exit(1)

    if system_name == 'Windows':
        icon_file = os.path.join(icons_dir, 'app.ico')
        img = Image.open(icon_png)
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(icon_file, sizes=icon_sizes)
        return icon_file

    elif system_name == 'Darwin':
        icon_file = os.path.join(icons_dir, 'app.icns')
        img = Image.open(icon_png)
        iconset_dir = os.path.join(icons_dir, 'AppIcon.iconset')
        os.makedirs(iconset_dir, exist_ok=True)
        sizes = [16, 32, 64, 128, 256, 512]
        for size in sizes:
            scaled_img = img.resize((size, size), Image.LANCZOS)
            scaled_img.save(os.path.join(iconset_dir, f'icon_{size}x{size}.png'))
            # Retina sizes
            retina_size = size * 2
            scaled_img = img.resize((retina_size, retina_size), Image.LANCZOS)
            scaled_img.save(os.path.join(iconset_dir, f'icon_{size}x{size}@2x.png'))
        # Use iconutil to create .icns
        subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', icon_file])
        shutil.rmtree(iconset_dir)
        return icon_file

    else:  # Linux or other
        return icon_png

def compile_app():
    try:
        import PyInstaller
    except ImportError:
        print("Please install PyInstaller with 'pip install pyinstaller'")
        sys.exit(1)

    system = platform.system()
    if system == 'Windows':
        system_name = 'Windows'
    elif system == 'Darwin':
        system_name = 'macOS'
    else:
        system_name = 'Linux'

    # Generate icon
    icon_file = generate_icon(system)

    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Build command
    if system_name == 'Windows':
        add_data_option = '--add-data assets;assets'
    else:
        add_data_option = '--add-data assets:assets'

    cmd = [
        'pyinstaller',
        '--clean',
        '--windowed',
        '--onefile',
        '--name', 'RainSound',
        '--icon', icon_file,
        add_data_option,
        'main.py'
    ]

    # Run PyInstaller
    subprocess.run(cmd)

if __name__ == '__main__':
    compile_app()
