import os
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

# Loop through categories and download images
for category, search_terms in search_data.items():
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

print("\n✅ Download complete!")
