"""Keep Kokoro's espeak-ng working from a deep folder. Call before importing kokoro_onnx.

The espeak-ng library bundled with espeakng-loader only accepts a data path
shorter than 160 characters. A longer one (a .venv deep under e.g.
~/Library/Application Support/...) makes it silently fall back to its
compiled-in build path and fail with "Error processing file
/Users/runner/work/espeakng-loader/.../phontab". Only in that case, point
kokoro_onnx at a system espeak-ng instead, or stop with the fix if there is
none. An explicit PHONEMIZER_ESPEAK_LIBRARY always wins.
"""
import ctypes.util
import os
import sys

ESPEAK_PATH_MAX = 159   # bundled espeak-ng: 159 chars works, 160 fails
SYSTEM_LIBS = ('/opt/homebrew/lib/libespeak-ng.dylib',   # Apple silicon Homebrew
               '/usr/local/lib/libespeak-ng.dylib')       # Intel Homebrew


def use_system_espeak():
    """Return the system espeak-ng library chosen, or None to keep the bundled one."""
    if os.environ.get('PHONEMIZER_ESPEAK_LIBRARY'):
        return os.environ['PHONEMIZER_ESPEAK_LIBRARY']
    try:
        import espeakng_loader
    except ImportError:
        return None   # the kokoro_onnx import reports the missing install
    data = espeakng_loader.get_data_path()
    if len(data) <= ESPEAK_PATH_MAX:
        return None
    lib = next((p for p in SYSTEM_LIBS if os.path.exists(p)), None) \
        or ctypes.util.find_library('espeak-ng')
    if lib:
        os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = lib
        return lib
    sys.exit(f"[espeak] espeak-ng's data path is {len(data)} characters; the bundled "
             f"library only accepts {ESPEAK_PATH_MAX}:\n  {data}\n"
             f"  fix: move the toolkit to a shorter folder and re-create .venv, or install "
             f"a system espeak-ng (macOS: brew install espeak-ng; Debian/Ubuntu: "
             f"apt install libespeak-ng1)")
