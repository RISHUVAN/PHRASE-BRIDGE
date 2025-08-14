"""
Language codes and names for the translation application
Contains mapping between language names and their ISO codes
"""

# Dictionary mapping language names to their ISO 639-1 codes
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Dutch": "nl",
    "Polish": "pl",
    "Turkish": "tr",
    "Swedish": "sv",
    "Norwegian": "no",
    "Danish": "da",
    "Finnish": "fi",
    "Greek": "el",
    "Hebrew": "he",
    "Thai": "th",
    "Vietnamese": "vi",
    "Indonesian": "id",
    "Malay": "ms",
    "Czech": "cs",
    "Hungarian": "hu",
    "Romanian": "ro",
    "Bulgarian": "bg",
    "Croatian": "hr",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Estonian": "et",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Ukrainian": "uk",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Persian": "fa",
    "Swahili": "sw",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bosnian": "bs",
    "Catalan": "ca",
    "Filipino": "tl",
    "Galician": "gl",
    "Georgian": "ka",
    "Icelandic": "is",
    "Irish": "ga",
    "Kazakh": "kk",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Latin": "la",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Maltese": "mt",
    "Mongolian": "mn",
    "Nepali": "ne",
    "Pashto": "ps",
    "Serbian": "sr",
    "Sinhala": "si",
    "Tajik": "tg",
    "Uzbek": "uz",
    "Welsh": "cy",
    "Yiddish": "yi"
}

# Get sorted list of language names for display
def get_language_names():
    """Return sorted list of language names"""
    return sorted(LANGUAGES.keys())

# Get language code from name
def get_language_code(language_name):
    """Get ISO language code from language name"""
    return LANGUAGES.get(language_name, "en")

# Get language name from code
def get_language_name(language_code):
    """Get language name from ISO language code"""
    for name, code in LANGUAGES.items():
        if code == language_code:
            return name
    return "English"
