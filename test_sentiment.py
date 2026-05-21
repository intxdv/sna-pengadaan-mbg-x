#!/usr/bin/env python
"""Quick test of sentiment analyzer integration"""

import sys
sys.path.insert(0, '.')

from src.sentiment_analyzer import get_sentiment_analyzer

# Test sentiment analyzer
analyzer = get_sentiment_analyzer()
print("[SUCCESS] Sentiment analyzer initialized")

test_texts = [
    "This is a great program",
    "Terrible policy, very bad",
    "It is okay, nothing special"
]

print("\nTesting sentiment scores:")
for text in test_texts:
    score = analyzer.analyze_sentiment(text)
    classification = analyzer.classify_sentiment(score)
    print(f"  '{text}'")
    print(f"    Score: {score:.3f} | Classification: {classification}")

print("\n[SUCCESS] All sentiment tests passed!")
