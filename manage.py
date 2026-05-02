import os
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
VENDOR_PATH = CURRENT_DIR.parent / ".vendor"
if VENDOR_PATH.exists():
    sys.path.append(str(VENDOR_PATH))


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brain_mri_project.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
