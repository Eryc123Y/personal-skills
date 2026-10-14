"""Real ffmpeg checks for silent, timed, and embedded frame extraction.

Run with: python -m unittest discover -s manim-video/tests -v
No Manim installation, speech service, or third-party Python package is needed.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "requires ffmpeg and ffprobe")
class CheckFramesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.script = Path(__file__).resolve().parents[1] / "scripts/check_frames.py"
        cls.video = cls.root / "silent.mp4"
        command = ["ffmpeg", "-v", "error", "-y"]
        for color in ["red", "green", "blue"]:
            command += ["-f", "lavfi", "-i", f"color=c={color}:s=128x72:r=10:d=1"]
        command += ["-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]",
                    "-map", "[v]", "-c:v", "mpeg4", "-q:v", "2", str(cls.video)]
        subprocess.run(command, check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def setUp(self) -> None:
        self.output = self.root / self.id().split(".")[-1]

    def run_check(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(self.script), str(self.video),
                               *arguments, "-o", str(self.output), "--width", "128"],
                              capture_output=True, text=True, timeout=30)

    def timeline(self, data: dict) -> str:
        target = self.root / f"{self.output.name}.json"
        target.write_text(json.dumps(data))
        return str(target)

    def assert_color(self, image: Path, dominant: int) -> None:
        pixels = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(image),
                                          "-vf", "scale=1:1", "-frames:v", "1",
                                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
        self.assertEqual(len(pixels), 3)
        self.assertGreater(pixels[dominant], 90)
        for index in range(3):
            if index != dominant:
                self.assertLess(pixels[index], 30)

    def test_silent_timestamps_extract_correct_visual_states(self) -> None:
        result = self.run_check("--at", "0.2", "1.2", "2.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        frames = sorted(self.output.glob("at_*.png"))
        self.assertEqual(len(frames), 3)
        for color, frame in enumerate(frames):
            self.assert_color(frame, color)
        self.assertTrue((self.output / "contact.png").is_file())
        self.assertIn("audio stream: no", result.stdout)
        self.assertNotIn("vs timings", result.stdout)

    def test_single_timestamp_produces_contact_sheet(self) -> None:
        result = self.run_check("--at", "1.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_color(self.output / "contact.png", 1)

    def test_existing_timeline_invocation_retains_boundaries_and_duration(self) -> None:
        timing = self.timeline({"duration": 3, "segments": [{"id": "intro", "start": 0, "end": 1}]})
        result = self.run_check(timing)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_color(self.output / "intro_in.png", 0)
        self.assert_color(self.output / "intro_out.png", 0)
        self.assertIn("vs timings 3.00s", result.stdout)

    def test_embedded_clip_applies_offset_once(self) -> None:
        timing = self.timeline({"duration": 1, "segments": [{"id": "clip", "start": 0, "end": 1}]})
        result = self.run_check(timing, "--offset", "1", "--at", "1.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_color(self.output / "clip_in.png", 1)
        self.assert_color(self.output / "clip_out.png", 1)
        self.assert_color(self.output / "at_0001.20.png", 2)
        self.assertNotIn("vs timings", result.stdout)

    def test_empty_segments_with_explicit_duration_and_timestamp(self) -> None:
        timing = self.timeline({"duration": 3, "segments": []})
        result = self.run_check(timing, "--at", "0.2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("vs timings 3.00s", result.stdout)

    def test_missing_selection_and_invalid_timestamps_fail(self) -> None:
        for arguments in [(), ("--at", "-1"), ("--at", "nan"), ("--at", "inf")]:
            with self.subTest(arguments=arguments):
                result = self.run_check(*arguments)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse(self.output.exists())

    def test_out_of_range_selection_does_not_leave_stale_contact_sheet(self) -> None:
        good = self.run_check("--at", "0.2")
        self.assertEqual(good.returncode, 0, good.stderr)
        bad = self.run_check("--at", "9")
        self.assertEqual(bad.returncode, 2, bad.stderr)
        self.assertFalse((self.output / "contact.png").exists())


if __name__ == "__main__":
    unittest.main()
