#!/usr/bin/env python3
"""Check the Manim toolchain. Run with the Python that will render.

    python doctor.py              # Manim CE: exit 0 when every required check passes
    python doctor.py --engine gx  # ManimGX (references/manimgx.md): package, GPU render, ffmpeg; no TeX
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


def check_gx() -> bool:
    """ManimGX renders on the GPU and brings Typst, mitex and fonts: one tiny frame proves the whole chain."""
    if importlib.util.find_spec("manimgx") is None:
        return check(f"manimgx importable in {sys.executable}", False,
                     "uv pip install manimgx==0.1.1  (Python 3.13+, its own environment)")
    from importlib.metadata import version as pkg_version
    check(f"manimgx importable ({pkg_version('manimgx')}) in {sys.executable}", True)
    try:
        import manimgx as m

        class Probe(m.Scene):
            def construct(self) -> None:
                self.add(m.MathTex(r"e^{i\pi}+1=0"), m.Text("中文", font="PingFang SC").shift(m.DOWN))

        m.config.pixel_width, m.config.pixel_height = 320, 180
        frames: list[bytes] = []
        Probe().render(frames=lambda f: frames.append(f.pixels()))
        rendered = bool(frames) and any(frames[-1][k] for k in range(0, len(frames[-1]), 4))
    except Exception as exc:  # noqa: BLE001 - reported, not raised
        return check("ManimGX GPU render", False, f"{type(exc).__name__}: {str(exc)[:120]}")
    return check("ManimGX GPU render (formula and CJK text)", rendered, "no pixels drawn: check the GPU adapter")


def main() -> int:
    ok = True
    if "--engine" in sys.argv and sys.argv[sys.argv.index("--engine") + 1:][:1] == ["gx"]:
        ok &= check_gx()
        for name, hint in REQUIRED_BINS.items():
            ok &= check(name, shutil.which(name) is not None, hint)
        return 0 if ok else 1
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
