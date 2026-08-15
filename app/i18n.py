"""
Logi Options+ GTK Internationalization (i18n) Module
Supports automatic OS language detection, GNU gettext catalogues,
and seamless fallback to English.
"""

import gettext
import locale
import os
from pathlib import Path

DOMAIN = "logi-options-gtk"
LOCALES_DIR = Path(__file__).parent / "locale"
SYSTEM_LOCALES_DIR = Path("/usr/share/locale")
USER_LOCALES_DIR = Path(os.path.expanduser("~/.local/share/locale"))

# Set user default locale from environment variables (LANG, LC_ALL, LC_MESSAGES)
try:
    locale.setlocale(locale.LC_ALL, '')
except Exception:
    pass

# Determine best locales directory
locales_path = None
if LOCALES_DIR.exists():
    locales_path = str(LOCALES_DIR)
elif USER_LOCALES_DIR.exists() and (USER_LOCALES_DIR / "pt_BR" / "LC_MESSAGES" / f"{DOMAIN}.mo").exists():
    locales_path = str(USER_LOCALES_DIR)
elif SYSTEM_LOCALES_DIR.exists():
    locales_path = str(SYSTEM_LOCALES_DIR)
else:
    locales_path = str(LOCALES_DIR)

try:
    translation = gettext.translation(
        domain=DOMAIN,
        localedir=locales_path,
        fallback=True
    )
    _ = translation.gettext
    ngettext = translation.ngettext
except Exception:
    def _(msg: str) -> str:
        return msg

    def ngettext(singular: str, plural: str, n: int) -> str:
        return singular if n == 1 else plural

__all__ = ["_", "ngettext", "DOMAIN", "LOCALES_DIR"]
