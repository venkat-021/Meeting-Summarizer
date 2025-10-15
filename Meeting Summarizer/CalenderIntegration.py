# app/services/free_calendar.py
import icalendar
from datetime import datetime, timedelta
import re
from typing import Dict, List, Any
import uuid

class FreeCalendarService:
    def __init__(self):
        self.event_templates = {
            "follow_up": "Follow-up: {topic}",
            "review": "Review: {topic}",
            "decision": "Decision Discussion: {topic}"
        }
    
    async def extract_events_free(self, meeting_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract calendar events from meeting content using free methods"""
        transcript = meeting_data.get('transcript', {}).get('text', '')
        summary = meeting_data.get('llm_summary', {}).get('summary', '')
        
        events = []
        
        # Extract dates and times
        date_matches = self._extract_dates(transcript + " " + summary)
        time_matches = self._extract_times(transcript + " " + summary)
        
        # Extract topics for events
        topics = self._extract_event_topics(transcript)
        
        # Create event suggestions
        for i, topic in enumerate(topics[:3]):  # Limit to 3 events
            event = {
                "event_id": str(uuid.uuid4()),
                "title": self._generate_event_title(topic),
                "description": f"Automatically generated from meeting discussion about: {topic}",
                "suggested_date": self._suggest_date(date_matches, i),
                "suggested_time": self._suggest_time(time_matches, i),
                "duration_minutes": 30,
                "confidence": 0.7 - (i * 0.1),  # Decreasing confidence
                "type": "suggested",
                "participants": []  # Could extract from transcript
            }
            events.append(event)
        
        return events
    
    async def generate_ics_file(self, events: List[Dict[str, Any]]) -> str:
        """Generate .ics file for calendar import (completely free)"""
        calendar = icalendar.Calendar()
        calendar.add('prodid', '-//Meeting Intelligence//Free Calendar//EN')
        calendar.add('version', '2.0')
        
        for event_data in events:
            event = icalendar.Event()
            event.add('summary', event_data['title'])
            event.add('description', event_data['description'])
            event.add('dtstart', event_data['suggested_date'])
            event.add('dtend', event_data['suggested_date'] + timedelta(minutes=30))
            event.add('dtstamp', datetime.now())
            event.add('uid', event_data['event_id'])
            
            calendar.add_component(event)
        
        return calendar.to_ical().decode('utf-8')
    
    def _extract_dates(self, text: str) -> List[datetime]:
        """Extract date mentions from text"""
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # MM/DD/YYYY
            r'(\d{1,2}(?:st|nd|rd|th) of \w+)',   # 1st of January
            r'(next \w+)',                         # next Monday
            r'(\w+ \d{1,2})',                      # January 15
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Simple date parsing (in real implementation, use dateparser)
                    parsed_date = datetime.now() + timedelta(days=7)  # Placeholder
                    dates.append(parsed_date)
                except:
                    continue
        
        return dates
    
    def _extract_times(self, text: str) -> List[str]:
        """Extract time mentions from text"""
        time_patterns = [
            r'(\d{1,2}:\d{2}\s*(?:AM|PM)?)',      # 2:30 PM
            r'(\d{1,2}\s*(?:AM|PM))',              # 2 PM
            r'(at \d{1,2})',                       # at 2
        ]
        
        times = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            times.extend(matches)
        
        return times
    
    def _extract_event_topics(self, text: str) -> List[str]:
        """Extract potential event topics"""
        # Look for action items and decisions
        action_phrases = [
            r'follow up on ([^.!?]+)',
            r'discuss ([^.!?]+) next',
            r'review ([^.!?]+)',
            r'meet about ([^.!?]+)'
        ]
        
        topics = []
        for pattern in action_phrases:
            matches = re.findall(pattern, text, re.IGNORECASE)
            topics.extend(matches)
        
        # Add some generic topics if none found
        if not topics:
            topics = ["Action Items", "Project Update", "Team Discussion"]
        
        return topics[:5]  # Limit topics
    
    def _generate_event_title(self, topic: str) -> str:
        """Generate event title from topic"""
        if "follow" in topic.lower():
            return f"Follow-up: {topic}"
        elif "review" in topic.lower():
            return f"Review: {topic}"
        else:
            return f"Discussion: {topic}"
    
    def _suggest_date(self, dates: List[datetime], index: int) -> datetime:
        """Suggest a date for the event"""
        if dates and index < len(dates):
            return dates[index]
        else:
            # Default: next business day
            next_day = datetime.now() + timedelta(days=1)
            # Skip weekends
            while next_day.weekday() >= 5:  # 5=Saturday, 6=Sunday
                next_day += timedelta(days=1)
            return next_day
    
    def _suggest_time(self, times: List[str], index: int) -> str:
        """Suggest a time for the event"""
        if times and index < len(times):
            return times[index]
        else:
            # Default: 10:00 AM
            return "10:00 AM"