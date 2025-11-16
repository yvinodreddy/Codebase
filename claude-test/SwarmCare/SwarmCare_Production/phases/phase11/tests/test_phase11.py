"""
Phase 11: Research & Publications
Comprehensive Unit Tests - Production Ready
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import (
    Phase11Implementation,
    ResearchPaperGenerator,
    CitationManager,
    QualityValidator,
    PaperTemplates
)


class TestResearchPaperGenerator(unittest.TestCase):
    """Test cases for ResearchPaperGenerator"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = ResearchPaperGenerator()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertIsNotNone(self.generator.citation_manager)
        self.assertIsNotNone(self.generator.quality_validator)
        self.assertIsNotNone(self.generator.templates)

    def test_generate_paper_clinical_ai(self):
        """Test generating clinical AI paper"""
        paper = self.generator.generate_paper(
            title="Test Clinical AI Paper",
            paper_type="technical",
            domain="clinical_ai"
        )

        self.assertIn("metadata", paper)
        self.assertIn("content", paper)
        self.assertIn("citations", paper)
        self.assertEqual(paper["metadata"]["title"], "Test Clinical AI Paper")
        self.assertEqual(paper["metadata"]["domain"], "clinical_ai")
        self.assertGreater(paper["metadata"]["word_count"], 1000)
        self.assertGreater(paper["metadata"]["citation_count"], 0)

    def test_generate_paper_ai_systems(self):
        """Test generating AI systems paper"""
        paper = self.generator.generate_paper(
            title="Multi-Agent Systems",
            paper_type="architecture",
            domain="ai_systems"
        )

        self.assertEqual(paper["metadata"]["type"], "architecture")
        self.assertIn("abstract", paper["content"])
        self.assertIn("introduction", paper["content"])
        self.assertIn("methodology", paper["content"])

    def test_generate_paper_compliance(self):
        """Test generating compliance paper"""
        paper = self.generator.generate_paper(
            title="HIPAA Compliance",
            paper_type="security",
            domain="compliance"
        )

        self.assertEqual(paper["metadata"]["type"], "security")
        self.assertIn("results", paper["content"])
        self.assertIn("discussion", paper["content"])
        self.assertIn("conclusion", paper["content"])

    def test_validate_papers(self):
        """Test paper validation"""
        papers = [
            self.generator.generate_paper("Paper 1", "technical", "clinical_ai"),
            self.generator.generate_paper("Paper 2", "architecture", "ai_systems")
        ]

        results = self.generator.validate_papers(papers)

        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn("valid", result)
            self.assertIn("checks", result)
            self.assertIn("score", result)

    def test_paper_content_completeness(self):
        """Test all paper sections are generated"""
        paper = self.generator.generate_paper(
            "Complete Paper Test",
            "technical",
            "clinical_ai"
        )

        required_sections = [
            "abstract", "introduction", "methodology",
            "results", "discussion", "conclusion", "bibliography"
        ]

        for section in required_sections:
            self.assertIn(section, paper["content"])
            self.assertTrue(len(paper["content"][section]) > 0)


class TestCitationManager(unittest.TestCase):
    """Test cases for CitationManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = CitationManager()

    def test_generate_citations_base(self):
        """Test generating base citations"""
        citations = self.manager.generate_citations("unknown_domain", "technical")

        self.assertGreater(len(citations), 0)
        self.assertIsInstance(citations, list)

        for cite in citations:
            self.assertIn("id", cite)
            self.assertIn("authors", cite)
            self.assertIn("title", cite)
            self.assertIn("journal", cite)
            self.assertIn("year", cite)

    def test_generate_citations_clinical_ai(self):
        """Test generating clinical AI citations"""
        citations = self.manager.generate_citations("clinical_ai", "technical")

        self.assertGreater(len(citations), 3)

    def test_generate_citations_ai_systems(self):
        """Test generating AI systems citations"""
        citations = self.manager.generate_citations("ai_systems", "architecture")

        self.assertGreater(len(citations), 3)

    def test_format_bibliography(self):
        """Test bibliography formatting"""
        citations = [
            {
                "id": "test2024",
                "authors": "Test, A. et al.",
                "title": "Test Paper",
                "journal": "Test Journal",
                "year": "2024",
                "volume": "1",
                "pages": "1-10"
            }
        ]

        bibliography = self.manager.format_bibliography(citations)

        self.assertIn("Test, A. et al.", bibliography)
        self.assertIn("Test Paper", bibliography)
        self.assertIn("2024", bibliography)


class TestQualityValidator(unittest.TestCase):
    """Test cases for QualityValidator"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = QualityValidator()

    def test_validate_complete_paper(self):
        """Test validating a complete paper"""
        paper = {
            "metadata": {
                "title": "Test Paper",
                "word_count": 2000,
                "citation_count": 5
            },
            "content": {
                "abstract": "Test abstract",
                "introduction": "Test intro",
                "methodology": "Test method",
                "results": "Test results",
                "discussion": "Test discussion",
                "conclusion": "Test conclusion",
                "bibliography": "Test bib"
            }
        }

        result = self.validator.validate_paper(paper)

        self.assertTrue(result["valid"])
        self.assertEqual(result["score"], 100.0)
        self.assertTrue(all(result["checks"].values()))

    def test_validate_incomplete_paper(self):
        """Test validating an incomplete paper"""
        paper = {
            "metadata": {
                "title": "Incomplete Paper",
                "word_count": 500,
                "citation_count": 1
            },
            "content": {
                "abstract": "Test abstract"
            }
        }

        result = self.validator.validate_paper(paper)

        self.assertFalse(result["valid"])
        self.assertLess(result["score"], 100.0)

    def test_validation_checks(self):
        """Test individual validation checks"""
        paper = {
            "metadata": {
                "title": "Test",
                "word_count": 1500,
                "citation_count": 4
            },
            "content": {
                "abstract": "A",
                "introduction": "B",
                "methodology": "C",
                "results": "D",
                "discussion": "E",
                "conclusion": "F",
                "bibliography": "G"
            }
        }

        result = self.validator.validate_paper(paper)

        checks = result["checks"]
        self.assertTrue(checks["has_abstract"])
        self.assertTrue(checks["has_introduction"])
        self.assertTrue(checks["has_methodology"])
        self.assertTrue(checks["sufficient_citations"])
        self.assertTrue(checks["sufficient_length"])


