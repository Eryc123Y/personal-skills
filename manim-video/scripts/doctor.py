#!/usr/bin/env python3
"""Check the Manim toolchain. Run with the Python that will render.

    python doctor.py            # exit 0 when every required check passes
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys

REQUIRED_BINS = {
    "ffmpeg": "brew install ffmpeg",
    "ffprobe": "brew install ffmpeg",
}
TEX_BINS = {
    "latex": "MacTeX / BasicTeX, needed for MathTex",
    "xelatex": "needed for Chinese inside MathTex (ctex)",
    "dvisvgm": "converts TeX output to SVG for Manim",
}
TEX_PACKAGES = ["ctex.sty", "xeCJK.sty", "standalone.cls", "amsmath.sty"]
CJK_FONTS = ["PingFang SC", "Heiti SC", "Noto Sans CJK SC", "Source Han Sans SC"]


def check(label: str, ok: bool, hint: str = "") -> bool:
    print(f"[{'ok' if ok else '--'}] {label}" + ("" if ok or not hint else f"  ->  {hint}"))
    return ok


def run(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def main() -> int:
    ok = True
    has_manim = importlib.util.find_spec("manim") is not None
    version = ""
    if has_manim:
        from importlib.metadata import version as pkg_version
        version = pkg_version("manim")
    ok &= check(f"manim importable ({version or 'missing'}) in {sys.executable}", has_manim,
                'uv pip install manim  (or: uv add manim)')
    for name, hint in REQUIRED_BINS.items():
        ok &= check(name, shutil.which(name) is not None, hint)

    tex_ok = all(check(name, shutil.which(name) is not None, hint) for name, hint in TEX_BINS.items())
    if tex_ok:
        for pkg in TEX_PACKAGES:
            tex_ok &= check(f"TeX package {pkg}", bool(run(["kpsewhich", pkg]).strip()),
                            f"tlmgr install {pkg.rsplit('.', 1)[0].lower()}")
    if not tex_ok:
        print("     without TeX: MathTex/Tex are unavailable; see references/cjk-and-tex.md")

    fonts = run(["fc-list", ":lang=zh", "family"])
    found = [f for f in CJK_FONTS if f in fonts]
    check(f"CJK font for Text ({found[0] if found else 'none found'})", bool(found),
          "set CJK_FONT in timed_scene.py to an installed font")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
