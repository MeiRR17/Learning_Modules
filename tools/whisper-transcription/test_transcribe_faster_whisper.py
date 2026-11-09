"""Bounded offline tests for optional faster-whisper backend, no model required."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

MODULE = Path(__file__).parent / "transcribe_faster_whisper.py"
spec = importlib.util.spec_from_file_location("local_faster_whisper_adapter", MODULE)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class FakeWhisperModel:
    def __init__(self, path, **options):
        assert options["local_files_only"] is True
        self.path = path

    def transcribe(self, file, **options):
        assert options["language"] == "he"
        return (
            [SimpleNamespace(start=0.0, end=1.25, text="שלום"),
             SimpleNamespace(start=2.0, end=3.5, text="עולם")],
            SimpleNamespace(language="he", duration=3.5),
        )


class LocalWhisperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.media = self.base / "owned.wav"
        self.media.write_bytes(b"synthetic audio fixture")
        self.model = self.base / "whisper-model"
        self.model.mkdir()
        self.output = self.base / "output"
        self.output.mkdir()

    def test_timestamp_rounds_milliseconds(self):
        self.assertEqual(adapter.srt_timestamp(61.9996), "00:01:02,000")

    def test_outputs_transcript_srt_and_provenance(self):
        digest = adapter.hash_file(self.media)
        result = adapter.transcribe(self.media, self.model, self.output,
                                    model_factory=FakeWhisperModel)
        self.assertEqual(result["source_sha256"], digest)
        self.assertEqual(result["segment_count"], 2)
        self.assertFalse(result["external_upload"])
        self.assertFalse(result["indexing_performed"])
        self.assertIn("שלום", Path(result["outputs"]["txt"]).read_text(encoding="utf-8"))
        self.assertIn("00:00:01,250", Path(result["outputs"]["srt"]).read_text(encoding="utf-8"))
        self.assertEqual(json.loads(Path(result["outputs"]["manifest"]).read_text())["engine"], "faster-whisper")

    def test_refuses_existing_outputs(self):
        self.output.joinpath("owned.faster-whisper.txt").write_text("existing")
        with self.assertRaises(FileExistsError):
            adapter.transcribe(self.media, self.model, self.output,
                               model_factory=FakeWhisperModel)

    def test_rejects_input_symlink(self):
        link = self.base / "link.wav"
        link.symlink_to(self.media)
        with self.assertRaises(ValueError):
            adapter.transcribe(link, self.model, self.output,
                               model_factory=FakeWhisperModel)

    def test_missing_model_cannot_fetch_automatically(self):
        with self.assertRaises(ValueError):
            adapter.transcribe(self.media, self.base / "missing", self.output,
                               model_factory=FakeWhisperModel)

    def test_original_media_unmodified(self):
        before = self.media.read_bytes()
        adapter.transcribe(self.media, self.model, self.output,
                           model_factory=FakeWhisperModel)
        self.assertEqual(self.media.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
