#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    # Add src to sys.path so Python can find wall_e.settings
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wall_e.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

