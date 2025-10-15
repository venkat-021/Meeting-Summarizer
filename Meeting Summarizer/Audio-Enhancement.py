# app/services/free_audio_enhancement.py
import librosa
import numpy as np
import noisereduce as nr
from scipy import signal
import soundfile as sf
from typing import Dict, Any, List

class FreeAudioEnhancer:
    def __init__(self):
        self.enhancement_methods = [
            "noise_reduction",
            "normalization", 
            "trim_silence",
            "bandpass_filter"
        ]
    
    async def enhance_audio(self, audio_path: str, methods: List[str] = None) -> Dict[str, Any]:
        """Enhance audio quality using free methods"""
        if methods is None:
            methods = self.enhancement_methods
        
        try:
            y, sr = librosa.load(audio_path, sr=16000)
            original_stats = self._get_audio_stats(y, sr)
            
            enhanced_audio = y.copy()
            applied_methods = []
            
            for method in methods:
                if method == "noise_reduction" and method in methods:
                    enhanced_audio = await self._reduce_noise(enhanced_audio, sr)
                    applied_methods.append("noise_reduction")
                
                elif method == "normalization" and method in methods:
                    enhanced_audio = await self._normalize_audio(enhanced_audio)
                    applied_methods.append("normalization")
                
                elif method == "trim_silence" and method in methods:
                    enhanced_audio = await self._trim_silence(enhanced_audio, sr)
                    applied_methods.append("trim_silence")
                
                elif method == "bandpass_filter" and method in methods:
                    enhanced_audio = await self._bandpass_filter(enhanced_audio, sr)
                    applied_methods.append("bandpass_filter")
            
            enhanced_stats = self._get_audio_stats(enhanced_audio, sr)
            
            # Save enhanced audio
            enhanced_path = audio_path.replace('.', '_enhanced.')
            sf.write(enhanced_path, enhanced_audio, sr)
            
            return {
                "enhanced_path": enhanced_path,
                "applied_methods": applied_methods,
                "improvement_metrics": {
                    "snr_improvement": enhanced_stats['snr'] - original_stats['snr'],
                    "clarity_improvement": enhanced_stats['clarity'] - original_stats['clarity']
                },
                "original_stats": original_stats,
                "enhanced_stats": enhanced_stats
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "applied_methods": [],
                "improvement_metrics": {}
            }
    
    async def _reduce_noise(self, y, sr) -> np.ndarray:
        """Reduce background noise"""
        try:
            return nr.reduce_noise(y=y, sr=sr)
        except:
            return y  # Return original if noise reduction fails
    
    async def _normalize_audio(self, y) -> np.ndarray:
        """Normalize audio volume"""
        max_val = np.max(np.abs(y))
        if max_val > 0:
            return y / max_val
        return y
    
    async def _trim_silence(self, y, sr) -> np.ndarray:
        """Trim leading and trailing silence"""
        try:
            intervals = librosa.effects.split(y, top_db=20)
            if len(intervals) > 0:
                start = intervals[0][0]
                end = intervals[-1][1]
                return y[start:end]
            return y
        except:
            return y
    
    async def _bandpass_filter(self, y, sr) -> np.ndarray:
        """Apply bandpass filter for voice frequencies (300-3400 Hz)"""
        try:
            nyquist = sr / 2
            low = 300 / nyquist
            high = 3400 / nyquist
            b, a = signal.butter(4, [low, high], btype='band')
            return signal.filtfilt(b, a, y)
        except:
            return y
    
    def _get_audio_stats(self, y, sr) -> Dict[str, float]:
        """Get audio quality statistics"""
        rms = np.sqrt(np.mean(y**2))
        snr = 20 * np.log10(rms / (np.std(y) + 1e-10)) if rms > 0 else 0
        
        # Simple clarity metric (spectral centroid)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        clarity = np.mean(spectral_centroid)
        
        return {
            "snr": float(snr),
            "clarity": float(clarity),
            "rms": float(rms),
            "duration": len(y) / sr
        }