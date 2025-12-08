#!/usr/bin/env python3
"""
Module de transcription audio avec OpenAI Whisper
Optimisé pour CPU (Xeon X3430)
"""

import os
import whisper
from typing import Dict, Optional


class AudioTranscriber:
    def __init__(self, model_name: str = "medium"):
        """
        Initialise le transcripteur Whisper
        
        Args:
            model_name: Modèle Whisper à utiliser
                - tiny: ~39M params, très rapide, moins précis
                - base: ~74M params, bon compromis
                - small: ~244M params, meilleure qualité
                - medium: ~769M params, très précis (RECOMMANDÉ)
                - large: ~1550M params, le meilleur, très lent
        """
        self.model_name = model_name
        self.model = None
        
        print(f"🎙️ Initialisation de Whisper (modèle: {model_name})...")
        print("   (Le premier lancement téléchargera le modèle)")
    
    def _load_model(self):
        """Charge le modèle Whisper (lazy loading)"""
        if self.model is None:
            print(f"📥 Chargement du modèle Whisper '{self.model_name}'...")
            self.model = whisper.load_model(self.model_name)
            print("✓ Modèle chargé")
    
    def transcribe(self, audio_path: str, language: str = "fr") -> Dict:
        """
        Transcrit un fichier audio en texte
        
        Args:
            audio_path: Chemin vers le fichier audio
            language: Langue de la transcription (fr, en, etc.)
            
        Returns:
            Dict avec:
                - text: Transcription complète
                - segments: Liste des segments avec timestamps
                - language: Langue détectée
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")
        
        # Charger le modèle si nécessaire
        self._load_model()
        
        print(f"🎤 Transcription en cours...")
        print(f"   Fichier : {audio_path}")
        print(f"   Langue : {language}")
        print(f"   (Cela peut prendre 30-60 secondes sur CPU...)")
        
        try:
            # Transcription avec Whisper
            result = self.model.transcribe(
                audio_path,
                language=language,
                task="transcribe",
                fp16=False,  # Pas de FP16 sur CPU
                verbose=False
            )
            
            text = result['text'].strip()
            
            print(f"✓ Transcription terminée")
            print(f"  Texte : {text[:100]}...")
            print(f"  Langue détectée : {result.get('language', 'N/A')}")
            
            return {
                'text': text,
                'segments': result.get('segments', []),
                'language': result.get('language', language)
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la transcription : {e}")
    
    def transcribe_segments(self, audio_path: str, language: str = "fr") -> list:
        """
        Transcrit et retourne les segments avec timestamps
        Utile pour synchroniser avec la vidéo
        
        Returns:
            Liste de dicts avec:
                - start: Timestamp début (secondes)
                - end: Timestamp fin (secondes)
                - text: Texte du segment
        """
        result = self.transcribe(audio_path, language)
        
        segments = []
        for seg in result.get('segments', []):
            segments.append({
                'start': seg.get('start', 0),
                'end': seg.get('end', 0),
                'text': seg.get('text', '').strip()
            })
        
        return segments


# Test du module
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audio_transcriber.py <AUDIO_FILE>")
        print("\nModèles disponibles:")
        print("  tiny  - Le plus rapide, moins précis (~1GB RAM)")
        print("  base  - Bon compromis (recommandé) (~1GB RAM)")
        print("  small - Meilleure qualité (~2GB RAM)")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    transcriber = AudioTranscriber(model_name=model)
    
    try:
        result = transcriber.transcribe(audio_path)
        
        print("\n" + "="*60)
        print("TRANSCRIPTION COMPLÈTE")
        print("="*60)
        print(result['text'])
        print("\n" + "="*60)
        
        if result.get('segments'):
            print("\nSEGMENTS:")
            for i, seg in enumerate(result['segments'][:5], 1):  # Afficher 5 premiers
                print(f"  [{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")
            if len(result['segments']) > 5:
                print(f"  ... et {len(result['segments']) - 5} autres segments")
                
    except Exception as e:
        print(f"❌ Erreur : {e}")
