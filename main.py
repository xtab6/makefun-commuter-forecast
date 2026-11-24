"""Charm the Commuter: Forecast a City That Isn't.

Writes one line of weather forecast (at most 140 characters) for the
invented city of Wobbleford to /output/entry.txt.

Stdlib only. Deterministic: no network, no clock, no randomness.
"""

import os

LINE = (
    "Good morning, Wobbleford: drizzle till nine, then bright sun \u2014 "
    "the 7:40 bus is on time, and your umbrella gets the morning off."
)

MAX_CHARS = 140


def validate(text):
    """The gate: UTF-8 text of 1 to 140 characters, not only whitespace,
    a single line, no trailing newline."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1 to 140 characters, got %d" % len(text))
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")
    return text


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    text = validate(LINE)
    out = output_dir()
    os.makedirs(out, exist_ok=True)
    target = os.path.join(out, "entry.txt")
    # Clean only the contents of the output folder, never the folder itself:
    # the grader mounts /output, removing it fails with EPERM.
    if os.path.exists(target):
        os.remove(target)
    with open(target, "wb") as fh:
        fh.write(text.encode("utf-8"))
    # Read back what was written and prove it is byte-identical to the
    # validated line: a silent short write must never pass as a valid entry.
    with open(target, "rb") as fh:
        written = fh.read()
    if written != text.encode("utf-8"):
        raise ValueError("read-back mismatch: entry.txt is not the validated line")


if __name__ == "__main__":
    main()
