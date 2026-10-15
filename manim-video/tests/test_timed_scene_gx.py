"""The ManimGX timed-scene template on a real timeline.

Run with a Python that has ManimGX:  <venv>/bin/python -m unittest discover -s manim-video/tests -v
Skipped when manimgx is not importable (the CE checks in this folder need no Manim at all).
"""
from pathlib import Path
import importlib.util
import json
import sys
import tempfile
import unittest
import warnings

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"
HAS_GX = importlib.util.find_spec("manimgx") is not None


@unittest.skipUnless(HAS_GX, "requires manimgx")
class TimedSceneGxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(TEMPLATES))
        import manimgx
        import timed_scene_gx
        cls.m, cls.ts = manimgx, timed_scene_gx
        cls.temp = tempfile.TemporaryDirectory()
        cls.timings = Path(cls.temp.name) / "t.json"
        cls.timings.write_text(json.dumps({"duration": 3.0, "segments": [
            {"id": "a", "text": "第一句", "start": 0.2, "end": 1.4, "pauses": [[0.5, 0.7]]},
            {"id": "b", "text": "第二句", "start": 1.8, "end": 2.6}]}), encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()
        sys.path.remove(str(TEMPLATES))

    def scene(self, late=0.0):
        m, ts, timings = self.m, self.ts, str(self.timings)

        class Clip(ts.TimedScene):
            TIMINGS = timings

            def construct(self):
                self.say("a")
                self.add(ts.mix_line("误差 $e(x)$ 的上界是 $10{,}987$，对"))
                self.beat(0)
                self.marks = [self.now]
                self.play(m.FadeIn(m.Circle()), run_time=0.4 + late)
                self.say("b")
                self.marks.append(self.now)
                self.finish()

        return Clip()

    def render(self, scene, height):
        m = self.m
        old = m.config.frame_rate, m.config.pixel_width, m.config.pixel_height
        m.config.frame_rate, m.config.pixel_width, m.config.pixel_height = 30, height * 16 // 9, height
        try:
            frames = []
            scene.render(frames=lambda f: frames.append(1))
            return len(frames)
        finally:
            m.config.frame_rate, m.config.pixel_width, m.config.pixel_height = old

    def test_anchors_and_length(self):
        s = self.scene()
        self.render(s, 360)
        self.assertAlmostEqual(s.marks[0], 0.2 + 0.7, delta=1 / 30)
        self.assertAlmostEqual(s.marks[1], 1.8, delta=1 / 30)
        self.assertAlmostEqual(s.now, 3.0, delta=1 / 30)
        self.assertEqual(s.overruns, [])

    def test_late_beat_warns_in_preview(self):
        s = self.scene(late=1.0)              # 1.4 s of animation from 0.9 s runs past b's start (1.8 s)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            self.render(s, 360)
        self.assertTrue(s.overruns and any("late" in str(w.message) for w in caught))

    def test_late_beat_fails_in_final(self):
        with self.assertRaises(RuntimeError):
            self.render(self.scene(late=1.0), 1080)

    def test_mix_line_spacing(self):
        line = self.ts.mix_line("误差 $e(x)$，对")
        self.assertIsInstance(line, self.m.Typst)
        self.assertGreater(line.width, 0)
        with self.assertRaises(ValueError):
            self.ts.mix_line("误差 $e(x)")


if __name__ == "__main__":
    unittest.main()
