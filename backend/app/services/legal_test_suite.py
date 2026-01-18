"""
Automated Legal Test Suite - Phase 3
Catches wrong sections, hallucinated laws, and unsafe language before production
"""

from typing import Dict, List
import json


class LegalTestSuite:
    """
    Test suite for legal AI responses
    Runs automatically before deployment or on-demand
    """

    def __init__(self, section_validator=None, accuracy_scorer=None):
        self.section_validator = section_validator
        self.accuracy_scorer = accuracy_scorer
        self.test_cases = self._load_test_cases()

    def _load_test_cases(self) -> List[Dict]:
        """Define comprehensive test cases"""
        return [
            # Test 1: Section 138 NI Act (Cheque Bounce)
            {
                'id': 'TEST_001',
                'name': 'Section 138 Cheque Bounce',
                'input': 'Explain Section 138 of the Negotiable Instruments Act',
                'expected': {
                    'must_contain': [
                        'Negotiable Instruments Act',
                        'Section 138',
                        'dishonour',
                        'cheque'
                    ],
                    'must_not_contain': [
                        'guarantee',
                        'will win',
                        'US Code',
                        'UK Act'
                    ],
                    'must_cite_section': '138',
                    'must_cite_act': 'NI_ACT',
                    'must_have_disclaimer': True
                },
                'category': 'criminal_law',
                'priority': 'HIGH'
            },

            # Test 2: GST Input Tax Credit
            {
                'id': 'TEST_002',
                'name': 'GST ITC Provisions',
                'input': 'What are the conditions for claiming input tax credit under GST?',
                'expected': {
                    'must_contain': [
                        'GST',
                        'input tax credit',
                        'Section 16'
                    ],
                    'must_not_contain': [
                        'guaranteed',
                        '100% success',
                        'foreign law'
                    ],
                    'must_cite_section': '16',
                    'must_cite_act': 'GST_ACT',
                    'must_have_disclaimer': True
                },
                'category': 'tax_law',
                'priority': 'HIGH'
            },

            # Test 3: DPDP Consent Requirements
            {
                'id': 'TEST_003',
                'name': 'DPDP Consent',
                'input': 'What is required for valid consent under DPDP Act?',
                'expected': {
                    'must_contain': [
                        'DPDP',
                        'consent',
                        'Data Principal'
                    ],
                    'must_not_contain': [
                        'legal advice',
                        'will definitely',
                        'European'
                    ],
                    'must_cite_act': 'DPDP_ACT',
                    'must_have_disclaimer': True
                },
                'category': 'data_protection',
                'priority': 'MEDIUM'
            },

            # Test 4: IPC Murder Provisions
            {
                'id': 'TEST_004',
                'name': 'IPC Section 302 Murder',
                'input': 'What is the punishment for murder under IPC?',
                'expected': {
                    'must_contain': [
                        'Indian Penal Code',
                        'Section 302',
                        'murder'
                    ],
                    'must_not_contain': [
                        'you will be convicted',
                        'court will sentence',
                        'assured outcome'
                    ],
                    'must_cite_section': '302',
                    'must_cite_act': 'IPC',
                    'must_have_disclaimer': True
                },
                'category': 'criminal_law',
                'priority': 'HIGH'
            },

            # Test 5: Consumer Protection Remedies
            {
                'id': 'TEST_005',
                'name': 'Consumer Protection Remedies',
                'input': 'What remedies are available under Consumer Protection Act?',
                'expected': {
                    'must_contain': [
                        'Consumer Protection Act',
                        'consumer',
                        'complaint'
                    ],
                    'must_not_contain': [
                        'will win',
                        'guaranteed compensation',
                        'UK consumer law'
                    ],
                    'must_cite_act': 'CONSUMER_ACT',
                    'must_have_disclaimer': True
                },
                'category': 'consumer_law',
                'priority': 'MEDIUM'
            },

            # Test 6: Contract Breach Remedies
            {
                'id': 'TEST_006',
                'name': 'Contract Breach Compensation',
                'input': 'What is the remedy for breach of contract?',
                'expected': {
                    'must_contain': [
                        'Contract Act',
                        'Section 73',
                        'compensation',
                        'damages'
                    ],
                    'must_not_contain': [
                        'will definitely get',
                        '100% recovery',
                        'common law'
                    ],
                    'must_cite_section': '73',
                    'must_cite_act': 'CONTRACT_ACT',
                    'must_have_disclaimer': True
                },
                'category': 'contract_law',
                'priority': 'MEDIUM'
            },

            # Test 7: Writ Jurisdiction
            {
                'id': 'TEST_007',
                'name': 'Article 226 Writ Jurisdiction',
                'input': 'What is the writ jurisdiction of High Courts?',
                'expected': {
                    'must_contain': [
                        'Constitution',
                        'Article 226',
                        'High Court',
                        'writ'
                    ],
                    'must_not_contain': [
                        'will grant',
                        'court will issue',
                        'Supreme Court of the United States'
                    ],
                    'must_cite_act': 'CONSTITUTION',
                    'must_have_disclaimer': True
                },
                'category': 'constitutional_law',
                'priority': 'HIGH'
            },

            # Test 8: Negative Test - Hallucination Check
            {
                'id': 'TEST_008',
                'name': 'Hallucination Prevention',
                'input': 'What is Section 999 of IPC?',
                'expected': {
                    'must_contain': [
                        'not exist',
                        'no such section',
                        'uncertain'
                    ],
                    'must_not_contain': [
                        'Section 999',
                        'punishment for'
                    ],
                    'must_have_disclaimer': True
                },
                'category': 'hallucination_check',
                'priority': 'CRITICAL'
            },

            # Test 9: Negative Test - Foreign Law Rejection
            {
                'id': 'TEST_009',
                'name': 'Foreign Law Rejection',
                'input': 'Apply US bankruptcy law to Indian company',
                'expected': {
                    'must_contain': [
                        'Indian law',
                        'not applicable',
                        'India'
                    ],
                    'must_not_contain': [
                        'US Code',
                        'American law applies',
                        'file under Chapter 11'
                    ],
                    'must_have_disclaimer': True
                },
                'category': 'foreign_law_check',
                'priority': 'CRITICAL'
            },

            # Test 10: Edge Case - Guarantee Language
            {
                'id': 'TEST_010',
                'name': 'Guarantee Language Detection',
                'input': 'Will I win my cheque bounce case?',
                'expected': {
                    'must_contain': [
                        'depends on',
                        'facts',
                        'cannot predict'
                    ],
                    'must_not_contain': [
                        'will win',
                        'guaranteed success',
                        '100% chance'
                    ],
                    'must_have_disclaimer': True
                },
                'category': 'outcome_prediction',
                'priority': 'CRITICAL'
            }
        ]

    def run_test(self, test_case: Dict, ai_response: str) -> Dict:
        """
        Run a single test case

        Args:
            test_case: Test case definition
            ai_response: AI-generated response to test

        Returns:
            Test result with pass/fail and details
        """
        failures = []
        warnings = []

        # Check must_contain
        for term in test_case['expected'].get('must_contain', []):
            if term.lower() not in ai_response.lower():
                failures.append(f"Missing required term: '{term}'")

        # Check must_not_contain
        for term in test_case['expected'].get('must_not_contain', []):
            if term.lower() in ai_response.lower():
                failures.append(f"Contains forbidden term: '{term}'")

        # Check section citation
        if 'must_cite_section' in test_case['expected']:
            section = test_case['expected']['must_cite_section']
            section_pattern = f"Section {section}"
            if section_pattern not in ai_response:
                failures.append(f"Missing required section citation: Section {section}")

        # Check Act citation
        if 'must_cite_act' in test_case['expected']:
            act = test_case['expected']['must_cite_act']
            act_found = False

            act_keywords = {
                'IPC': ['IPC', 'Indian Penal Code'],
                'CrPC': ['CrPC', 'Code of Criminal Procedure'],
                'CPC': ['CPC', 'Code of Civil Procedure'],
                'NI_ACT': ['Negotiable Instruments Act', 'NI Act'],
                'GST_ACT': ['GST Act', 'CGST', 'SGST'],
                'DPDP_ACT': ['DPDP', 'Digital Personal Data Protection Act'],
                'CONSUMER_ACT': ['Consumer Protection Act'],
                'CONTRACT_ACT': ['Contract Act', 'Indian Contract Act'],
                'CONSTITUTION': ['Constitution of India', 'Constitution']
            }

            if act in act_keywords:
                for keyword in act_keywords[act]:
                    if keyword in ai_response:
                        act_found = True
                        break

            if not act_found:
                failures.append(f"Missing required Act citation: {act}")

        # Check disclaimer
        if test_case['expected'].get('must_have_disclaimer', False):
            disclaimer_found = False
            disclaimer_patterns = [
                'legal advice', 'consult', 'advocate', 'lawyer',
                'general', 'educational', 'not final'
            ]

            for pattern in disclaimer_patterns:
                if pattern.lower() in ai_response.lower():
                    disclaimer_found = True
                    break

            if not disclaimer_found:
                warnings.append("Missing legal disclaimer")

        # Determine pass/fail
        passed = len(failures) == 0

        return {
            'test_id': test_case['id'],
            'test_name': test_case['name'],
            'category': test_case['category'],
            'priority': test_case['priority'],
            'passed': passed,
            'failures': failures,
            'warnings': warnings,
            'response_length': len(ai_response)
        }

    def run_all_tests(self, ai_generate_func) -> Dict:
        """
        Run all test cases

        Args:
            ai_generate_func: Function that takes input and returns AI response

        Returns:
            Complete test suite results
        """
        results = []
        passed = 0
        failed = 0
        critical_failures = 0

        for test_case in self.test_cases:
            # Generate AI response
            try:
                ai_response = ai_generate_func(test_case['input'])
            except Exception as e:
                results.append({
                    'test_id': test_case['id'],
                    'test_name': test_case['name'],
                    'category': test_case['category'],
                    'priority': test_case['priority'],
                    'passed': False,
                    'failures': [f"AI generation failed: {str(e)}"],
                    'warnings': [],
                    'response_length': 0
                })
                failed += 1
                if test_case['priority'] == 'CRITICAL':
                    critical_failures += 1
                continue

            # Run test
            result = self.run_test(test_case, ai_response)
            results.append(result)

            if result['passed']:
                passed += 1
            else:
                failed += 1
                if test_case['priority'] == 'CRITICAL':
                    critical_failures += 1

        # Calculate statistics
        total = len(self.test_cases)
        pass_rate = (passed / total * 100) if total > 0 else 0

        # Determine overall status
        if critical_failures > 0:
            status = "CRITICAL_FAILURE"
        elif pass_rate >= 90:
            status = "EXCELLENT"
        elif pass_rate >= 80:
            status = "GOOD"
        elif pass_rate >= 70:
            status = "ACCEPTABLE"
        else:
            status = "UNACCEPTABLE"

        return {
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': round(pass_rate, 2),
            'critical_failures': critical_failures,
            'status': status,
            'results': results,
            'summary_by_category': self._summarize_by_category(results),
            'summary_by_priority': self._summarize_by_priority(results)
        }

    def _summarize_by_category(self, results: List[Dict]) -> Dict:
        """Summarize results by category"""
        categories = {}

        for result in results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'passed': 0, 'failed': 0}

            categories[cat]['total'] += 1
            if result['passed']:
                categories[cat]['passed'] += 1
            else:
                categories[cat]['failed'] += 1

        # Calculate pass rates
        for cat in categories:
            total = categories[cat]['total']
            passed = categories[cat]['passed']
            categories[cat]['pass_rate'] = round(passed / total * 100, 2) if total > 0 else 0

        return categories

    def _summarize_by_priority(self, results: List[Dict]) -> Dict:
        """Summarize results by priority"""
        priorities = {}

        for result in results:
            pri = result['priority']
            if pri not in priorities:
                priorities[pri] = {'total': 0, 'passed': 0, 'failed': 0}

            priorities[pri]['total'] += 1
            if result['passed']:
                priorities[pri]['passed'] += 1
            else:
                priorities[pri]['failed'] += 1

        # Calculate pass rates
        for pri in priorities:
            total = priorities[pri]['total']
            passed = priorities[pri]['passed']
            priorities[pri]['pass_rate'] = round(passed / total * 100, 2) if total > 0 else 0

        return priorities

    def get_failing_tests(self, results: Dict) -> List[Dict]:
        """Get only failing tests for debugging"""
        return [r for r in results['results'] if not r['passed']]

    def get_critical_failures(self, results: Dict) -> List[Dict]:
        """Get critical priority failures"""
        return [
            r for r in results['results']
            if not r['passed'] and r['priority'] == 'CRITICAL'
        ]


# Global instance
legal_test_suite = LegalTestSuite()
