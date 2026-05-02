import sys
from pathlib import Path


VENDOR_PATH = Path(__file__).resolve().parent.parent / ".vendor"
if VENDOR_PATH.exists():
    sys.path.append(str(VENDOR_PATH))
