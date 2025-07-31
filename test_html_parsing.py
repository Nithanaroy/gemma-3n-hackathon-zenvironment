#!/usr/bin/env python3
"""
Direct test of the _get_next_item function using the provided HTML sample
"""

from custom_google_images_download import CustomGoogleImagesDownload


def test_html_parsing():
    """Test the HTML parsing with the provided goog-img-test.html content"""
    
    # Read the HTML file
    try:
        with open('goog-img-test.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: goog-img-test.html not found")
        return
    
    # Initialize the custom downloader
    downloader = CustomGoogleImagesDownload()
    
    print("Testing HTML parsing with goog-img-test.html...")
    print("=" * 50)
    
    # Test the main _get_next_item method
    print("Testing main _get_next_item method:")
    result, end_pos = downloader._get_next_item(html_content)
    
    if result != "no_links":
        print("✅ Successfully parsed an image!")
        print(f"Image URL: {result.get('ou', 'N/A')}")
        print(f"Image format: {result.get('ity', 'N/A')}")
        print(f"Source: {result.get('ru', 'N/A')}")
        print(f"End position: {end_pos}")
    else:
        print("❌ No links found with main method")
    
    print("\n" + "-" * 50)
    
    # Test the alternative method
    print("Testing alternative _get_next_item_alternative method:")
    result_alt, end_pos_alt = downloader._get_next_item_alternative(
        html_content)

    if result_alt != "no_links":
        print("✅ Successfully parsed an image with alternative method!")
        print(f"Image URL: {result_alt.get('ou', 'N/A')}")
        print(f"Image format: {result_alt.get('ity', 'N/A')}")
        print(f"Source: {result_alt.get('ru', 'N/A')}")
        print(f"End position: {end_pos_alt}")
    else:
        print("❌ No links found with alternative method")

    print("\n" + "-" * 50)

    # Test the fallback method
    print("Testing fallback method:")
    result_fallback, end_pos_fallback = downloader._get_next_item_fallback(
        html_content)
    
    if result_fallback != "no_links":
        print("✅ Successfully parsed an image with fallback method!")
        print(f"Image URL: {result_fallback.get('ou', 'N/A')}")
        print(f"Image format: {result_fallback.get('ity', 'N/A')}")
        print(f"Source: {result_fallback.get('ru', 'N/A')}")
        print(f"End position: {end_pos_fallback}")
    else:
        print("❌ No links found with fallback method")


if __name__ == "__main__":
    test_html_parsing()
