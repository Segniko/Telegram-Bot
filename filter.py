import re

def is_valid_tweet(tweet_data):
    """
    Checks if a tweet meets the criteria:
    - Has Image: Yes
    - Has Caption: Yes
    - Is Video: No
    - Is Ad: No
    - Has Links: No (Strictly no external links)
    - Contains Hashtag: #UCL
    """
    text = tweet_data.get('text', '')
    has_image = tweet_data.get('has_image', False)
    is_video = tweet_data.get('is_video', False)
    is_ad = tweet_data.get('is_ad', False)
    
    # 1. Basic Content Checks
    if not has_image:
        return False, "No image"
    if not text or len(text.strip()) == 0:
        return False, "No caption"
    if is_video:
        return False, "Is video"
    if is_ad:
        return False, "Is ad"

    # 2. Link Check (Strict)
    # Regex to find http/https links
    # We assume the scraper removes the internal media link, or we handle it here.
    # If the text still contains http/https, it's likely an external link.
    if re.search(r'https?://', text):
        return False, "Contains links"

    # 3. Hashtag Check
    if '#UCL' not in text:
        return False, "Missing #UCL hashtag"

    # 4. Time Check (48 hours)
    timestamp_str = tweet_data.get('timestamp')
    
    if not timestamp_str:
        return False, "No timestamp found"

    try:
        from datetime import datetime, timedelta, timezone
        # Twitter timestamp format: 2023-10-03T18:45:00.000Z
        try:
            tweet_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        except ValueError:
            tweet_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        
        if now - tweet_time > timedelta(hours=1):
            return False, "Older than 1 hour"
            
    except Exception as e:
        print(f"Error parsing timestamp {timestamp_str}: {e}")
        return False, f"Timestamp parse error: {e}"

    return True, "Valid"
