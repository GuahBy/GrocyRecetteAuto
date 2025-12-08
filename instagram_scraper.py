#!/usr/bin/env python3
"""
Module de scraping Instagram Reels
Utilise yt-dlp pour télécharger les vidéos et extraire les métadonnées
"""

import os
import json
import subprocess
import tempfile
from typing import Dict, Optional
from pathlib import Path


class InstagramScraper:
    def __init__(self, download_dir: str = None, cookies_file: str = None):
        """
        Initialise le scraper Instagram
        
        Args:
            download_dir: Dossier pour télécharger les vidéos (None = temp)
            cookies_file: Chemin vers le fichier cookies Instagram (optionnel)
        """
        self.download_dir = download_dir or tempfile.gettempdir()
        self.cookies_file = cookies_file
        
    def download_reel(self, url: str) -> Dict:
        """
        Télécharge un Reel Instagram et extrait les métadonnées
        
        Args:
            url: URL du Reel Instagram
            
        Returns:
            Dict avec:
                - video_path: Chemin du fichier vidéo
                - audio_path: Chemin du fichier audio
                - description: Description du post
                - title: Titre
                - uploader: Créateur
                - duration: Durée en secondes
        """
        # Créer un dossier unique pour ce téléchargement
        temp_id = os.urandom(8).hex()
        output_dir = os.path.join(self.download_dir, f"instagram_{temp_id}")
        os.makedirs(output_dir, exist_ok=True)
        
        output_template = os.path.join(output_dir, "%(id)s.%(ext)s")
        
        try:
            # Étape 1 : Extraire les métadonnées
            print("📥 Extraction des métadonnées Instagram...")
            metadata = self._extract_metadata(url)
            
            # Étape 2 : Télécharger la vidéo
            print("🎥 Téléchargement de la vidéo...")
            video_path = self._download_video(url, output_template)
            
            # Étape 3 : Extraire l'audio
            print("🎵 Extraction de l'audio...")
            audio_path = self._extract_audio(video_path)
            
            result = {
                'video_path': video_path,
                'audio_path': audio_path,
                'description': metadata.get('description', ''),
                'title': metadata.get('title', ''),
                'uploader': metadata.get('uploader', ''),
                'duration': metadata.get('duration', 0),
                'thumbnail': metadata.get('thumbnail', ''),
                'upload_date': metadata.get('upload_date', ''),
                'view_count': metadata.get('view_count', 0),
                'like_count': metadata.get('like_count', 0),
            }
            
            print(f"✓ Téléchargement terminé")
            print(f"  Vidéo : {video_path}")
            print(f"  Audio : {audio_path}")
            print(f"  Description : {result['description'][:100]}...")
            
            return result
            
        except Exception as e:
            # Nettoyer en cas d'erreur
            self._cleanup(output_dir)
            raise Exception(f"Erreur lors du téléchargement : {e}")
    
    def _extract_metadata(self, url: str) -> Dict:
        """Extrait les métadonnées sans télécharger"""
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-playlist',
        ]
        
        # Ajouter les cookies si disponibles
        if self.cookies_file and os.path.exists(self.cookies_file):
            cmd.extend(['--cookies', self.cookies_file])
        
        cmd.append(url)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            return json.loads(result.stdout)
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur yt-dlp : {e.stderr}")
        except subprocess.TimeoutExpired:
            raise Exception("Timeout lors de l'extraction des métadonnées")
    
    def _download_video(self, url: str, output_template: str) -> str:
        """Télécharge la vidéo"""
        cmd = [
            'yt-dlp',
            '-f', 'best',  # Meilleure qualité
            '--no-playlist',
            '-o', output_template,
        ]
        
        # Ajouter les cookies si disponibles
        if self.cookies_file and os.path.exists(self.cookies_file):
            cmd.extend(['--cookies', self.cookies_file])
        
        cmd.append(url)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=120
            )
            
            # Trouver le fichier téléchargé
            output_dir = os.path.dirname(output_template)
            video_files = list(Path(output_dir).glob('*.*'))
            video_files = [f for f in video_files if f.suffix not in ['.json', '.mp3', '.wav']]
            
            if not video_files:
                raise Exception("Aucun fichier vidéo trouvé après téléchargement")
            
            return str(video_files[0])
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur lors du téléchargement : {e.stderr}")
        except subprocess.TimeoutExpired:
            raise Exception("Timeout lors du téléchargement (vidéo trop longue ?)")
    
    def _extract_audio(self, video_path: str) -> str:
        """Extrait l'audio de la vidéo"""
        audio_path = os.path.splitext(video_path)[0] + '.mp3'
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',  # Pas de vidéo
            '-acodec', 'libmp3lame',
            '-ar', '16000',  # 16kHz pour Whisper
            '-ac', '1',  # Mono
            '-b:a', '64k',  # Bitrate réduit
            '-y',  # Overwrite
            audio_path
        ]
        
        try:
            subprocess.run(
                cmd,
                capture_output=True,
                check=True,
                timeout=60
            )
            
            return audio_path
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur ffmpeg : {e.stderr.decode()}")
        except subprocess.TimeoutExpired:
            raise Exception("Timeout lors de l'extraction audio")
    
    def _cleanup(self, directory: str):
        """Nettoie le dossier de téléchargement"""
        try:
            import shutil
            if os.path.exists(directory):
                shutil.rmtree(directory)
        except Exception as e:
            print(f"⚠️ Impossible de nettoyer {directory}: {e}")
    
    def cleanup_files(self, video_path: str = None, audio_path: str = None):
        """Nettoie les fichiers téléchargés"""
        try:
            if video_path and os.path.exists(video_path):
                # Nettoyer tout le dossier parent
                parent_dir = os.path.dirname(video_path)
                self._cleanup(parent_dir)
        except Exception as e:
            print(f"⚠️ Erreur de nettoyage : {e}")


# Test du module
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python instagram_scraper.py <URL_INSTAGRAM_REEL>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    scraper = InstagramScraper()
    try:
        result = scraper.download_reel(url)
        print("\n✅ Résultat :")
        print(f"Description : {result['description']}")
        print(f"Durée : {result['duration']}s")
        print(f"Créateur : {result['uploader']}")
    except Exception as e:
        print(f"❌ Erreur : {e}")
