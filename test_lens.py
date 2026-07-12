import unittest
from lens import analyze


class LensTests(unittest.TestCase):
    def test_calculates_downstream_blast_radius(self):
        report = analyze([{ "source": "api", "target": "orders" }, { "source": "orders", "target": "db" }], "api")
        self.assertEqual(report["blast_radius"], ["db", "orders"])

    def test_detects_cycle(self):
        report = analyze([{ "source": "a", "target": "b" }, { "source": "b", "target": "a" }])
        self.assertTrue(report["cycles"])

    def test_finds_shared_dependency(self):
        report = analyze([{ "source": "a", "target": "db" }, { "source": "b", "target": "db" }])
        self.assertEqual(report["shared_dependencies"], ["db"])


if __name__ == "__main__":
    unittest.main()
