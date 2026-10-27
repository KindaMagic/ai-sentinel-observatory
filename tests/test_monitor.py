"""Offline tests for Sentinel feed parsing, risk logic and fail-safe status."""
import datetime as dt
import email.utils
import importlib.util
import pathlib
import unittest
from unittest.mock import patch

FILE = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "monitor.py"
spec = importlib.util.spec_from_file_location("monitor", FILE)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


def rss(title, link="https://openai.com/index/model-oversight/", days_ago=0):
    published = email.utils.format_datetime(
        dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_ago)
    )
    return ('<rss version="2.0"><channel><item><title>' + title +
            '</title><link>' + link + '</link><pubDate>' + published +
            '</pubDate><description>AI model safety evaluation report</description></item></channel></rss>').encode()


class SentinelTests(unittest.TestCase):
    def test_parser_accepts_recent_official_item(self):
        items = monitor.feed_items(rss("AI model safety incident"))
        self.assertEqual(len(items), 1)

    def test_parser_rejects_unauthorised_link(self):
        self.assertEqual(monitor.feed_items(rss("Safety", link="https://evil.example.com/")), [])

    def test_parser_rejects_old_item(self):
        self.assertEqual(monitor.feed_items(rss("Safety", days_ago=30)), [])

    def test_serious_is_signal_not_confirmed_emergency(self):
        self.assertEqual(monitor.classify({"title": "AI agent unsanctioned action",
                                           "summary": ""}), "serious-keyword")

    def test_generic_risk_word_is_not_itself_an_incident(self):
        self.assertIsNone(monitor.classify({"title": "New model monitoring risks",
                                            "summary": ""}))

    def test_routine_security_improvements_not_misclassified_as_incidents(self):
        self.assertIsNone(monitor.classify({
            "title": "GPT-6.1 helps engineers strengthen code security",
            "summary": "Model agent reviews security risks and proposes fixes"
        }))
        self.assertIsNone(monitor.classify({
            "title": "Securing our frontier model training environment",
            "summary": "Improved containment and high-compute red-teaming"
        }))

    def test_total_feed_outage_disables_risk(self):
        with patch.object(monitor, "source_fetch", side_effect=RuntimeError("offline")):
            report = monitor.generate()
        self.assertIsNone(report["riskAssessment"]["level"])
        self.assertEqual(report["checkStatus"], "failed")

    def test_no_screened_publications_is_green_not_an_all_clear(self):
        original = monitor.FEEDS
        monitor.FEEDS = [
            ("OpenAI", "https://openai.com/news/rss.xml"),
            ("DeepMind", "https://deepmind.google/blog/rss.xml"),
        ]
        try:
            def fetch(url):
                if "openai" in url:
                    return rss("New model release")
                return rss("New benchmark results", link="https://deepmind.google/blog/benchmark")
            with patch.object(monitor, "source_fetch", side_effect=fetch):
                report = monitor.generate()
            self.assertEqual(report["riskAssessment"]["level"], "green")
            self.assertIn("never means safe", report["riskAssessment"]["warning"])
        finally:
            monitor.FEEDS = original

    def test_one_serious_source_is_amber(self):
        original = monitor.FEEDS
        monitor.FEEDS = [
            ("OpenAI", "https://openai.com/news/rss.xml"),
            ("DeepMind", "https://deepmind.google/blog/rss.xml"),
        ]
        try:
            def fetch(url):
                if "openai" in url:
                    return rss("AI agent unsanctioned actions")
                return rss("New AI model release", link="https://deepmind.google/blog/release")
            with patch.object(monitor, "source_fetch", side_effect=fetch):
                self.assertEqual(monitor.generate()["riskAssessment"]["level"], "amber")
        finally:
            monitor.FEEDS = original

    def test_multi_source_serious_remains_amber_without_human_review(self):
        original = monitor.FEEDS
        monitor.FEEDS = [
            ("OpenAI", "https://openai.com/news/rss.xml"),
            ("DeepMind", "https://deepmind.google/blog/rss.xml"),
        ]
        try:
            def fetch(url):
                if "openai" in url:
                    return rss("AI agent unsanctioned actions")
                return rss("AI agent security breach", link="https://deepmind.google/blog/security")
            with patch.object(monitor, "source_fetch", side_effect=fetch):
                report = monitor.generate()
            self.assertEqual(report["riskAssessment"]["level"], "amber")
            self.assertEqual(report["riskAssessment"]["formalPublicRating"], "unassigned")
        finally:
            monitor.FEEDS = original


if __name__ == "__main__":
    unittest.main()
