import re
import urllib.parse
from google_images_download import google_images_download


class CustomGoogleImagesDownload(google_images_download.googleimagesdownload):
    """
    Custom class that extends googleimagesdownload to fix the _get_next_item
    function for the new Google Images HTML layout.
    """

    def _get_next_item(self, s):
        """
        Override the _get_next_item function to work with the new Google
        Images HTML layout. The new layout uses different HTML structure
        without the 'rg_meta notranslate' class.
        """
        # Try to find image links in the new HTML format
        # Looking for image URLs in href attributes that contain image data

        # Pattern to find image URLs in the new format
        # Format: href="/url?esrc=s&amp;q=...&amp;url=https://..."
        url_pattern = r'href="(/url\?[^"]*&amp;url=https?://[^"]*)"'
        matches = re.findall(url_pattern, s)

        if not matches:
            # If no URL links found, try to find direct image sources
            # Look for img src attributes
            img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
            img_matches = re.findall(img_pattern, s)

            if not img_matches:
                return "no_links", 0

            # Use the first image found
            image_url = img_matches[0]

            # Create a mock object similar to the original format
            mock_object = {
                'ou': image_url,  # image_link
                'ity': 'jpg',     # image_format
                'oh': 0,          # image_height
                'ow': 0,          # image_width
                'pt': '',         # image_description
                'rh': '',         # image_host
                'ru': image_url,  # image_source
                'tu': image_url   # image_thumbnail_url
            }

            # Find the end position for this match
            end_pos = s.find('>', s.find(img_matches[0])) + 1
            return mock_object, end_pos

        # Extract the actual image URL from the Google redirect URL
        first_match = matches[0]

        # Decode HTML entities first
        import html
        decoded_url = html.unescape(first_match)

        # Parse the URL parameter
        parsed_url = urllib.parse.urlparse(decoded_url)
        url_parts = urllib.parse.parse_qs(parsed_url.query)

        if 'url' in url_parts:
            actual_url = url_parts['url'][0]

            # Extract image format from URL
            image_format = 'jpg'  # default
            if '.' in actual_url:
                ext = actual_url.split('.')[-1].lower()
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
                    image_format = ext

            # Create object in the expected format
            final_object = {
                'ou': actual_url,     # image_link
                'ity': image_format,  # image_format
                'oh': 0,              # image_height (unknown)
                'ow': 0,              # image_width (unknown)
                'pt': '',             # image_description
                'rh': '',             # image_host
                'ru': actual_url,     # image_source
                'tu': actual_url      # image_thumbnail_url
            }

            # Find end position
            end_pos = s.find(first_match) + len(first_match)
            return final_object, end_pos

        return "no_links", 0

    def _get_next_item_alternative(self, s):
        """
        Alternative implementation that tries to parse the simplified mobile
        HTML format shown in the goog-img-test.html file.
        """
        # Look for table cells containing image links
        # Pattern: <td><a href="/url?...
        cell_pattern = r'<td[^>]*><a[^>]+href="(/url\?[^"]*)"[^>]*>'
        matches = re.findall(cell_pattern, s)

        if not matches:
            return "no_links", 0

        first_match = matches[0]

        # Extract the actual URL from the Google redirect
        try:
            parsed = urllib.parse.urlparse(first_match)
            query_params = urllib.parse.parse_qs(parsed.query)

            if 'url' in query_params:
                actual_url = query_params['url'][0]

                # Determine image format
                image_format = 'jpg'
                if '.' in actual_url:
                    parts = actual_url.split('.')
                    # Remove query params
                    potential_ext = parts[-1].lower().split('?')[0]
                    valid_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp',
                                  'webp', 'svg']
                    if potential_ext in valid_exts:
                        image_format = potential_ext

                # Create the expected object format
                final_object = {
                    'ou': actual_url,     # original URL / image_link
                    'ity': image_format,  # image type / image_format
                    'oh': 0,              # original height
                    'ow': 0,              # original width
                    'pt': '',             # page title / image_description
                    'rh': '',             # referring host / image_host
                    'ru': actual_url,     # referring URL / image_source
                    'tu': actual_url      # thumbnail URL
                }

                # Find end position to continue parsing
                end_pos = s.find(first_match) + len(first_match)
                return final_object, end_pos

        except Exception as e:
            print(f"Error parsing URL: {e}")

        return "no_links", 0

    def _get_next_item_fallback(self, s):
        """
        Fallback method that tries multiple parsing strategies
        """
        # Strategy 1: Try original method first
        try:
            result = super()._get_next_item(s)
            if result[0] != "no_links":
                return result
        except Exception:
            pass

        # Strategy 2: Try alternative method
        result = self._get_next_item_alternative(s)
        if result[0] != "no_links":
            return result

        # Strategy 3: Try basic image extraction
        img_pattern = r'<img[^>]+src="([^"]+)"[^>]*alt="[^"]*"'
        matches = re.findall(img_pattern, s)

        if matches:
            image_url = matches[0]
            # Skip Google's own images (logo, etc.)
            if 'googlelogo' not in image_url and 'google.com' not in image_url:
                mock_object = {
                    'ou': image_url,
                    'ity': 'jpg',
                    'oh': 0,
                    'ow': 0,
                    'pt': '',
                    'rh': '',
                    'ru': image_url,
                    'tu': image_url
                }
                end_pos = s.find(image_url) + len(image_url)
                return mock_object, end_pos

        return "no_links", 0
