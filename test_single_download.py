#!/usr/bin/env python3

from custom_google_images_download import CustomGoogleImagesDownload
import os
import shutil

# Clean up any previous test downloads
if os.path.exists('test_single_image'):
    shutil.rmtree('test_single_image')

downloader = CustomGoogleImagesDownload()

arguments = {
    'keywords': 'gentle stream flowing over rocks',
    'limit': 1,
    'format': 'jpg', 
    'output_directory': 'test_single_image',
    'image_directory': 'stream_test',
    'safe_search': True,
    'print_urls': True
}

print('Testing single image download with new implementation...')
paths, errors = downloader.download(arguments)
print(f'Downloaded {len(paths)} images with {errors} errors')

# Check if files are valid
for path_key in paths:
    for img_path in paths[path_key]:
        if os.path.exists(img_path):
            size = os.path.getsize(img_path)
            print(f'File: {img_path} - Size: {size} bytes')
            
            # Try to read first few bytes to check if it's an image
            with open(img_path, 'rb') as f:
                header = f.read(20)
                if header.startswith(b'\xff\xd8\xff'):
                    print('✅ Valid JPEG file!')
                elif header.startswith(b'\x89PNG'):
                    print('✅ Valid PNG file!')
                elif header.startswith(b'GIF'):
                    print('✅ Valid GIF file!')
                elif (header.startswith(b'<html') or
                      header.startswith(b'<!DOCTYPE')):
                    print('❌ This is an HTML file, not an image!')
                else:
                    print(f'🤔 Unknown file type: {header[:10]!r}')
