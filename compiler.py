# compiler.py

import os
import sys
import subprocess
import shutil
import platform
from PIL import Image
import argparse

def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def generate_icon():
    icons_dir = resource_path(os.path.join('assets', 'icons'))
    icon_png = os.path.join(icons_dir, 'app.png')  # 512x512 PNG file

    if not os.path.exists(icon_png):
        print(f"Icon PNG file not found at {icon_png}")
        sys.exit(1)

    system = platform.system()

    if system == 'Windows':
        icon_file = os.path.join(icons_dir, 'app.ico')
        img = Image.open(icon_png)
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(icon_file, sizes=icon_sizes)
        print(f"Generated ICO icon at {icon_file}")

    elif system == 'Darwin':
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
        result = subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', icon_file], check=True)
        if result.returncode != 0:
            print("Error generating .icns file")
            sys.exit(1)
        shutil.rmtree(iconset_dir)
        print(f"Generated ICNS icon at {icon_file}")

    else:  # Linux or other
        print(f"No icon conversion needed for {system}")

def main():
    parser = argparse.ArgumentParser(description='Compiler script for Rainy app.')
    parser.add_argument('--generate-icon', action='store_true', help='Generate icons for the current platform.')
    args = parser.parse_args()

    if args.generate_icon:
        generate_icon()
    else:
        print("No action specified. Use --generate-icon to generate icons.")

if __name__ == '__main__':
    main()
