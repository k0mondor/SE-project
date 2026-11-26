import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from src import db
from src.bootstrap import ensure_database
from src.leadership_service import diagnose_shortages
from src.query_service import list_enterprises, segment_coverage


class LeadershipDiagnosisTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        database = patch.object(db, "DB_PATH", Path(directory.name) / "test.db")
        database.start()
        self.addCleanup(database.stop)
        ensure_database()

    def test_repository_sample_shortages_and_evidence(self):
        result = diagnose_shortages()
        self.assertEqual((result["total"], result["covered_count"]), (50, 5))
        self.assertEqual(
            [(item["segment"], item["count"]) for item in result["shortages"]],
            [("半导体设备", 3), ("晶圆制造", 4), ("先进封装", 4)],
        )
        equipment = result["shortages"][0]
        self.assertEqual(equipment["ratio"], 0.06)
        self.assertEqual(equipment["evidence"]["sample_count"], 50)
        self.assertEqual(equipment["status"], "weak")
        self.assertIn("半导体设备", [gap["supply_segment"] for gap in result["support_gaps"]])
        self.assertTrue(all(gap["status"] == "pending_verification" for gap in result["support_gaps"]))

    def test_hangzhou_diagnosis_and_details_use_same_region_scope(self):
        city = "浙江省杭州市"
        self.assertEqual(segment_coverage(city)["total"], 38)
        self.assertEqual(list_enterprises(region=city)["total"], 38)
        result = diagnose_shortages(city, include_subregions=True)
        self.assertEqual(result["total"], 40)
        for segment in result["segments"]:
            evidence = list_enterprises(
                region=city, include_subregions=True, segments=segment["segment"],
            )
            self.assertEqual(evidence["total"], segment["count"])
            self.assertTrue(all(item["source_url"] for item in evidence["items"]))

    def test_missing_dictionary_segment_and_empty_region(self):
        with closing(db.connect()) as conn, conn:
            conn.execute("INSERT INTO chain_segment (name, level) VALUES ('样例未覆盖环节', 2)")
        result = diagnose_shortages()
        self.assertEqual(result["shortages"][0]["status"], "missing")
        self.assertEqual(result["shortages"][0]["count"], 0)
        empty = diagnose_shortages("无样本地区")
        self.assertEqual(empty["total"], 0)
        self.assertEqual(empty["shortages"], [])
        self.assertEqual(empty["support_gaps"], [])
        self.assertTrue(all(item["ratio"] is None and item["status"] == "no_data" for item in empty["segments"]))

    def test_ratio_equal_to_threshold_is_covered(self):
        with closing(db.connect()) as conn, conn:
            conn.execute(
                "UPDATE enterprise SET chain_segment = '半导体设备' "
                "WHERE id IN (SELECT id FROM enterprise WHERE chain_segment = '芯片设计' LIMIT 2)"
            )
        equipment = next(item for item in diagnose_shortages()["segments"] if item["segment"] == "半导体设备")
        self.assertEqual((equipment["ratio"], equipment["status"]), (0.1, "covered"))


if __name__ == "__main__":
    unittest.main()
