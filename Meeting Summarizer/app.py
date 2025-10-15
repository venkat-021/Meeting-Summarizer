import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import base64
import io

# Page configuration
st.set_page_config(
    page_title="Meeting Intelligence Platform - FREE",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .alert-critical {
        background-color: #ff6b6b;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #c92a2a;
    }
    .alert-warning {
        background-color: #ffd93d;
        color: black;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f9a826;
    }
</style>
""", unsafe_allow_html=True)

class MeetingIntelligenceApp:
    def __init__(self):
        self.api_url = "http://localhost:8000"  # Change to your API URL
        
    def run(self):
        # Sidebar
        st.sidebar.title("🎙️ Meeting Intelligence")
        st.sidebar.markdown("---")
        
        menu = st.sidebar.selectbox(
            "Navigation",
            ["🏠 Dashboard", "📊 Analyze Meeting", "📈 Analytics", "⚙️ Settings"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **Free Features:**
        - AI Transcription
        - Speaker Diarization  
        - Emotion Detection
        - Voice Authenticity
        - Content Classification
        - Smart Summarization
        - Advanced Analytics
        - Real-time Processing
        """)
        
        if menu == "🏠 Dashboard":
            self.show_dashboard()
        elif menu == "📊 Analyze Meeting":
            self.analyze_meeting()
        elif menu == "📈 Analytics":
            self.show_analytics()
        elif menu == "⚙️ Settings":
            self.show_settings()
    
    def show_dashboard(self):
        st.markdown('<h1 class="main-header">🎙️ Meeting Intelligence Platform</h1>', unsafe_allow_html=True)
        
        
        st.markdown("---")
        
        # Features grid
        st.subheader("🚀 Free AI-Powered Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🎙️ Smart Transcription</h4>
                <p>High-accuracy speech-to-text using Whisper AI</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>👥 Speaker Diarization</h4>
                <p>Automatically identify and separate speakers</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>😊 Emotion Detection</h4>
                <p>Detect emotional tone from voice and text</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>🤖 AI Voice Detection</h4>
                <p>Identify AI-generated vs human voices</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📝 Smart Summarization</h4>
                <p>Extract key points and action items</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>⚠️ Content Classification</h4>
                <p>Detect ads, spam, or normal conversation</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Advanced Analytics</h4>
                <p>Meeting insights and participation metrics</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>📅 Calendar Integration</h4>
                <p>Auto-detect and schedule follow-up meetings</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick start section
        st.markdown("---")
        st.subheader("🚀 Get Started in 30 Seconds")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("""
            **1.** Upload any audio file (meeting, podcast, interview)  
            **2.** Our AI will analyze it in real-time  
            **3.** Get professional insights and summaries  
            **4.** Export results in multiple formats  
            """)
        
        with col2:
            if st.button("🎯 Start Analyzing Now", use_container_width=True):
                st.session_state.analyze_clicked = True
                st.experimental_rerun()
    
    def analyze_meeting(self):
        st.title("📊 Analyze Meeting Audio")
        
        # File upload section
        uploaded_file = st.file_uploader(
            "Upload Audio File", 
            type=['wav', 'mp3', 'm4a', 'ogg', 'flac'],
            help="Supported formats: WAV, MP3, M4A, OGG, FLAC"
        )
        
        if uploaded_file is not None:
            # Show file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name)
            with col2:
                st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024 / 1024:.2f} MB")
            with col3:
                st.metric("File Type", uploaded_file.type)
            
            # Analysis options
            st.subheader("🔧 Analysis Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                transcribe = st.checkbox("Transcription", value=True)
                emotion = st.checkbox("Emotion Analysis", value=True)
            with col2:
                speakers = st.checkbox("Speaker Detection", value=True)
                authenticity = st.checkbox("Voice Authenticity", value=True)
            with col3:
                content = st.checkbox("Content Classification", value=True)
                summary = st.checkbox("AI Summary", value=True)
            
            # Process button
            if st.button("🚀 Analyze Audio", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing your audio... This may take a few moments."):
                    try:
                        # Send to API
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{self.api_url}/analyze-audio-free/", files=files)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.analysis_result = result
                            st.success("✅ Analysis Complete!")
                            st.experimental_rerun()
                        else:
                            st.error(f"❌ Analysis failed: {response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # Display results if available
        if 'analysis_result' in st.session_state:
            self.display_analysis_results(st.session_state.analysis_result)
    
    def display_analysis_results(self, result):
        st.markdown("---")
        st.title("📋 Analysis Results")
        
        # Summary Card
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            duration = result.get('processing_metadata', {}).get('audio_duration', 0)
            st.metric("Duration", f"{duration:.1f}s")
        
        with col2:
            speakers = result.get('speaker_analysis', {}).get('speaker_count', 1)
            st.metric("Speakers", speakers)
        
        with col3:
            emotion = result.get('emotion_analysis', {}).get('primary_emotion', 'Unknown')
            st.metric("Primary Emotion", emotion.capitalize())
        
        with col4:
            is_ai = result.get('voice_authenticity', {}).get('is_ai_voice', False)
            ai_status = "🤖 AI" if is_ai else "👤 Human"
            st.metric("Voice Type", ai_status)
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📝 Summary", "🎙️ Transcript", "😊 Emotions", "👥 Speakers", 
            "🔍 Details", "📤 Export"
        ])
        
        with tab1:
            self.display_summary_tab(result)
        
        with tab2:
            self.display_transcript_tab(result)
        
        with tab3:
            self.display_emotions_tab(result)
        
        with tab4:
            self.display_speakers_tab(result)
        
        with tab5:
            self.display_details_tab(result)
        
        with tab6:
            self.display_export_tab(result)
    
    def display_summary_tab(self, result):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Executive Summary")
            summary = result.get('llm_summary', {}).get('summary', 'No summary available')
            st.write(summary)
            
            st.subheader("✅ Action Items")
            action_items = result.get('llm_summary', {}).get('action_items', [])
            if action_items:
                for i, item in enumerate(action_items, 1):
                    st.write(f"{i}. {item}")
            else:
                st.info("No specific action items detected")
        
        with col2:
            st.subheader("⚠️ Alerts & Insights")
            
            # Voice authenticity alert
            authenticity = result.get('voice_authenticity', {})
            if authenticity.get('is_ai_voice', False):
                confidence = authenticity.get('ai_confidence', 0) * 100
                st.warning(f"🤖 AI Voice Detected ({confidence:.1f}% confidence)")
            
            # Content classification
            content = result.get('content_classification', {})
            if content.get('content_type') != 'normal':
                content_type = content.get('content_type', 'unknown').title()
                st.info(f"📢 Content Type: {content_type}")
            
            # Key metrics
            st.subheader("📊 Quick Stats")
            stats_data = {
                "Metric": ["Word Count", "Speaking Rate", "Emotion Intensity", "Confidence"],
                "Value": [
                    len(result.get('transcript', {}).get('text', '').split()),
                    "Medium",  # Simplified
                    "High" if result.get('emotion_analysis', {}).get('emotional_intensity', 0) > 0.7 else "Medium",
                    f"{result.get('confidence_score', 0) * 100:.1f}%"
                ]
            }
            st.dataframe(pd.DataFrame(stats_data), use_container_width=True)
    
    def display_transcript_tab(self, result):
        transcript = result.get('transcript', {}).get('text', 'No transcript available')
        
        st.subheader("🎙️ Full Transcript")
        st.text_area("Transcript", transcript, height=300, label_visibility="collapsed")
        
        # Speaker segments if available
        segments = result.get('speaker_analysis', {}).get('segments', [])
        if segments:
            st.subheader("👥 Speaker Timeline")
            
            segment_data = []
            for segment in segments[:10]:  # Show first 10 segments
                segment_data.append({
                    "Speaker": segment.get('speaker', 'Unknown'),
                    "Start": f"{segment.get('start_time', 0):.1f}s",
                    "End": f"{segment.get('end_time', 0):.1f}s", 
                    "Duration": f"{segment.get('duration', 0):.1f}s"
                })
            
            if segment_data:
                st.dataframe(pd.DataFrame(segment_data), use_container_width=True)
    
    def display_emotions_tab(self, result):
        emotion_data = result.get('emotion_analysis', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("😊 Emotion Breakdown")
            
            if 'emotion_breakdown' in emotion_data:
                emotions = emotion_data['emotion_breakdown']
                
                # Create emotion chart
                fig = px.pie(
                    values=list(emotions.values()),
                    names=list(emotions.keys()),
                    title="Emotion Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Detailed emotion breakdown not available")
        
        with col2:
            st.subheader("📈 Sentiment Analysis")
            
            sentiment = emotion_data.get('sentiment', {})
            sentiment_label = sentiment.get('label', 'Neutral')
            sentiment_score = sentiment.get('score', 0.5) * 100
            
            # Sentiment gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = sentiment_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"Sentiment: {sentiment_label}"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightcoral"},
                        {'range': [30, 70], 'color': "lightyellow"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
    
    def display_speakers_tab(self, result):
        speaker_data = result.get('speaker_analysis', {})
        speakers = speaker_data.get('speakers', [])
        
        if speakers:
            st.subheader("👥 Speaker Analysis")
            
            # Speaker distribution
            speaker_names = [s['speaker_id'] for s in speakers]
            segment_counts = [s['segments_count'] for s in speakers]
            
            fig = px.bar(
                x=speaker_names,
                y=segment_counts,
                title="Speaking Segments per Speaker",
                labels={'x': 'Speaker', 'y': 'Number of Segments'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Speaker details table
            speaker_table = []
            for speaker in speakers:
                speaker_table.append({
                    "Speaker ID": speaker['speaker_id'],
                    "Segments": speaker['segments_count'],
                    "Confidence": "High"  # Simplified
                })
            
            st.dataframe(pd.DataFrame(speaker_table), use_container_width=True)
        else:
            st.info("Detailed speaker analysis not available")
    
    def display_details_tab(self, result):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 Voice Authenticity")
            authenticity = result.get('voice_authenticity', {})
            
            if authenticity:
                is_ai = authenticity.get('is_ai_voice', False)
                confidence = authenticity.get('confidence', 0) * 100
                
                st.metric("Voice Type", "🤖 AI Generated" if is_ai else "👤 Human")
                st.metric("Confidence", f"{confidence:.1f}%")
                st.metric("Detection Method", authenticity.get('detection_method', 'Unknown'))
                
                # Features table
                features = authenticity.get('features', {})
                if features:
                    feature_data = {"Feature": list(features.keys()), "Value": list(features.values())}
                    st.dataframe(pd.DataFrame(feature_data), use_container_width=True)
        
        with col2:
            st.subheader("📄 Content Classification")
            content = result.get('content_classification', {})
            
            if content:
                content_type = content.get('content_type', 'unknown').title()
                confidence = content.get('confidence', 0) * 100
                
                st.metric("Content Type", content_type)
                st.metric("Confidence", f"{confidence:.1f}%")
                st.metric("Spam Score", f"{content.get('spam_score', 0) * 100:.1f}%")
                st.metric("Ad Score", f"{content.get('ad_score', 0) * 100:.1f}%")
                
                reasoning = content.get('reasoning', '')
                if reasoning:
                    st.text_area("Classification Reasoning", reasoning, height=100)
    
    def display_export_tab(self, result):
        st.subheader("📤 Export Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as JSON", use_container_width=True):
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Export as CSV", use_container_width=True):
                # Create simplified CSV
                csv_data = {
                    'Metric': ['Duration', 'Speakers', 'Primary Emotion', 'Voice Type', 'Content Type'],
                    'Value': [
                        f"{result.get('processing_metadata', {}).get('audio_duration', 0):.1f}s",
                        result.get('speaker_analysis', {}).get('speaker_count', 1),
                        result.get('emotion_analysis', {}).get('primary_emotion', 'Unknown'),
                        'AI' if result.get('voice_authenticity', {}).get('is_ai_voice', False) else 'Human',
                        result.get('content_classification', {}).get('content_type', 'Unknown')
                    ]
                }
                df = pd.DataFrame(csv_data)
                csv_str = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV", 
                    data=csv_str,
                    file_name=f"meeting_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("📝 Export as Text", use_container_width=True):
                # Create text report
                text_report = f"""
MEETING INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

SUMMARY:
{result.get('llm_summary', {}).get('summary', 'No summary available')}

KEY METRICS:
- Duration: {result.get('processing_metadata', {}).get('audio_duration', 0):.1f} seconds
- Speakers: {result.get('speaker_analysis', {}).get('speaker_count', 1)}
- Primary Emotion: {result.get('emotion_analysis', {}).get('primary_emotion', 'Unknown')}
- Voice Type: {'AI' if result.get('voice_authenticity', {}).get('is_ai_voice', False) else 'Human'}

ACTION ITEMS:
"""
                action_items = result.get('llm_summary', {}).get('action_items', [])
                for i, item in enumerate(action_items, 1):
                    text_report += f"{i}. {item}\n"
                
                st.download_button(
                    label="📥 Download Text Report",
                    data=text_report,
                    file_name=f"meeting_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
        
        st.markdown("---")
        st.subheader("🔄 API Access")
        st.code(f"POST {self.api_url}/analyze-audio-free/", language="bash")
        st.info("Use the API directly for integration with other applications")
    
    def show_analytics(self):
        st.title("📈 Analytics & Insights")
        st.info("📊 Historical analytics and trends will appear here as you analyze more meetings")
        
        # Placeholder analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Meeting Duration Trends")
            # Sample data
            duration_data = pd.DataFrame({
                'Date': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                'Avg Duration (min)': [25, 30, 28, 35, 32]
            })
            st.line_chart(duration_data.set_index('Date'))
        
        with col2:
            st.subheader("Emotion Distribution")
            emotion_data = pd.DataFrame({
                'Emotion': ['Positive', 'Neutral', 'Negative'],
                'Percentage': [45, 35, 20]
            })
            st.bar_chart(emotion_data.set_index('Emotion'))
    
    def show_settings(self):
        st.title("⚙️ Settings")
        
        st.subheader("🔑 API Configuration")
        
        with st.form("api_config"):
            google_api_key = st.text_input("Google AI API Key", type="password", 
                                         help="Get from https://makersuite.google.com/app/apikey")
            perplexity_api_key = st.text_input("Perplexity API Key", type="password",
                                             help="Get from https://www.perplexity.ai/settings/api")
            
            if st.form_submit_button("💾 Save Settings"):
                st.success("✅ Settings saved! (In a real app, these would be stored securely)")
        
        st.subheader("🎛️ Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Enable real-time processing", value=True)
            st.checkbox("Auto-detect speakers", value=True)
            st.checkbox("Generate detailed transcripts", value=True)
        
        with col2:
            st.checkbox("Enable emotion analysis", value=True)
            st.checkbox("Check voice authenticity", value=True)
            st.checkbox("Auto-export results", value=False)
        
        st.subheader("ℹ️ System Information")
        st.code("""
Meeting Intelligence Platform - FREE Version
Version: 2.0.0
Status: ✅ Operational
Cost: $0/month
Models: Whisper, SpeechBrain, Gemini, PyAnnote
        """)

# Run the app
if __name__ == "__main__":
    app = MeetingIntelligenceApp()
    app.run()