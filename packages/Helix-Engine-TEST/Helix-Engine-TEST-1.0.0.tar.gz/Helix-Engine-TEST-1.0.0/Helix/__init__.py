from version import HLX_MAJOR_VER, HLX_MINOR_VER, HLX_PATCH_VER, HLX_YR_EDITION
def engine_info(void_t):
    print(f"Helix Engine v{HLX_MAJOR_VER}.{HLX_MINOR_VER}.{HLX_PATCH_VER}+{HLX_YR_EDITION}\n")

from .helix import *

if "HLX_HIDE_PROMPT" not in os.environ: engine_info();