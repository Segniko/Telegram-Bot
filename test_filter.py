import unittest
from filter import is_valid_tweet

class TestFilter(unittest.TestCase):
    def test_valid_tweet(self):
        tweet = {
            'text': 'Great match! #UCL',
            'has_image': True,
            'is_video': False,
            'is_ad': False
        }
        valid, reason = is_valid_tweet(tweet)
        self.assertTrue(valid)
        self.assertEqual(reason, "Valid")

    def test_no_image(self):
        tweet = {
            'text': 'Great match! #UCL',
            'has_image': False,
            'is_video': False,
            'is_ad': False
        }
        valid, reason = is_valid_tweet(tweet)
        self.assertFalse(valid)
        self.assertEqual(reason, "No image")

    def test_video(self):
        tweet = {
            'text': 'Great match! #UCL',
            'has_image': True,
            'is_video': True,
            'is_ad': False
        }
        valid, reason = is_valid_tweet(tweet)
        self.assertFalse(valid)
        self.assertEqual(reason, "Is video")

    def test_ad(self):
        tweet = {
            'text': 'Buy this! #UCL',
            'has_image': True,
            'is_video': False,
            'is_ad': True
        }
        valid, reason = is_valid_tweet(tweet)
        self.assertFalse(valid)
        self.assertEqual(reason, "Is ad")

    def test_links(self):
        tweet = {
            'text': 'Check this out: https://example.com #UCL',
            'has_image': True,
            'is_video': False,
            'is_ad': False
        }
        valid, reason = is_valid_tweet(tweet)
        self.assertFalse(valid)
        self.assertEqual(reason, "Contains links")

    def test_missing_hashtag(self):
        tweet = {
            'text': 'Great match!',
            'has_image': True,
            'is_video': False,
            'is_ad': False
        }
        valid, reason = is_valid_tweet(tweet)
        self.assertFalse(valid)
        self.assertEqual(reason, "Missing #UCL hashtag")

if __name__ == '__main__':
    unittest.main()
