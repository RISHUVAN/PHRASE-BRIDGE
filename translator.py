"""
Translation service module
Handles API integration with Google Translate
"""

import os
from googletrans import Translator, LANGUAGES
import requests
from typing import Optional, Tuple

class TranslationService:
    """Service class for handling translation requests"""
    
    def __init__(self):
        """Initialize the translation service"""
        self.translator = Translator()
        self.max_chars = 5000  # Character limit for translation
        
    def translate_text(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> Tuple[Optional[str], Optional[str]]:
        """
        Translate text from source language to target language
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code (default: "auto")
            target_lang (str): Target language code (default: "en")
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (translated_text, error_message)
        """
        try:
            # Check if text is empty
            if not text or not text.strip():
                return None, "Please enter text to translate"
            
            # Check character limit
            if len(text) > self.max_chars:
                return None, f"Text too long. Maximum {self.max_chars} characters allowed."
            
            # Check if source and target languages are the same
            if source_lang == target_lang and source_lang != "auto":
                return text, None
            
            # Perform translation
            result = self.translator.translate(
                text,
                src=source_lang,
                dest=target_lang
            )
            
            # Return translated text
            return result.text, None
            
        except requests.exceptions.ConnectionError:
            return None, "Network error: Please check your internet connection"
        except requests.exceptions.Timeout:
            return None, "Translation timeout: Please try again"
        except requests.exceptions.HTTPError as e:
            return None, f"Translation service error: {str(e)}"
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "too many requests" in error_msg:
                return None, "Rate limit exceeded: Please wait a moment and try again"
            elif "403" in error_msg or "forbidden" in error_msg:
                return None, "Translation service access denied: Please check your connection"
            elif "service unavailable" in error_msg:
                return None, "Translation service temporarily unavailable"
            else:
                return None, f"Translation failed: {str(e)}"
    
    def detect_language(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Detect the language of the given text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (detected_language_code, error_message)
        """
        try:
            if not text or not text.strip():
                return None, "No text provided for language detection"
            
            detection = self.translator.detect(text)
            return detection.lang, None
            
        except Exception as e:
            return None, f"Language detection failed: {str(e)}"
    
    def get_supported_languages(self) -> dict:
        """
        Get dictionary of supported languages
        
        Returns:
            dict: Dictionary mapping language codes to names
        """
        return LANGUAGES
    
    def is_service_available(self) -> bool:
        """
        Check if the translation service is available
        
        Returns:
            bool: True if service is available, False otherwise
        """
        try:
            # Try a simple translation to test service availability
            test_result = self.translator.translate("test", src="en", dest="es")
            return test_result is not None
        except:
            return False
