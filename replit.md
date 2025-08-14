# Phrase Bridge - Language Translation Desktop Application

## Overview

Phrase Bridge is a desktop translation application built with Python and Tkinter that provides real-time language translation capabilities. The application offers a clean, user-friendly GUI for translating text between multiple languages using Google Translate's API. It supports over 40 languages with automatic language detection and includes features like text copying and service availability checking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **GUI Framework**: Tkinter with ttk widgets for native desktop UI
- **Main Window**: Single-window application with resizable interface (800x600 default, 600x500 minimum)
- **Component Structure**: Modular GUI design with separated widget creation, layout setup, and event binding
- **Threading**: Asynchronous translation processing to prevent UI freezing during API calls
- **Clipboard Integration**: pyperclip library for copy/paste functionality

### Backend Architecture
- **Translation Service**: Centralized TranslationService class handling all translation logic
- **Language Management**: Dedicated language_codes module with ISO 639-1 language mappings
- **Error Handling**: Comprehensive error management with user-friendly messaging
- **Input Validation**: Text length limits (5000 character maximum) and empty input checks

### Data Management
- **Language Database**: Static dictionary mapping 40+ language names to ISO codes
- **Session State**: In-memory state management for translation status and service availability
- **No Persistent Storage**: Application operates without local data persistence

### Design Patterns
- **Separation of Concerns**: Clear separation between GUI (gui.py), translation logic (translator.py), and language data (language_codes.py)
- **Service Layer Pattern**: TranslationService abstracts translation API interactions
- **Event-Driven Architecture**: Tkinter event system for user interactions and GUI updates

## External Dependencies

### Translation API
- **Google Translate API**: googletrans library for translation services
- **Service Integration**: Automatic language detection and multi-language support
- **Rate Limiting**: Built-in handling through googletrans library

### Python Libraries
- **GUI**: tkinter (built-in), ttk for enhanced widgets
- **Clipboard**: pyperclip for system clipboard operations
- **Threading**: threading (built-in) for asynchronous operations
- **HTTP**: requests library for network connectivity checking
- **Translation**: googletrans for Google Translate API access

### System Requirements
- **Python 3.x**: Core runtime environment
- **Internet Connection**: Required for translation API access
- **Desktop Environment**: Native desktop application requiring GUI support