class TestPaperTemplates(unittest.TestCase):
    """Test cases for PaperTemplates"""

    def setUp(self):
        """Set up test fixtures"""
        self.templates = PaperTemplates()

    def test_get_technical_template(self):
        """Test getting technical template"""
        template = self.templates.get_template("technical")

        self.assertIn("structure", template)
        self.assertIn("min_sections", template)
        self.assertEqual(template["citation_style"], "IEEE")

    def test_get_architecture_template(self):
        """Test getting architecture template"""
        template = self.templates.get_template("architecture")

        self.assertEqual(template["citation_style"], "ACM")
        self.assertGreater(template["min_sections"], 0)

    def test_get_security_template(self):
        """Test getting security template"""
        template = self.templates.get_template("security")

        self.assertIn("threat_model", template["structure"])

    def test_get_default_template(self):
        """Test getting default template for unknown type"""
        template = self.templates.get_template("unknown_type")

        self.assertIn("structure", template)
        self.assertIn("min_sections", template)


class TestPhase11Implementation(unittest.TestCase):
    """Test cases for Phase11Implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase11Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 11)
        self.assertEqual(self.implementation.phase_name, "Research & Publications")
        self.assertEqual(self.implementation.story_points, 21)
        self.assertEqual(self.implementation.priority, "P2")

    def test_execute_success(self):
        """Test successful execution"""
        task = {
            "goal": "Generate research papers",
            "phase_id": 11
        }

        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertIn("papers_generated", result.output)
        self.assertEqual(result.output["papers_generated"], 5)

    def test_phase_output_structure(self):
        """Test phase output has correct structure"""
        task = {"goal": "Test execution", "phase_id": 11}
        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        output = result.output

        self.assertIn("phase_id", output)
        self.assertIn("phase_name", output)
        self.assertIn("story_points", output)
        self.assertIn("papers_generated", output)
        self.assertIn("papers", output)
        self.assertIn("validation", output)

    def test_all_papers_generated(self):
        """Test all 5 research papers are generated"""
        task = {"goal": "Generate all papers", "phase_id": 11}
        result = self.implementation.execute(task)

        self.assertEqual(len(result.output["papers"]), 5)

        paper_titles = [p["title"] for p in result.output["papers"]]
        self.assertIn("RAG-based Clinical Decision Support: A Multi-Ontology Approach", paper_titles)
        self.assertIn("Multi-Agent AI Orchestration in Healthcare: The SWARMCARE Framework", paper_titles)

    def test_all_papers_validated(self):
        """Test all papers pass validation"""
        task = {"goal": "Validate papers", "phase_id": 11}
        result = self.implementation.execute(task)

        validation_results = result.output["validation"]
        self.assertEqual(len(validation_results), 5)

        for validation in validation_results:
            self.assertTrue(validation["valid"])
            self.assertEqual(validation["score"], 100.0)

    def test_production_ready_flag(self):
        """Test production_ready flag is set correctly"""
        task = {"goal": "Check production readiness", "phase_id": 11}
        result = self.implementation.execute(task)

        self.assertTrue(result.output["production_ready"])

    def test_get_stats(self):
        """Test getting execution statistics"""
        stats = self.implementation.get_stats()

        self.assertEqual(stats["phase_id"], 11)
        self.assertEqual(stats["phase_name"], "Research & Publications")
        self.assertEqual(stats["framework_version"], "100%")


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # Initialize
        implementation = Phase11Implementation()

        # Execute
        task = {"goal": "Complete research paper generation", "phase_id": 11}
        result = implementation.execute(task)

        # Verify success
        self.assertTrue(result.success)

        # Verify all papers generated
        self.assertEqual(result.output["papers_generated"], 5)

        # Verify all validations passed
        all_valid = all(v["valid"] for v in result.output["validation"])
        self.assertTrue(all_valid)

        # Verify production ready
        self.assertTrue(result.output["production_ready"])

    def test_paper_quality_standards(self):
        """Test all papers meet quality standards"""
        generator = ResearchPaperGenerator()

        topics = ["clinical_ai", "ai_systems", "compliance", "knowledge_management", "medical_education"]

        for domain in topics:
            paper = generator.generate_paper(
                f"Test {domain} Paper",
                "technical",
                domain
            )

            # Validate
            validation = generator.quality_validator.validate_paper(paper)

            # Assert quality standards
            self.assertTrue(validation["valid"])
            self.assertGreaterEqual(paper["metadata"]["word_count"], 1000)
            self.assertGreaterEqual(paper["metadata"]["citation_count"], 3)
            self.assertEqual(validation["score"], 100.0)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
