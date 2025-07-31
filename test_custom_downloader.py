#!/usr/bin/env python3
"""
Test script to verify the custom Google Images download functionality
"""

from custom_google_images_download import CustomGoogleImagesDownload
import os


def test_custom_downloader():
    """Test the custom downloader with a simple search"""

    # Create test directory
    test_dir = "test_downloads"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Initialize custom downloader
    downloader = CustomGoogleImagesDownload()

    # Test arguments
    arguments = {
        "keywords": "gentle stream flowing over rocks",
        "limit": 2,  # Just test with 2 images
        "print_urls": True,
        "format": "jpg",
        "output_directory": test_dir,
        "image_directory": "test_stream",
        "safe_search": True,
        "no_download": True  # Just test URL extraction first
    }

    print("Testing custom Google Images downloader...")
    print(f"Search term: {arguments['keywords']}")
    print(f"Limit: {arguments['limit']}")
    print("=" * 50)

    try:
        # Test the download function
        paths, errors = downloader.download(arguments)

        print("\nResults:")
        print(f"Paths found: {len(paths)}")
        print(f"Errors: {errors}")

        if paths:
            print("\nSuccessfully found image URLs!")
            for path in paths:
                print(f"- {path}")
        else:
            print("No image URLs found. The parsing might need adjustment.")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_custom_downloader()
