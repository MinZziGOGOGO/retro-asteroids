"""Sound generation — retro sounds via pygame.sndarray with fallback."""

import random
import struct
import pygame

_SOUND_ENABLED = True
_sound_cache: dict = {}

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
except (pygame.error, NotImplementedError):
    # No audio device, or a pygame build without the mixer module:
    # the game still runs, just silently.
    _SOUND_ENABLED = False


def _generate_square_wave(freq: float, duration: float, volume: float = 0.3):
    """Generate a square wave sound and return a pygame Sound object."""
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    samples = []

    period = sample_rate / freq if freq > 0 else 1
    for i in range(num_samples):
        # square wave
        val = 1.0 if (i % int(period)) < int(period) / 2 else -1.0
        samples.append(int(val * volume * 32767))

    # pack as 16-bit signed
    raw = struct.pack(f"<{num_samples}h", *samples)
    return pygame.mixer.Sound(buffer=raw)


def _generate_noise(duration: float, volume: float = 0.3):
    """Generate white noise."""
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    samples = []

    for _ in range(num_samples):
        val = random.uniform(-1.0, 1.0)
        samples.append(int(val * volume * 32767))

    raw = struct.pack(f"<{num_samples}h", *samples)
    return pygame.mixer.Sound(buffer=raw)


def _get_or_create(key: str, factory):
    if not _SOUND_ENABLED:
        return None
    if key not in _sound_cache:
        try:
            _sound_cache[key] = factory()
        except Exception:
            return None
    return _sound_cache[key]


def play_fire():
    """Short blip on fire."""
    s = _get_or_create("fire", lambda: _generate_square_wave(800, 0.05, 0.2))
    if s:
        s.play()


def play_thrust():
    """Low rumble. Played repeatedly while thrusting (rate-limited by caller)."""
    s = _get_or_create("thrust", lambda: _generate_square_wave(60, 0.15, 0.15))
    if s:
        s.play()


def play_explosion():
    """Explosion noise."""
    s = _get_or_create("explosion", lambda: _generate_noise(0.3, 0.25))
    if s:
        s.play()


def play_extra_life():
    """Rising tone for extra life."""
    s = _get_or_create("extralife", lambda: _generate_square_wave(600, 0.3, 0.2))
    if s:
        s.play()


def is_sound_enabled() -> bool:
    return _SOUND_ENABLED
