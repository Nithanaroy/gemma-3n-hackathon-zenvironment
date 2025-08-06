import os
import glob
from custom_google_images_download import CustomGoogleImagesDownload

# Sample categories with search strings
search_data = {
    "forests": [
        "dense mossy forest trail foggy morning",
        "sunlight filtering through tall pine trees"
    ],
    "water": [
        "gentle stream flowing over rocks",
        "waves crashing on a quiet beach at sunset"
    ],
    "mountains": [
        "clear sky mountain summit view",
        "snow-covered mountain valley no footprints"
    ],
    "meadows": [
        "tall grass waving in the wind wide landscape",
        "colorful wildflower meadow under blue sky"
    ],
    "sky": [
        "clear night sky full of stars from forest",
        "sunrise with pink and orange sky over hills"
    ]
}

# Image downloader object
downloader = CustomGoogleImagesDownload()

# Directory to save images
output_dir = "nature_meditation_images"

# Number of images per search term
limit = 5


def rename_downloaded_files(output_dir, category):
    """
    Rename downloaded files in a category folder to use auto-incremental
    numbers
    """
    category_path = os.path.join(output_dir, f"output/{category}")
    
    if not os.path.exists(category_path):
        print(f"Warning: Directory {category_path} does not exist")
        return
    
    # Get all jpg files in the directory
    jpg_files = glob.glob(os.path.join(category_path, "*.jpg"))
    
    if not jpg_files:
        print(f"No JPG files found in {category_path}")
        return
    
    # Sort files by modification time to maintain download order
    jpg_files.sort(key=os.path.getmtime)
    
    # Rename files to incremental numbers
    for i, old_file in enumerate(jpg_files, 1):
        new_filename = f"{category}_{i:03d}.jpg"
        new_file_path = os.path.join(category_path, new_filename)
        
        # Only rename if the new name is different
        if old_file != new_file_path:
            try:
                os.rename(old_file, new_file_path)
                old_name = os.path.basename(old_file)
                print(f"Renamed: {old_name} -> {new_filename}")
            except OSError as e:
                print(f"Error renaming {old_file}: {e}")


# Loop through categories and download images
for category, search_terms in search_data.items():
    print(f"\n📁 Processing category: {category}")
    
    for term in search_terms:
        print(f"Downloading: {term}")
        arguments = {
            "keywords": term,
            "limit": limit,
            "print_urls": False,
            "format": "jpg",
            "output_directory": output_dir,
            "image_directory": f"output/{category}",
            "chromedriver": "chromedriver-mac-arm64/chromedriver",
            "safe_search": True
        }
        try:
            downloader.download(arguments)
        except Exception as e:
            print(f"Error downloading {term}: {e}")
    
    # Rename all files in this category to use incremental numbers
    print(f"🔄 Renaming files in {category} category...")
    rename_downloaded_files(output_dir, category)


print("\n✅ Download complete!")
