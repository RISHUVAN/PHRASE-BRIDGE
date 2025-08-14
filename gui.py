"""
GUI module for the Phrase Bridge translation application
Contains the main application window and all UI components
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import pyperclip
from translator import TranslationService
from language_codes import get_language_names, get_language_code, get_language_name

class TranslationApp:
    """Main application class for the translation GUI"""
    
    def __init__(self, root):
        """Initialize the translation application"""
        self.root = root
        self.translator = TranslationService()
        self.is_translating = False
        
        # Configure the main window
        self.setup_window()
        
        # Create GUI components
        self.create_widgets()
        
        # Setup layout
        self.setup_layout()
        
        # Bind events
        self.bind_events()
        
        # Check service availability on startup
        self.check_service_availability()
    
    def setup_window(self):
        """Configure the main application window"""
        self.root.title("🌍 Phrase Bridge - Language Translator")
        self.root.geometry("900x700")
        self.root.minsize(700, 600)
        
        # Set window icon (if available)
        try:
            # This would work if we had an icon file
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
        
        # Configure modern style with colors
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define color scheme
        self.colors = {
            'primary': '#2E86AB',      # Blue
            'secondary': '#A23B72',    # Purple
            'accent': '#F18F01',       # Orange
            'success': '#C73E1D',      # Red-orange
            'background': '#F5F7FA',   # Light gray-blue
            'surface': '#FFFFFF',      # White
            'text_primary': '#2C3E50', # Dark blue-gray
            'text_secondary': '#7F8C8D', # Gray
            'border': '#E1E8ED'        # Light border
        }
        
        # Configure custom styles
        self.configure_styles(style)
        
        # Configure main window
        self.root.configure(bg=self.colors['background'])
    
    def configure_styles(self, style):
        """Configure custom TTK styles with modern colors"""
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Helvetica', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        style.map('Primary.TButton',
                 background=[('active', '#1e5a7a'),
                           ('pressed', '#1a4d66')])
        
        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Helvetica', 9),
                       borderwidth=0,
                       focuscolor='none')
        style.map('Secondary.TButton',
                 background=[('active', '#8b2e5a'),
                           ('pressed', '#742849')])
        
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Helvetica', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        style.map('Accent.TButton',
                 background=[('active', '#d67a01'),
                           ('pressed', '#b86801')])
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Primary.TLabelframe',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       font=('Helvetica', 11, 'bold'),
                       borderwidth=2,
                       relief='flat')
        style.configure('Primary.TLabelframe.Label',
                       background=self.colors['surface'],
                       foreground=self.colors['primary'],
                       font=('Helvetica', 11, 'bold'))
        
        # Configure combobox styles
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['surface'],
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='solid')
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       font=('Helvetica', 20, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text_secondary'],
                       font=('Helvetica', 10))
        
        style.configure('Status.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text_secondary'],
                       font=('Helvetica', 9),
                       relief='flat',
                       borderwidth=1)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame with modern styling
        self.main_frame = ttk.Frame(self.root, padding="20", style='Card.TFrame')
        
        # Header section
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.configure(style='Card.TFrame')
        
        # Title and subtitle
        self.title_label = ttk.Label(
            self.header_frame,
            text="🌍 Phrase Bridge",
            style='Title.TLabel'
        )
        
        self.subtitle_label = ttk.Label(
            self.header_frame,
            text="Breaking language barriers with intelligent translation",
            style='Subtitle.TLabel'
        )
        
        # Language selection frame with modern styling
        self.lang_frame = ttk.LabelFrame(
            self.main_frame, 
            text="🗣️ Language Selection", 
            padding="15",
            style='Primary.TLabelframe'
        )
        
        # Source language section with search functionality
        self.source_lang_label = ttk.Label(
            self.lang_frame, 
            text="From:",
            font=("Helvetica", 11, "bold"),
            foreground=self.colors['text_primary']
        )
        self.source_lang_var = tk.StringVar(value="Auto Detect")
        self.source_lang_combo = ttk.Combobox(
            self.lang_frame,
            textvariable=self.source_lang_var,
            values=get_language_names(),
            state="normal",  # Allow typing for search
            width=25,
            style='Modern.TCombobox',
            font=("Helvetica", 10)
        )
        
        # Animated swap languages button
        self.swap_button = ttk.Button(
            self.lang_frame,
            text="🔄",
            width=4,
            command=self.swap_languages,
            style='Accent.TButton'
        )
        
        # Target language section with search functionality
        self.target_lang_label = ttk.Label(
            self.lang_frame, 
            text="To:",
            font=("Helvetica", 11, "bold"),
            foreground=self.colors['text_primary']
        )
        self.target_lang_var = tk.StringVar(value="Spanish")
        self.target_lang_combo = ttk.Combobox(
            self.lang_frame,
            textvariable=self.target_lang_var,
            values=[lang for lang in get_language_names() if lang != "Auto Detect"],
            state="normal",  # Allow typing for search
            width=25,
            style='Modern.TCombobox',
            font=("Helvetica", 10)
        )
        
        # Input frame with modern styling
        self.input_frame = ttk.LabelFrame(
            self.main_frame, 
            text="📝 Text to Translate", 
            padding="15",
            style='Primary.TLabelframe'
        )
        
        # Input text area with custom styling
        self.input_text = scrolledtext.ScrolledText(
            self.input_frame,
            height=8,
            width=75,
            wrap=tk.WORD,
            font=("Helvetica", 12),
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            borderwidth=2,
            highlightthickness=1,
            highlightcolor=self.colors['primary']
        )
        
        # Input controls frame
        self.input_controls = ttk.Frame(self.input_frame, style='Card.TFrame')
        
        # Character count with dynamic color
        self.char_count_label = ttk.Label(
            self.input_controls,
            text="0/5000 characters",
            font=("Helvetica", 10),
            foreground=self.colors['text_secondary']
        )
        
        # Paste button
        self.paste_button = ttk.Button(
            self.input_controls,
            text="📋 Paste",
            command=self.paste_text,
            style='Secondary.TButton'
        )
        
        # Clear input button
        self.clear_input_button = ttk.Button(
            self.input_controls,
            text="🗑️ Clear",
            command=self.clear_input,
            style='Secondary.TButton'
        )
        
        # Enhanced translate button
        self.translate_button = ttk.Button(
            self.input_controls,
            text="✨ Translate",
            command=self.translate_text,
            style="Primary.TButton"
        )
        
        # Enhanced progress bar with color
        self.progress_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400,
            style='Colored.Horizontal.TProgressbar'
        )
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="🔄 Translating your text...",
            font=("Helvetica", 10, "italic"),
            foreground=self.colors['primary']
        )
        
        # Output frame with modern styling
        self.output_frame = ttk.LabelFrame(
            self.main_frame, 
            text="🎯 Translation Result", 
            padding="15",
            style='Primary.TLabelframe'
        )
        
        # Output text area with custom styling
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            height=8,
            width=75,
            wrap=tk.WORD,
            font=("Helvetica", 12),
            state=tk.DISABLED,
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['success'],
            selectforeground='white',
            relief='flat',
            borderwidth=2,
            highlightthickness=1,
            highlightcolor=self.colors['success']
        )
        
        # Output controls frame
        self.output_controls = ttk.Frame(self.output_frame, style='Card.TFrame')
        
        # Copy button with animation
        self.copy_button = ttk.Button(
            self.output_controls,
            text="📋 Copy Translation",
            command=self.copy_translation,
            state=tk.DISABLED,
            style='Accent.TButton'
        )
        
        # Clear output button
        self.clear_output_button = ttk.Button(
            self.output_controls,
            text="🗑️ Clear",
            command=self.clear_output,
            state=tk.DISABLED,
            style='Secondary.TButton'
        )
        
        # Export button
        self.export_button = ttk.Button(
            self.output_controls,
            text="💾 Save",
            command=self.save_translation,
            state=tk.DISABLED,
            style='Secondary.TButton'
        )
        
        # Enhanced status bar with modern styling
        self.status_frame = ttk.Frame(self.main_frame, style='Card.TFrame', padding="10")
        self.status_var = tk.StringVar(value="✅ Ready to translate")
        self.status_bar = ttk.Label(
            self.status_frame,
            textvariable=self.status_var,
            style='Status.TLabel',
            anchor=tk.W,
            font=("Helvetica", 10)
        )
        
        # Statistics label
        self.stats_var = tk.StringVar(value="")
        self.stats_label = ttk.Label(
            self.status_frame,
            textvariable=self.stats_var,
            style='Status.TLabel',
            anchor=tk.E,
            font=("Helvetica", 9)
        )
    
    def setup_layout(self):
        """Setup the layout of all widgets with modern spacing"""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Header section
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header_frame.columnconfigure(0, weight=1)
        
        self.title_label.grid(row=0, column=0, pady=(0, 5))
        self.subtitle_label.grid(row=1, column=0, pady=(0, 10))
        
        # Language selection
        self.lang_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.lang_frame.columnconfigure(1, weight=1)
        self.lang_frame.columnconfigure(3, weight=1)
        
        self.source_lang_label.grid(row=0, column=0, padx=(0, 8), pady=5)
        self.source_lang_combo.grid(row=0, column=1, padx=(0, 15), pady=5, sticky="ew")
        self.swap_button.grid(row=0, column=2, padx=15, pady=5)
        self.target_lang_label.grid(row=0, column=3, padx=(15, 8), pady=5)
        self.target_lang_combo.grid(row=0, column=4, padx=(0, 0), pady=5, sticky="ew")
        
        # Input frame
        self.input_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.rowconfigure(0, weight=1)
        
        self.input_text.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.input_controls.grid(row=1, column=0, sticky="ew")
        self.input_controls.columnconfigure(2, weight=1)
        
        self.char_count_label.grid(row=0, column=0, sticky="w")
        self.paste_button.grid(row=0, column=1, padx=(10, 5))
        self.clear_input_button.grid(row=0, column=3, padx=(5, 5))
        self.translate_button.grid(row=0, column=4, padx=(5, 0))
        
        # Progress frame (initially hidden)
        self.progress_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self.progress_frame.columnconfigure(0, weight=1)
        self.progress_label.grid(row=0, column=0, pady=(0, 5))
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        self.progress_frame.grid_remove()
        
        # Output frame
        self.output_frame.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)
        
        self.output_text.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.output_controls.grid(row=1, column=0, sticky="ew")
        self.output_controls.columnconfigure(2, weight=1)
        
        self.copy_button.grid(row=0, column=0, sticky="w")
        self.clear_output_button.grid(row=0, column=1, padx=(10, 5))
        self.export_button.grid(row=0, column=3, padx=(5, 0))
        
        # Status frame
        self.status_frame.grid(row=5, column=0, sticky="ew")
        self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.columnconfigure(1, weight=1)
        
        self.status_bar.grid(row=0, column=0, sticky="ew")
        self.stats_label.grid(row=0, column=1, sticky="ew")
        
        # Configure main frame row weights for expansion
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(4, weight=1)
    
    def bind_events(self):
        """Bind events to widgets"""
        # Text change events
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        self.input_text.bind('<Button-1>', self.on_text_change)
        
        # Language change events
        self.source_lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        self.target_lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Language search functionality
        self.source_lang_combo.bind('<KeyRelease>', self.on_source_lang_search)
        self.target_lang_combo.bind('<KeyRelease>', self.on_target_lang_search)
        
        # Enter key in input text
        self.input_text.bind('<Control-Return>', lambda e: self.translate_text())
        
        # Enhanced paste functionality with Ctrl+V
        self.input_text.bind('<Control-v>', self.enhanced_paste)
        self.root.bind('<Control-v>', self.global_paste_handler)
        
        # Additional keyboard shortcuts
        self.root.bind('<Control-c>', self.copy_shortcut_handler)
        self.root.bind('<F5>', lambda e: self.translate_text())
        self.root.bind('<Escape>', self.clear_focus)
    
    def on_text_change(self, event=None):
        """Handle text change in input area with enhanced visual feedback"""
        text = self.input_text.get("1.0", tk.END).strip()
        char_count = len(text)
        word_count = len(text.split()) if text else 0
        
        # Update character count with emojis and dynamic colors
        if char_count > 4500:
            self.char_count_label.config(
                text=f"⚠️ {char_count}/5000 characters • {word_count} words",
                foreground="#C73E1D"  # Red
            )
        elif char_count > 4000:
            self.char_count_label.config(
                text=f"⚡ {char_count}/5000 characters • {word_count} words",
                foreground="#F18F01"  # Orange
            )
        elif char_count > 0:
            self.char_count_label.config(
                text=f"📝 {char_count}/5000 characters • {word_count} words",
                foreground=self.colors['primary']  # Blue
            )
        else:
            self.char_count_label.config(
                text="Ready to translate...",
                foreground=self.colors['text_secondary']  # Gray
            )
        
        # Enable/disable translate button with dynamic styling
        if char_count > 0 and not self.is_translating:
            self.translate_button.config(state=tk.NORMAL)
        else:
            self.translate_button.config(state=tk.DISABLED)
    
    def on_language_change(self, event=None):
        """Handle language selection change"""
        # Update target language combo to exclude "Auto Detect"
        if self.target_lang_var.get() == "Auto Detect":
            self.target_lang_var.set("English")
    
    def on_source_lang_search(self, event=None):
        """Handle source language search as user types"""
        search_text = self.source_lang_var.get().lower()
        if search_text:
            # Filter languages that match the search text
            all_languages = get_language_names()
            filtered_languages = [lang for lang in all_languages if search_text in lang.lower()]
            self.source_lang_combo['values'] = filtered_languages
            
            # If exact match found, select it
            for lang in all_languages:
                if lang.lower() == search_text:
                    self.source_lang_var.set(lang)
                    break
        else:
            # Reset to all languages if search is empty
            self.source_lang_combo['values'] = get_language_names()
    
    def on_target_lang_search(self, event=None):
        """Handle target language search as user types"""
        search_text = self.target_lang_var.get().lower()
        if search_text:
            # Filter languages that match the search text (exclude Auto Detect)
            all_languages = [lang for lang in get_language_names() if lang != "Auto Detect"]
            filtered_languages = [lang for lang in all_languages if search_text in lang.lower()]
            self.target_lang_combo['values'] = filtered_languages
            
            # If exact match found, select it
            for lang in all_languages:
                if lang.lower() == search_text:
                    self.target_lang_var.set(lang)
                    break
        else:
            # Reset to all languages (exclude Auto Detect)
            self.target_lang_combo['values'] = [lang for lang in get_language_names() if lang != "Auto Detect"]
    
    def swap_languages(self):
        """Swap source and target languages"""
        source = self.source_lang_var.get()
        target = self.target_lang_var.get()
        
        # Don't swap if source is Auto Detect
        if source == "Auto Detect":
            return
        
        self.source_lang_var.set(target)
        self.target_lang_var.set(source)
        
        # Also swap the text content
        input_text = self.input_text.get("1.0", tk.END).strip()
        output_text = self.output_text.get("1.0", tk.END).strip()
        
        if output_text:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", output_text)
            self.clear_output()
    
    def paste_text(self):
        """Enhanced paste text from clipboard into input area"""
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                # Clear existing text and paste new content
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", clipboard_text)
                self.on_text_change()
                
                # Visual feedback for paste action
                char_count = len(clipboard_text)
                word_count = len(clipboard_text.split())
                self.update_status(f"📋 Pasted {char_count} characters ({word_count} words) from clipboard")
                
                # Brief highlight effect
                self.input_text.tag_add("paste_highlight", "1.0", tk.END)
                self.input_text.tag_config("paste_highlight", background=self.colors['accent'], foreground="white")
                self.root.after(500, lambda: self.input_text.tag_delete("paste_highlight"))
            else:
                self.update_status("📋 Clipboard is empty")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste from clipboard: {str(e)}")
    
    def enhanced_paste(self, event=None):
        """Enhanced paste handler for Ctrl+V in text area"""
        self.paste_text()
        return "break"  # Prevent default paste behavior
    
    def global_paste_handler(self, event=None):
        """Global paste handler for the entire application"""
        # Only handle if input text area has focus
        if self.root.focus_get() == self.input_text:
            self.paste_text()
            return "break"
    
    def clear_input(self):
        """Clear the input text area with animation effect"""
        self.input_text.delete("1.0", tk.END)
        self.on_text_change()
        self.update_status("🗑️ Input cleared")
    
    def clear_output(self):
        """Clear the output text area with enhanced feedback"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.copy_button.config(state=tk.DISABLED)
        self.clear_output_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.DISABLED)
        self.stats_var.set("")
        self.update_status("🗑️ Output cleared")
    
    def copy_translation(self):
        """Enhanced copy translation to clipboard with visual feedback"""
        try:
            translation = self.output_text.get("1.0", tk.END).strip()
            if translation:
                # Copy to clipboard
                pyperclip.copy(translation)
                
                # Enhanced status message with statistics
                char_count = len(translation)
                word_count = len(translation.split())
                self.update_status(f"📋 Translation copied! {char_count} characters ({word_count} words)")
                
                # Enhanced visual feedback on button
                original_text = self.copy_button.cget('text')
                original_style = self.copy_button.cget('style')
                
                self.copy_button.config(text="✅ Copied!", style='Secondary.TButton')
                
                # Add visual highlight to output text
                self.output_text.config(state=tk.NORMAL)
                self.output_text.tag_add("copy_highlight", "1.0", tk.END)
                self.output_text.tag_config("copy_highlight", background=self.colors['success'], foreground="white")
                self.output_text.config(state=tk.DISABLED)
                
                # Reset after animation
                def reset_visual():
                    self.copy_button.config(text=original_text, style=original_style)
                    self.output_text.config(state=tk.NORMAL)
                    self.output_text.tag_delete("copy_highlight")
                    self.output_text.config(state=tk.DISABLED)
                
                self.root.after(1200, reset_visual)
                
                # Optional: Show brief popup confirmation
                self.show_copy_confirmation()
            else:
                self.update_status("⚠️ No translation to copy")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def show_copy_confirmation(self):
        """Show a brief, non-intrusive copy confirmation"""
        # Create a small tooltip-like popup
        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)
        popup.configure(bg=self.colors['success'])
        
        # Position near copy button
        x = self.root.winfo_x() + self.copy_button.winfo_x() + 50
        y = self.root.winfo_y() + self.copy_button.winfo_y() - 30
        popup.geometry(f"140x30+{x}+{y}")
        
        label = tk.Label(
            popup, 
            text="✅ Copied to clipboard!", 
            bg=self.colors['success'], 
            fg="white",
            font=("Helvetica", 9, "bold")
        )
        label.pack(expand=True)
        
        # Auto-close after 1.5 seconds
        popup.after(1500, popup.destroy)
    
    def copy_shortcut_handler(self, event=None):
        """Handle Ctrl+C keyboard shortcut"""
        # Check if output text has focus and translation exists
        if self.root.focus_get() == self.output_text:
            translation = self.output_text.get("1.0", tk.END).strip()
            if translation:
                self.copy_translation()
                return "break"
        return None
    
    def clear_focus(self, event=None):
        """Clear focus from current widget and reset to input"""
        self.input_text.focus_set()
        return "break"
    
    def save_translation(self):
        """Save translation to a text file"""
        try:
            translation = self.output_text.get("1.0", tk.END).strip()
            if not translation:
                messagebox.showwarning("Warning", "No translation to save")
                return
            
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Translation"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    # Include source text and translation
                    source_text = self.input_text.get("1.0", tk.END).strip()
                    source_lang = self.source_lang_var.get()
                    target_lang = self.target_lang_var.get()
                    
                    file.write(f"Phrase Bridge Translation\n")
                    file.write(f"={'='*30}\n\n")
                    file.write(f"Source Language: {source_lang}\n")
                    file.write(f"Target Language: {target_lang}\n\n")
                    file.write(f"Original Text:\n{source_text}\n\n")
                    file.write(f"Translation:\n{translation}\n")
                    
                self.update_status(f"💾 Translation saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save translation: {str(e)}")
    
    def translate_text(self):
        """Translate the input text"""
        if self.is_translating:
            return
        
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Warning", "Please enter text to translate")
            return
        
        source_lang = get_language_code(self.source_lang_var.get())
        target_lang = get_language_code(self.target_lang_var.get())
        
        # Start translation in a separate thread
        self.start_translation()
        
        def translate():
            """Translation worker function"""
            try:
                translated_text, error = self.translator.translate_text(
                    input_text, source_lang, target_lang
                )
                
                # Update GUI in main thread
                self.root.after(0, self.translation_complete, translated_text, error)
                
            except Exception as e:
                self.root.after(0, self.translation_complete, None, str(e))
        
        # Start translation thread
        thread = threading.Thread(target=translate, daemon=True)
        thread.start()
    
    def start_translation(self):
        """Start translation UI state with enhanced visuals"""
        self.is_translating = True
        self.translate_button.config(state=tk.DISABLED, text="⏳ Translating...")
        self.progress_frame.grid()
        self.progress_bar.start(10)  # Faster animation
        self.update_status("🔄 Processing your translation...")
        
        # Update progress label with animation
        self.animate_progress_text()
    
    def animate_progress_text(self):
        """Animate progress text for better user experience"""
        if not self.is_translating:
            return
        
        messages = [
            "🔄 Translating your text...",
            "🌐 Connecting to translation service...",
            "🎯 Processing language patterns...",
            "✨ Generating translation..."
        ]
        
        current_text = self.progress_label.cget('text')
        try:
            current_index = messages.index(current_text)
            next_index = (current_index + 1) % len(messages)
        except ValueError:
            next_index = 0
        
        self.progress_label.config(text=messages[next_index])
        if self.is_translating:
            self.root.after(800, self.animate_progress_text)
    
    def translation_complete(self, translated_text, error):
        """Handle translation completion with enhanced feedback"""
        self.is_translating = False
        self.translate_button.config(state=tk.NORMAL, text="✨ Translate")
        self.progress_bar.stop()
        self.progress_frame.grid_remove()
        
        if error:
            self.update_status(f"❌ Error: {error}")
            messagebox.showerror("Translation Error", error)
        elif translated_text:
            # Display translation with animation
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", translated_text)
            self.output_text.config(state=tk.DISABLED)
            
            # Enable output controls
            self.copy_button.config(state=tk.NORMAL)
            self.clear_output_button.config(state=tk.NORMAL)
            self.export_button.config(state=tk.NORMAL)
            
            # Update statistics
            source_text = self.input_text.get("1.0", tk.END).strip()
            word_count = len(translated_text.split())
            char_count = len(translated_text)
            self.stats_var.set(f"📊 {word_count} words • {char_count} characters")
            
            self.update_status("✅ Translation completed successfully")
            
            # Brief success animation
            self.flash_success_feedback()
        
        # Re-enable translate button if there's text
        self.on_text_change()
    
    def flash_success_feedback(self):
        """Brief visual feedback for successful translation"""
        # Flash the output frame background briefly
        original_style = self.output_frame.cget('style')
        self.root.after(100, lambda: self.output_frame.configure(style=original_style))
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        # Clear status after 5 seconds
        self.root.after(5000, lambda: self.status_var.set("Ready"))
    
    def check_service_availability(self):
        """Check if translation service is available"""
        def check():
            """Check service availability in background"""
            try:
                available = self.translator.is_service_available()
                if not available:
                    self.root.after(0, lambda: self.update_status("Translation service may not be available"))
            except:
                pass
        
        # Check in background thread
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
