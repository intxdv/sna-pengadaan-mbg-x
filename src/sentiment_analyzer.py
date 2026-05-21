"""
Sentiment Analysis Module
Analyzes sentiment of text mentions and provides sentiment-based metrics
"""

import logging
from typing import Dict, Tuple, List
import numpy as np

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    
try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None


class SentimentAnalyzer:
    """Analyze sentiment of text data using TextBlob"""
    
    POSITIVE_THRESHOLD = 0.05      # sentiment_score > 0.05
    NEGATIVE_THRESHOLD = -0.05     # sentiment_score < -0.05
    NEUTRAL_RANGE = (-0.05, 0.05)  # between thresholds
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize sentiment analyzer
        
        Args:
            logger: Optional logger for messages
        """
        self.logger = logger or logging.getLogger(__name__)
        
        # Phase 3 warning for Indonesian text limitation
        self.logger.warning(
            "========================================================================\n"
            "⚠️ PHASE 3 SENTIMENT ANALYSIS WARNING (INCOMPLETE & EXPERIMENTAL) ⚠️\n"
            "The current lexicon engines (VADER & TextBlob) only support English text.\n"
            "Analyzing Indonesian tweets will result in unrecognized vocabulary and default\n"
            "to a 0.0 score (100% Neutral). Phase 3 is NOT fully implemented.\n"
            "Future roadmap plans include implementing IndoBERT or integrating Google Translate.\n"
            "========================================================================"
        )
        
        # Initialize VADER (preferred for social media)
        self.vader_available = VADER_AVAILABLE
        if self.vader_available:
            self.sia = SentimentIntensityAnalyzer()
            self.logger.debug("VADER sentiment analyzer initialized")
        else:
            self.logger.warning("VADER not available")
        
        # Fallback to TextBlob if VADER not available
        self.textblob_available = TextBlob is not None
        if not self.vader_available and not self.textblob_available:
            self.logger.warning("No sentiment analyzer available. Install: pip install nltk")

    
    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text using VADER (preferred) or TextBlob
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment score from -1.0 (very negative) to 1.0 (very positive)
            
        Raises:
            ValueError: If text is empty or not string
        """
        if not isinstance(text, str):
            raise ValueError(f"Expected str, got {type(text)}")
        
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Try VADER first (better for social media)
        if self.vader_available:
            try:
                scores = self.sia.polarity_scores(text)
                # VADER compound score already in [-1, 1] range
                return float(scores['compound'])
            except Exception as e:
                self.logger.debug(f"VADER error: {e}, trying TextBlob")
        
        # Fallback to TextBlob
        if self.textblob_available:
            try:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                return max(-1.0, min(1.0, polarity))
            except Exception as e:
                self.logger.warning(f"TextBlob error: {e}")
                return 0.0
        
        # No analyzer available
        self.logger.warning("No sentiment analyzer available, returning 0.0")
        return 0.0
    
    def classify_sentiment(self, sentiment_score: float) -> str:
        """
        Classify sentiment score into category
        
        Args:
            sentiment_score: Score from -1.0 to 1.0
            
        Returns:
            Category: 'positive', 'negative', or 'neutral'
        """
        if sentiment_score > self.POSITIVE_THRESHOLD:
            return 'positive'
        elif sentiment_score < self.NEGATIVE_THRESHOLD:
            return 'negative'
        else:
            return 'neutral'
    
    def batch_analyze(self, texts: List[str]) -> Dict[str, any]:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of text strings
            
        Returns:
            Dictionary with:
            - scores: List of sentiment scores
            - classifications: List of classifications
            - statistics: Dict of aggregated stats
        """
        scores = []
        classifications = []
        
        for text in texts:
            try:
                score = self.analyze_sentiment(text)
                scores.append(score)
                classifications.append(self.classify_sentiment(score))
            except (ValueError, Exception) as e:
                self.logger.debug(f"Skipping text: {e}")
                scores.append(0.0)
                classifications.append('neutral')
        
        # Calculate statistics
        scores_array = np.array(scores)
        stats = {
            'mean': float(np.mean(scores_array)),
            'median': float(np.median(scores_array)),
            'std': float(np.std(scores_array)),
            'min': float(np.min(scores_array)),
            'max': float(np.max(scores_array)),
            'positive_count': sum(1 for c in classifications if c == 'positive'),
            'negative_count': sum(1 for c in classifications if c == 'negative'),
            'neutral_count': sum(1 for c in classifications if c == 'neutral'),
        }
        
        return {
            'scores': scores,
            'classifications': classifications,
            'statistics': stats
        }
    
    def community_sentiment_summary(self, df, community_col='community', 
                                    text_col='cleaned_text', 
                                    sentiment_col='sentiment_score') -> Dict:
        """
        Summarize sentiment by community
        
        Args:
            df: DataFrame with community and text columns
            community_col: Name of community column
            text_col: Name of text column
            sentiment_col: Name of sentiment score column (will be created)
            
        Returns:
            DataFrame with community sentiment statistics
        """
        # Calculate sentiment if not present
        if sentiment_col not in df.columns:
            df[sentiment_col] = df[text_col].apply(self.analyze_sentiment)
        
        # Group by community
        community_stats = []
        
        for community_id in df[community_col].unique():
            comm_data = df[df[community_col] == community_id]
            sentiments = comm_data[sentiment_col]
            
            stats = {
                'community': community_id,
                'mean_sentiment': float(sentiments.mean()),
                'median_sentiment': float(sentiments.median()),
                'std_sentiment': float(sentiments.std()),
                'positive_ratio': float((sentiments > self.POSITIVE_THRESHOLD).sum() / len(sentiments)),
                'negative_ratio': float((sentiments < self.NEGATIVE_THRESHOLD).sum() / len(sentiments)),
                'mention_count': len(comm_data),
            }
            community_stats.append(stats)
        
        return community_stats
    
    def influencer_sentiment_profile(self, df, actor_col='target', 
                                     text_col='cleaned_text',
                                     sentiment_col='sentiment_score',
                                     top_n=10) -> List[Dict]:
        """
        Get sentiment profile of top influencers
        
        Args:
            df: DataFrame with actor and text columns
            actor_col: Name of actor/influencer column
            text_col: Name of text column
            sentiment_col: Name of sentiment score column
            top_n: Number of top influencers to return
            
        Returns:
            List of dicts with influencer sentiment profiles
        """
        # Calculate sentiment if not present
        if sentiment_col not in df.columns:
            df[sentiment_col] = df[text_col].apply(self.analyze_sentiment)
        
        # Group by actor
        actor_stats = []
        
        for actor in df[actor_col].unique():
            actor_data = df[df[actor_col] == actor]
            sentiments = actor_data[sentiment_col]
            
            if len(sentiments) > 0:
                stats = {
                    'actor': actor,
                    'mean_sentiment': float(sentiments.mean()),
                    'mention_count': len(actor_data),
                    'positive_mentions': int((sentiments > self.POSITIVE_THRESHOLD).sum()),
                    'negative_mentions': int((sentiments < self.NEGATIVE_THRESHOLD).sum()),
                    'positive_ratio': float((sentiments > self.POSITIVE_THRESHOLD).sum() / len(sentiments)),
                }
                actor_stats.append(stats)
        
        # Sort by mention count and return top N
        actor_stats = sorted(actor_stats, key=lambda x: x['mention_count'], reverse=True)
        return actor_stats[:top_n]


def get_sentiment_analyzer(logger: logging.Logger = None) -> SentimentAnalyzer:
    """
    Factory function to create sentiment analyzer
    
    Args:
        logger: Optional logger
        
    Returns:
        SentimentAnalyzer instance
    """
    return SentimentAnalyzer(logger=logger)
