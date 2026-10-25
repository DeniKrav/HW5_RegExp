import os
import re
import shutil


def to_salty(text):
    """Translate Russian text to the 'salty language'."""
    vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    return re.sub(f"[{vowels}]", lambda m: m.group(0) + "с" + m.group(0).lower(), text)


def extract_chords(filepath):
    """Return a set of unique chords found in the song file."""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    pattern = r"\b[A-H][#b]?(?:m|maj|min|dim|aug|sus|add)?\d*\b"
    return set(re.findall(pattern, text))


def rename_files(dir, pattern, new_pattern=None, sample_names=None, to_replace=False):
    """Rename files in a directory by regex pattern and/or sample name mapping.

    Args:
        dir: Directory containing the files.
        pattern: Regex pattern to select files and replace in names.
        new_pattern: Replacement string. If None, no regex replacement is done.
        sample_names: Dict mapping sample names (e.g. {'G1': 'WT_rep1'}).
        to_replace: If True, rename files (overwrite existing). If False, copy.
    """
    for filename in os.listdir(dir):
        if not re.search(pattern, filename):
            continue

        new_name = filename
        if new_pattern is not None:
            new_name = re.sub(pattern, new_pattern, new_name)
        if sample_names:
            for old, new in sample_names.items():
                new_name = new_name.replace(old, new)

        if new_name == filename:
            continue

        src = os.path.join(dir, filename)
        dst = os.path.join(dir, new_name)

        if to_replace:
            os.replace(src, dst)
        else:
            shutil.copy2(src, dst)
