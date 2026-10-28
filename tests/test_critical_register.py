"""Validate the cumulative critical register and prevent automatic promotion."""
import json
import pathlib
import re
import unittest
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTER = ROOT / "critical-incidents.json"
MONITOR = ROOT / "scripts" / "monitor.py"


class CriticalRegisterTests(unittest.TestCase):
    def test_archive_is_valid_and_has_unique_stable_ids(self):
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        self.assertEqual(data["schemaVersion"], 1)
        self.assertIsInstance(data["entries"], list)
        ids = [item["id"] for item in data["entries"]]
        self.assertEqual(len(ids), len(set(ids)))
        for item in data["entries"]:
            self.assertRegex(item["id"], r"^SCI-[0-9]{4}-[0-9]{3,}$")
            for field in ("title", "eventDate", "disclosedDate", "recordedDate",
                          "lastCheckedDate", "setting", "incidentType", "observed",
                          "confirmedConsequences", "criticalThreshold", "notEstablished",
                          "status", "verification"):
                self.assertTrue(isinstance(item.get(field), str) and item[field].strip(), field)
            self.assertIn(item["status"], ("resolved", "ongoing", "unknown"))
            self.assertTrue(item.get("sources"))
            for source in item["sources"]:
                url = urlparse(source["url"])
                self.assertEqual(url.scheme, "https")
                self.assertTrue(url.hostname)
            self.assertIsInstance(item.get("amendments", []), list)

    def test_monitor_does_not_write_or_promote_critical_records(self):
        source = MONITOR.read_text(encoding="utf-8")
        self.assertNotIn('critical-incidents.json', source)
        self.assertNotIn('SCI-', source)

    def test_archive_is_separate_from_provisional_source_watch(self):
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
        self.assertIn("No entry is created by the automatic feed monitor", data["publicationRule"])


if __name__ == "__main__":
    unittest.main()
