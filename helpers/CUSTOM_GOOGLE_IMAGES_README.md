# Custom Google Images Download

This custom implementation fixes the `_get_next_item` function in the `google_images_download` library to work with Google's updated HTML layout.

## Problem

The original `google_images_download` library stopped working because Google changed their image search HTML structure. The old implementation looked for `rg_meta notranslate` classes containing JSON data, but the new format uses different HTML patterns.

## Solution

This custom implementation (`CustomGoogleImagesDownload`) extends the original library and overrides the `_get_next_item` function to:

1. Parse the new HTML format that uses `href="/url?..."` patterns
2. Handle HTML entity encoding (`&amp;` instead of `&`)
3. Extract actual image URLs from Google's redirect URLs
4. Maintain compatibility with the original library's interface

## Files

- `custom_google_images_download.py` - The main custom implementation
- `data_downloader.py` - Updated to use the custom implementation
- `test_custom_downloader.py` - Test script for the custom downloader
- `test_html_parsing.py` - Direct test of HTML parsing functionality

## Key Features

### Main Parsing Method
The primary `_get_next_item` method:
- Searches for URLs in the pattern: `href="/url?...&amp;url=https://..."`
- Decodes HTML entities using `html.unescape()`
- Extracts the actual image URL from Google's redirect parameters
- Determines image format from file extension

### Alternative Methods
- `_get_next_item_alternative()` - Alternative parsing strategy
- `_get_next_item_fallback()` - Multiple fallback strategies including the original method

### Error Handling
- Graceful fallback when parsing fails
- Maintains original error format for compatibility
- Handles various URL encoding scenarios

## Usage

```python
from custom_google_images_download import CustomGoogleImagesDownload

# Create downloader instance
downloader = CustomGoogleImagesDownload()

# Use exactly like the original library
arguments = {
    "keywords": "gentle stream flowing over rocks",
    "limit": 5,
    "format": "jpg",
    "output_directory": "downloads"
}

paths, errors = downloader.download(arguments)
```

## Testing

### Test HTML Parsing
```bash
python test_html_parsing.py
```

### Test Full Download
```bash
python test_custom_downloader.py
```

### Test Your Data Downloader
```bash
python data_downloader.py
```

## HTML Format Analysis

The new Google Images HTML uses this structure:
```html
<td><a href="/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url=https://actual-image-site.com/image.jpg&amp;ved=...">
```

Key differences from old format:
- No `rg_meta notranslate` divs with JSON
- Image URLs embedded in redirect links
- HTML entity encoding (`&amp;` instead of `&`)
- Multiple redirect parameters to parse

## Compatibility

- Maintains full compatibility with original `google_images_download` library
- All original parameters and methods work unchanged
- Can be used as a drop-in replacement
- Preserves original return format and error handling

## Notes

- Some image URLs may still fail due to rate limiting or access restrictions
- The implementation handles both direct image URLs and redirect URLs
- Error messages are preserved for debugging
- Works with the mobile HTML format that Google sometimes returns
