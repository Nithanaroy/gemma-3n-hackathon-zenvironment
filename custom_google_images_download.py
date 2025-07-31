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
        # First, try to find Google's own thumbnail URLs (often more reliable)
        thumbnail_url = self._extract_google_thumbnail_urls(s)
        if thumbnail_url:
            # Decode HTML entities
            import html
            thumbnail_url = html.unescape(thumbnail_url)
            
            print(f"✅ Using Google thumbnail URL: {thumbnail_url}")
            
            # Extract format
            image_format = 'jpg'
            if '.' in thumbnail_url:
                ext = thumbnail_url.split('.')[-1].lower().split('?')[0]
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']:
                    image_format = ext
            
            final_object = {
                'ou': thumbnail_url,
                'ity': image_format,
                'oh': 0,
                'ow': 0,
                'pt': '',
                'rh': '',
                'ru': thumbnail_url,
                'tu': thumbnail_url
            }
            
            # Find a reasonable end position
            end_pos = s.find('encrypted-tbn') + 200  # Safe offset
            return final_object, end_pos
        
        # Try to find image links in the new HTML format
        # Looking for image URLs in href attributes that contain image data

        # Pattern to find image URLs in the new format
        # Format: href="/url?esrc=s&amp;q=...&amp;url=https://..."
        url_pattern = r'href="(/url\?[^"]*&amp;url=https?://[^"]*)"'
        matches = re.findall(url_pattern, s)

        if not matches:
            # If no URL links found, try to find direct image sources
            print("🔍 No redirect URLs found, searching for direct "
                  "image URLs...")
            
            # Look for direct image URLs first
            direct_img_patterns = [
                # High-res image URLs
                (r'src="(https?://[^"]*\.'
                 r'(?:jpg|jpeg|png|gif|bmp|webp|svg)[^"]*)"'),
                # Data attributes with images
                (r'data-[^=]*="(https?://[^"]*\.'
                 r'(?:jpg|jpeg|png|gif|bmp|webp|svg)[^"]*)"'),
                # Any direct image URLs in quotes
                (r'"(https?://[^"]*\.(?:jpg|jpeg|png|gif|bmp|webp|svg)'
                 r'(?:\?[^"]*)?)"'),
            ]
            
            for pattern in direct_img_patterns:
                direct_matches = re.findall(pattern, s, re.IGNORECASE)
                if direct_matches:
                    for img_url in direct_matches:
                        # Skip Google's own images and thumbnails
                        skip_patterns = ['googlelogo', 'google.com', 'gstatic',
                                         'thumb', 'small', 'icon']
                        if any(skip in img_url.lower()
                               for skip in skip_patterns):
                            continue
                        
                        print(f"🎯 Found direct image URL: {img_url}")
                        
                        # Extract format
                        image_format = 'jpg'
                        if '.' in img_url:
                            ext = img_url.split('.')[-1].lower().split('?')[0]
                            valid_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp',
                                          'webp', 'svg']
                            if ext in valid_exts:
                                image_format = ext

                        mock_object = {
                            'ou': img_url,  # image_link
                            'ity': image_format,     # image_format
                            'oh': 0,          # image_height
                            'ow': 0,          # image_width
                            'pt': '',         # image_description
                            'rh': '',         # image_host
                            'ru': img_url,  # image_source
                            'tu': img_url   # image_thumbnail_url
                        }

                        end_pos = s.find(img_url) + len(img_url)
                        return mock_object, end_pos
            
            # Fallback to generic img src search
            print("🔍 Searching for any img src attributes...")
            img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
            img_matches = re.findall(img_pattern, s)

            if not img_matches:
                print("❌ No image sources found at all")
                return "no_links", 0

            # Use the first non-Google image found
            for image_url in img_matches:
                google_patterns = ['googlelogo', 'google.com']
                is_google_img = any(pattern in image_url
                                    for pattern in google_patterns)
                if not is_google_img:
                    print(f"📷 Using fallback img src: {image_url}")
                    
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
                    end_pos = s.find('>', s.find(image_url)) + 1
                    return mock_object, end_pos
            
            print("❌ No valid image URLs found")
            return "no_links", 0

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
            
            # Print the extracted URL for debugging
            print(f"🔍 Extracted URL: {actual_url}")
            
            # Check if this is a direct image URL or a page URL
            image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp',
                                'webp', 'svg']
            is_direct_image = any(actual_url.lower().endswith(f'.{ext}')
                                  for ext in image_extensions)

            if not is_direct_image:
                print("⚠️  WARNING: URL appears to be a webpage, "
                      "not direct image:")
                print(f"    {actual_url}")
                # Try to find actual image URLs in the remaining HTML
                return self._find_direct_image_urls(s, first_match)

            # Extract image format from URL
            image_format = 'jpg'  # default
            if '.' in actual_url:
                # Remove query params
                ext = actual_url.split('.')[-1].lower().split('?')[0]
                if ext in image_extensions:
                    image_format = ext

            print(f"✅ Valid image URL found: {actual_url}")
            print(f"   Format: {image_format}")

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

    def _find_direct_image_urls(self, s, skip_until):
        """
        Helper method to find direct image URLs when the main method
        finds webpage URLs instead of direct image URLs.
        """
        # Skip past the already processed content
        remaining_html = s[s.find(skip_until) + len(skip_until):]
        
        # Look for direct image URLs in various patterns
        patterns = [
            # Direct image URLs in data attributes
            (r'data-src="(https?://[^"]*\.'
             r'(?:jpg|jpeg|png|gif|bmp|webp|svg)[^"]*)"'),
            # Image URLs in src attributes
            r'src="(https?://[^"]*\.(?:jpg|jpeg|png|gif|bmp|webp|svg)[^"]*)"',
            # URLs ending with image extensions
            (r'"(https?://[^"]*\.(?:jpg|jpeg|png|gif|bmp|webp|svg)'
             r'(?:\?[^"]*)?)"'),
        ]

        for pattern in patterns:
            matches = re.findall(pattern, remaining_html, re.IGNORECASE)
            if matches:
                for url in matches:
                    # Skip thumbnails and tiny images
                    skip_words = ['thumb', 'small', 'icon']
                    if any(skip in url.lower() for skip in skip_words):
                        continue

                    print(f"🎯 Found direct image URL: {url}")

                    # Extract format
                    image_format = 'jpg'
                    if '.' in url:
                        ext = url.split('.')[-1].lower().split('?')[0]
                        valid_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp',
                                      'webp', 'svg']
                        if ext in valid_exts:
                            image_format = ext
                    
                    final_object = {
                        'ou': url,
                        'ity': image_format,
                        'oh': 0,
                        'ow': 0,
                        'pt': '',
                        'rh': '',
                        'ru': url,
                        'tu': url
                    }
                    
                    end_pos = s.find(skip_until) + len(skip_until) + 100
                    return final_object, end_pos
        
        print("❌ No direct image URLs found")
        return "no_links", 0

    def _extract_google_thumbnail_urls(self, s):
        """
        Extract Google's own thumbnail URLs which are often direct image URLs.
        These are typically more reliable than the linked webpage URLs.
        """
        # Google often stores thumbnail URLs in various data attributes
        thumbnail_patterns = [
            # Common Google thumbnail patterns
            r'data-src="(https://encrypted-tbn\d\.gstatic\.com/[^"]*)"',
            r'src="(https://encrypted-tbn\d\.gstatic\.com/[^"]*)"',
            # Google Lens and other direct image URLs
            r'"(https://[^"]*\.googleusercontent\.com/[^"]*)"',
            # Direct images from google servers
            r'"(https://lh\d+\.googleusercontent\.com/[^"]*)"',
            # Images from google storage
            (r'"(https://storage\.googleapis\.com/[^"]*\.'
             r'(jpg|jpeg|png|gif|webp))"'),
        ]
        
        for pattern in thumbnail_patterns:
            matches = re.findall(pattern, s, re.IGNORECASE)
            if matches:
                for match in matches:
                    # Handle tuple results from patterns with groups
                    url = match[0] if isinstance(match, tuple) else match
                    
                    # Skip very small thumbnails
                    small_sizes = ['=s24', '=s48', '=w24', '=h24']
                    if any(size in url for size in small_sizes):
                        continue
                    
                    print(f"🖼️  Found Google thumbnail: {url}")
                    
                    # Try to get a larger version by modifying URL parameters
                    if '=s' in url:
                        # Replace small size with larger size
                        url = re.sub(r'=s\d+', '=s400', url)
                        print(f"🔍 Enhanced to larger size: {url}")
                    
                    return url
        
        return None
