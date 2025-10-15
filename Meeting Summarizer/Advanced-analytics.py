# app/services/free_analytics.py
import pandas as pd
import numpy as np
from collections import Counter
import re
from typing import Dict, List, Any
import plotly.express as px
import plotly.graph_objects as go

class FreeAnalyticsEngine:
    def __init__(self):
        self.meeting_history = []
    
    async def generate_comprehensive_analytics(self, meeting_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analytics using free methods"""
        
        analytics = {
            "meeting_metrics": await self._calculate_meeting_metrics(meeting_data),
            "participant_insights": await self._analyze_participants(meeting_data),
            "content_analysis": await self._analyze_content(meeting_data),
            "temporal_patterns": await self._analyze_temporal_patterns(meeting_data),
            "engagement_score": await self._calculate_engagement(meeting_data),
            "visualizations": await self._generate_visualizations(meeting_data)
        }
        
        return analytics
    
    async def _calculate_meeting_metrics(self, data: Dict) -> Dict[str, Any]:
        """Calculate basic meeting metrics"""
        transcript = data.get('transcript', {}).get('text', '')
        duration = data.get('processing_metadata', {}).get('audio_duration', 0)
        
        words = transcript.split()
        sentences = re.split(r'[.!?]+', transcript)
        
        return {
            "duration_minutes": round(duration / 60, 2),
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if len(s.strip()) > 0]),
            "words_per_minute": len(words) / max(duration / 60, 1),
            "speaker_count": data.get('speaker_analysis', {}).get('speaker_count', 1),
            "unique_topics": len(self._extract_topics(transcript))
        }
    
    async def _analyze_participants(self, data: Dict) -> Dict[str, Any]:
        """Analyze participant behavior"""
        speaker_data = data.get('speaker_analysis', {})
        segments = speaker_data.get('segments', [])
        
        if not segments:
            return {"analysis": "Insufficient speaker data"}
        
        # Calculate speaking time distribution
        speaker_times = {}
        for segment in segments:
            speaker = segment.get('speaker', 'Unknown')
            duration = segment.get('duration', 0)
            speaker_times[speaker] = speaker_times.get(speaker, 0) + duration
        
        total_time = sum(speaker_times.values())
        
        return {
            "speaking_time_distribution": {
                speaker: {
                    "time_seconds": time,
                    "percentage": round((time / total_time) * 100, 2) if total_time > 0 else 0
                }
                for speaker, time in speaker_times.items()
            },
            "dominant_speaker": max(speaker_times.items(), key=lambda x: x[1])[0] if speaker_times else "Unknown",
            "participation_balance": self._calculate_participation_balance(speaker_times)
        }
    
    async def _analyze_content(self, data: Dict) -> Dict[str, Any]:
        """Analyze meeting content"""
        transcript = data.get('transcript', {}).get('text', '')
        
        return {
            "topic_clusters": self._cluster_topics(transcript),
            "sentiment_trend": await self._analyze_sentiment_trend(transcript),
            "keyword_evolution": self._track_keyword_evolution(transcript),
            "question_count": len(re.findall(r'\?', transcript)),
            "decision_points": self._identify_decisions(transcript)
        }
    
    async def _analyze_temporal_patterns(self, data: Dict) -> Dict[str, Any]:
        """Analyze temporal patterns in meeting"""
        segments = data.get('speaker_analysis', {}).get('segments', [])
        
        if not segments:
            return {"analysis": "No temporal data available"}
        
        # Analyze speaking patterns over time
        time_bins = np.linspace(0, max([s.get('end_time', 0) for s in segments] or [1]), 10)
        activity_by_time = []
        
        for i in range(len(time_bins)-1):
            bin_start, bin_end = time_bins[i], time_bins[i+1]
            bin_activity = sum(s.get('duration', 0) for s in segments 
                             if bin_start <= s.get('start_time', 0) < bin_end)
            activity_by_time.append(bin_activity)
        
        return {
            "activity_over_time": activity_by_time,
            "peak_activity_time": time_bins[np.argmax(activity_by_time)] if activity_by_time else 0,
            "engagement_trend": "stable"  # Simplified
        }
    
    async def _calculate_engagement(self, data: Dict) -> Dict[str, Any]:
        """Calculate meeting engagement score"""
        metrics = await self._calculate_meeting_metrics(data)
        participants = await self._analyze_participants(data)
        
        # Simple engagement formula
        word_count_score = min(metrics['word_count'] / 500, 1.0)
        speaker_balance = participants.get('participation_balance', 0.5)
        topic_diversity = min(len(metrics['unique_topics']) / 10, 1.0)
        
        engagement_score = (word_count_score + speaker_balance + topic_diversity) / 3
        
        return {
            "overall_score": round(engagement_score * 100, 1),
            "components": {
                "content_richness": round(word_count_score * 100, 1),
                "participation_balance": round(speaker_balance * 100, 1),
                "topic_diversity": round(topic_diversity * 100, 1)
            },
            "recommendations": self._generate_engagement_recommendations(engagement_score)
        }
    
    async def _generate_visualizations(self, data: Dict) -> Dict[str, Any]:
        """Generate visualization data (can be used by frontend)"""
        participants = await self._analyze_participants(data)
        temporal = await self._analyze_temporal_patterns(data)
        
        # Return data for frontend to create charts
        return {
            "speaker_pie_chart": {
                "labels": list(participants.get('speaking_time_distribution', {}).keys()),
                "values": [v['percentage'] for v in participants.get('speaking_time_distribution', {}).values()]
            },
            "activity_timeline": {
                "time_points": list(range(len(temporal.get('activity_over_time', [])))),
                "activity_levels": temporal.get('activity_over_time', [])
            },
            "engagement_radar": {
                "metrics": ["Content", "Participation", "Topics"],
                "scores": [70, 65, 80]  # Example scores
            }
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics using frequency analysis"""
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        common_words = set(['this', 'that', 'with', 'have', 'from', 'they', 'what', 'about', 'would'])
        
        word_freq = Counter([w for w in words if w not in common_words])
        return [word for word, count in word_freq.most_common(10)]
    
    def _calculate_participation_balance(self, speaker_times: Dict[str, float]) -> float:
        """Calculate how balanced participation is (0-1, where 1 is perfectly balanced)"""
        if not speaker_times:
            return 0.5
        
        times = list(speaker_times.values())
        total = sum(times)
        if total == 0:
            return 0.5
        
        # Gini coefficient (simplified) - lower is more balanced
        sorted_times = sorted(times)
        n = len(sorted_times)
        gini = sum((2 * i - n - 1) * time for i, time in enumerate(sorted_times, 1))
        gini /= (n * sum(sorted_times))
        
        return 1 - gini  # Convert to balance score
    
    def _cluster_topics(self, text: str) -> List[Dict[str, Any]]:
        """Simple topic clustering using word co-occurrence"""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 10]
        
        topics = []
        for sentence in sentences[:20]:  # Limit for performance
            words = sentence.lower().split()
            if len(words) >= 4:
                # Use the sentence as a "topic" with key words
                key_words = [w for w in words if len(w) > 3][:3]
                topics.append({
                    "topic": " ".join(key_words),
                    "representative_sentence": sentence[:100] + "...",
                    "frequency": 1
                })
        
        # Group similar topics
        merged_topics = []
        for topic in topics:
            found_similar = False
            for existing in merged_topics:
                if len(set(topic["topic"].split()) & set(existing["topic"].split())) >= 1:
                    existing["frequency"] += 1
                    found_similar = True
                    break
            if not found_similar:
                merged_topics.append(topic)
        
        return sorted(merged_topics, key=lambda x: x["frequency"], reverse=True)[:5]
    
    async def _analyze_sentiment_trend(self, text: str) -> str:
        """Simple sentiment trend analysis"""
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'happy']
        negative_words = ['bad', 'poor', 'negative', 'problem', 'issue', 'concern']
        
        positive_count = sum(1 for word in positive_words if word in text.lower())
        negative_count = sum(1 for word in negative_words if word in text.lower())
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _track_keyword_evolution(self, text: str) -> List[Dict[str, Any]]:
        """Track how keywords appear throughout the meeting"""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        # Sample keywords at different points
        sample_points = [0, len(sentences)//3, 2*len(sentences)//3, len(sentences)-1]
        evolution = []
        
        for point in sample_points:
            if point < len(sentences):
                sentence = sentences[point]
                words = [w for w in sentence.split() if len(w) > 4]
                evolution.append({
                    "position": point,
                    "keywords": words[:3],
                    "sentence_preview": sentence[:50] + "..." if len(sentence) > 50 else sentence
                })
        
        return evolution
    
    def _identify_decisions(self, text: str) -> List[str]:
        """Identify potential decision points"""
        decision_patterns = [
            r"decided to ([^.!?]+)",
            r"agreed that ([^.!?]+)", 
            r"will ([^.!?]+)",
            r"should ([^.!?]+)",
            r"going to ([^.!?]+)"
        ]
        
        decisions = []
        for pattern in decision_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            decisions.extend(matches)
        
        return decisions[:5]  # Limit to top 5
    
    def _generate_engagement_recommendations(self, score: float) -> List[str]:
        """Generate recommendations based on engagement score"""
        recommendations = []
        
        if score < 0.3:
            recommendations.extend([
                "Consider shorter, more focused meetings",
                "Encourage more participant interaction",
                "Prepare agenda to stay on topic"
            ])
        elif score < 0.7:
            recommendations.extend([
                "Good meeting structure, could improve participation balance",
                "Consider time management for more efficient discussions"
            ])
        else:
            recommendations.extend([
                "Excellent meeting engagement",
                "Maintain current participation levels"
            ])
        
        return recommendations