"""
Configuration file for Math Animation System
Customize animation styles, colors, timing, and behavior

GitHub:
- Manim: https://github.com/ManimCommunity/manim
- mathsteps: https://github.com/google/mathsteps
"""

# ============================================================================
# ANIMATION SETTINGS
# ============================================================================

ANIMATION_CONFIG = {
    'pixel_height': 1080,
    'pixel_width': 1920,
    'frame_rate': 60,
    'background_color': '#1a1a2e',  # Dark background
}

# ============================================================================
# COLOR SCHEME (Professional & Modern)
# ============================================================================

COLORS = {
    'title': '#4A90E2',           # Professional blue
    'equation': '#FFFFFF',        # White
    'description': '#F5A623',     # Warm orange
    'result': '#7ED321',          # Success green
    'highlight': '#FF6B6B',       # Attention red
    'error': '#E74C3C',           # Error red
    'background': '#1a1a2e',      # Dark navy
    'step_bg': '#2C3E50',         # Dark blue-gray
    'accent': '#9B59B6',          # Purple accent
}

# ============================================================================
# TYPOGRAPHY SETTINGS
# ============================================================================

FONT_SIZES = {
    'title': 52,
    'subtitle': 38,
    'equation': 44,
    'description': 26,
    'step_indicator': 20,
    'label': 18,
    'small': 16,
}

# ============================================================================
# ANIMATION TIMING (in seconds)
# ============================================================================

TIMING = {
    'title_intro': 1.2,
    'title_underline': 1.2,
    'subtitle_fade': 0.8,
    'equation_box': 0.8,
    'equation_write': 1.2,
    'step_indicator': 0.5,
    'step_description': 0.7,
    'equation_transform': 1.5,
    'description_fadeout': 0.6,
    'final_glow': 1.0,
    'final_label': 1.0,
    'final_celebration': 1.0,
    'between_steps': 1.5,
    'wait_start': 1.0,
    'wait_initial': 1.5,
    'wait_step': 1.5,
    'wait_end': 2.0,
    'error_display': 3.0,
}

# ============================================================================
# MATH STEPPER SETTINGS
# ============================================================================

MATH_STEPPER = {
    'timeout': 10,  # Seconds to wait for Node.js process
    'js_file': 'math_stepper.js',
    'retry_on_failure': True,
    'max_retries': 2,
}

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

OUTPUT = {
    'default_quality': 'l',  # 'l' = low, 'm' = medium, 'h' = high, 'k' = 4k
    'default_format': 'mp4',
    'output_dir': './media/videos/',
    'save_last_frame': False,
    'transparent_background': False,
}

QUALITY_PRESETS = {
    'l': {'resolution': '480p', 'fps': 15, 'description': 'Low - Fast preview'},
    'm': {'resolution': '720p', 'fps': 30, 'description': 'Medium - Balanced'},
    'h': {'resolution': '1080p', 'fps': 60, 'description': 'High - Best for sharing'},
    'k': {'resolution': '2160p', 'fps': 60, 'description': '4K - Production quality'},
}

# ============================================================================
# BEHAVIOR SETTINGS
# ============================================================================

BEHAVIOR = {
    'show_step_numbers': True,
    'show_progress_bar': True,
    'show_substeps': False,
    'auto_pause_on_error': True,
    'verbose_logging': True,
    'validate_input': True,
    'strict_mode': False,  # Fail on warnings if True
}

# ============================================================================
# UI/UX SETTINGS
# ============================================================================

UI = {
    'use_rounded_corners': True,
    'corner_radius': 0.1,
    'box_padding': 0.3,
    'stroke_width': 2,
    'glow_effect': True,
    'celebration_effects': True,
    'show_error_suggestions': True,
}

# ============================================================================
# PRESETS
# ============================================================================

# Fast animation for quick preview
PRESET_FAST = {
    'animation_config': {
        'pixel_height': 720,
        'pixel_width': 1280,
        'frame_rate': 30,
    },
    'timing': {
        'title_intro': 0.5,
        'equation_write': 0.8,
        'step_description': 0.4,
        'equation_transform': 1.0,
        'description_fadeout': 0.3,
        'between_steps': 0.8,
    },
    'output': {
        'default_quality': 'l',
    }
}

# High quality for presentations
PRESET_PRESENTATION = {
    'animation_config': {
        'pixel_height': 1440,
        'pixel_width': 2560,
        'frame_rate': 60,
    },
    'timing': {
        'title_intro': 2.0,
        'equation_write': 2.0,
        'step_description': 1.5,
        'equation_transform': 2.0,
        'description_fadeout': 1.0,
        'between_steps': 2.5,
    },
    'output': {
        'default_quality': 'h',
    }
}

# Educational/detailed mode
PRESET_EDUCATIONAL = {
    'behavior': {
        'show_step_numbers': True,
        'show_substeps': True,
        'show_progress_bar': True,
        'verbose_logging': True,
    },
    'timing': {
        'between_steps': 3.0,
        'step_description': 1.5,
    },
    'ui': {
        'show_error_suggestions': True,
    }
}

# Minimal/clean style
PRESET_MINIMAL = {
    'ui': {
        'use_rounded_corners': False,
        'glow_effect': False,
        'celebration_effects': False,
    },
    'behavior': {
        'show_progress_bar': False,
    },
    'colors': {
        'background': '#000000',
        'equation': '#FFFFFF',
        'description': '#CCCCCC',
    }
}


def get_config(preset: str = None) -> dict:
    """
    Get configuration with optional preset
    
    Args:
        preset: 'fast', 'presentation', 'educational', or 'minimal'
        
    Returns:
        Configuration dictionary
    """
    config = {
        'animation': ANIMATION_CONFIG.copy(),
        'colors': COLORS.copy(),
        'fonts': FONT_SIZES.copy(),
        'timing': TIMING.copy(),
        'math_stepper': MATH_STEPPER.copy(),
        'output': OUTPUT.copy(),
        'behavior': BEHAVIOR.copy(),
        'ui': UI.copy(),
    }
    
    # Apply preset if specified
    presets = {
        'fast': PRESET_FAST,
        'presentation': PRESET_PRESENTATION,
        'educational': PRESET_EDUCATIONAL,
        'minimal': PRESET_MINIMAL,
    }
    
    if preset and preset.lower() in presets:
        preset_config = presets[preset.lower()]
        
        # Merge preset settings
        for section, settings in preset_config.items():
            if section in config:
                config[section].update(settings)
    
    return config


def print_config_info():
    """Print configuration information"""
    print("\n" + "="*70)
    print("Math Animation System - Configuration")
    print("="*70)
    print("\nAvailable Presets:")
    for name, preset in [
        ('fast', PRESET_FAST),
        ('presentation', PRESET_PRESENTATION),
        ('educational', PRESET_EDUCATIONAL),
        ('minimal', PRESET_MINIMAL)
    ]:
        print(f"\n  {name.upper()}")
        if 'timing' in preset:
            print(f"    - Faster animations" if name == 'fast' else "    - Detailed animations")
        if 'output' in preset:
            print(f"    - Quality: {preset['output'].get('default_quality', 'default')}")
    
    print("\n" + "="*70)


if __name__ == '__main__':
    print_config_info()
