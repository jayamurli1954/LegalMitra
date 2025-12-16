#!/usr/bin/env python3
"""
Legal AI Assistant - Simple Test Script
This script demonstrates the basic functionality of the legal AI assistant.
No database or complex setup required - just Python and an API key!
"""

import os
from typing import Dict, List
import json

# You can use either OpenAI or Anthropic - uncomment the one you want to use

# Option 1: Using OpenAI (uncomment these lines)
"""
from openai import OpenAI
client = OpenAI(api_key="your_openai_key_here")
MODEL = "gpt-4"
"""

# Option 2: Using Anthropic Claude (uncomment these lines)
"""
from anthropic import Anthropic
client = Anthropic(api_key="your_anthropic_key_here")
MODEL = "claude-sonnet-4-20250514"
"""

# System Prompt
SYSTEM_PROMPT = """You are an expert AI legal assistant specializing in the Indian legal system, functioning as a Junior Lawyer to assist Senior Advocates and legal professionals.

Core Responsibilities:
1. Legal Research & Analysis
2. Case Law Citation (proper format: AIR, SCC)
3. Document Drafting
4. Case Preparation
5. Act Interpretation

Knowledge Areas:
- Tax Laws (GST, Income Tax, Service Tax)
- Criminal Laws (BNS, BNSS, BSA + legacy IPC, CrPC)
- Civil Laws (CPC, Contract Act, Property Transfer)
- Corporate Laws (Companies Act, IBC)
- Constitutional Law

Citation Format:
[Year] Volume Reporter Page (Court)
Example: AIR 2023 SC 1234

Response Structure:
1. Issue Identification
2. Applicable Law (with section numbers)
3. Case Law Analysis (with proper citations)
4. Legal Position Summary
5. Practical Advice

Always:
- Provide accurate citations
- Distinguish binding vs persuasive precedents
- Check current status of cases
- Include practical, actionable advice
- Add appropriate disclaimers

Disclaimer: This is for informational purposes only and does not constitute legal advice."""


class LegalAssistant:
    """Simple Legal AI Assistant"""
    
    def __init__(self, api_provider="openai"):
        """Initialize with API provider"""
        self.api_provider = api_provider
        self.conversation_history = []
        
        if api_provider == "openai":
            from openai import OpenAI
            # Get from environment variable or replace with your key
            api_key = os.getenv("OPENAI_API_KEY", "your_openai_key_here")
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4o"
        elif api_provider == "anthropic":
            from anthropic import Anthropic
            # Get from environment variable or replace with your key
            api_key = os.getenv("ANTHROPIC_API_KEY", "your_anthropic_key_here")
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-sonnet-4-20250514"
        else:
            raise ValueError("Provider must be 'openai' or 'anthropic'")
    
    def ask_question(self, question: str, query_type: str = "research") -> str:
        """
        Ask a legal question
        
        Args:
            question: The legal question to ask
            query_type: Type of query - research/drafting/opinion/case_prep
        
        Returns:
            AI response with legal analysis
        """
        # Add query type context
        enhanced_question = f"Query Type: {query_type}\n\n{question}"
        
        if self.api_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": enhanced_question}
                ],
                temperature=0.3,  # Lower for more consistent legal answers
                max_tokens=3000
            )
            return response.choices[0].message.content
        
        elif self.api_provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": enhanced_question}
                ],
                temperature=0.3
            )
            return response.content[0].text
    
    def draft_document(self, document_type: str, details: Dict) -> str:
        """
        Draft a legal document
        
        Args:
            document_type: petition/reply/notice/opinion
            details: Dictionary with document details
        
        Returns:
            Drafted document
        """
        prompt = f"""
Please draft a {document_type} with the following details:

{json.dumps(details, indent=2)}

Provide a complete, professionally formatted {document_type} following 
Indian legal standards.
"""
        return self.ask_question(prompt, query_type="drafting")
    
    def search_case_law(self, topic: str, court: str = None, year: int = None) -> str:
        """
        Search for relevant case laws
        
        Args:
            topic: Legal topic or issue
            court: Specific court (optional)
            year: Specific year (optional)
        
        Returns:
            Relevant case laws with citations
        """
        filters = []
        if court:
            filters.append(f"Court: {court}")
        if year:
            filters.append(f"Year: {year}")
        
        filter_text = " | ".join(filters) if filters else ""
        
        prompt = f"""
Search for case laws on: {topic}
{filter_text}

Please provide:
1. Case name and proper citation
2. Court and year
3. Key legal principle (ratio decidendi)
4. Relevance to the topic
5. Current status

Provide at least 3-5 relevant cases.
"""
        return self.ask_question(prompt, query_type="research")
    
    def explain_section(self, act_name: str, section: str) -> str:
        """
        Explain a section of an Act
        
        Args:
            act_name: Name of the Act
            section: Section number
        
        Returns:
            Explanation of the section
        """
        prompt = f"""
Explain Section {section} of {act_name}:

1. Provide the section text (if known)
2. Explain its meaning and scope
3. Key points and interpretations
4. Relevant case laws applying this section
5. Practical implications

Be detailed and cite supporting cases.
"""
        return self.ask_question(prompt, query_type="research")


def print_header():
    """Print application header"""
    print("="*80)
    print(" "*25 + "LEGAL AI ASSISTANT")
    print(" "*20 + "Indian Legal System Expert")
    print("="*80)
    print()


def print_menu():
    """Print main menu"""
    print("\n" + "="*80)
    print("MAIN MENU:")
    print("1. Ask a Legal Question (Research)")
    print("2. Search Case Laws")
    print("3. Explain Act Section")
    print("4. Draft Document")
    print("5. Example Queries")
    print("6. Exit")
    print("="*80)


def run_examples(assistant: LegalAssistant):
    """Run example queries"""
    print("\n" + "="*80)
    print("RUNNING EXAMPLE QUERIES...")
    print("="*80)
    
    examples = [
        {
            "title": "GST Limitation Period",
            "question": "What is the limitation period for filing a GST appeal under CGST Act?",
            "type": "research"
        },
        {
            "title": "Case Law Search",
            "question": "Find Supreme Court cases on arbitration clause interpretation under Arbitration Act 1996",
            "type": "research"
        },
        {
            "title": "Section Explanation",
            "question": "Explain Section 16 of CGST Act 2017 regarding Input Tax Credit",
            "type": "research"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*80}")
        print(f"EXAMPLE {i}: {example['title']}")
        print(f"{'='*80}")
        print(f"\nQuestion: {example['question']}\n")
        print("Response:")
        print("-"*80)
        
        try:
            response = assistant.ask_question(example['question'], example['type'])
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\n" + "="*80)
        input("\nPress Enter to continue to next example...")


def main():
    """Main application"""
    print_header()
    
    # Choose API provider
    print("Choose API Provider:")
    print("1. OpenAI (GPT-4)")
    print("2. Anthropic (Claude)")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice == "1":
            provider = "openai"
            break
        elif choice == "2":
            provider = "anthropic"
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    # Initialize assistant
    try:
        assistant = LegalAssistant(api_provider=provider)
        print(f"\n✅ Legal AI Assistant initialized with {provider.upper()}")
    except Exception as e:
        print(f"\n❌ Error initializing assistant: {str(e)}")
        print("\nPlease check:")
        print("1. API key is set in environment variable or in the script")
        print("2. Required library is installed (pip install openai OR pip install anthropic)")
        return
    
    # Main loop
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            # Ask legal question
            print("\n" + "="*80)
            print("LEGAL RESEARCH QUERY")
            print("="*80)
            question = input("\nEnter your legal question: ").strip()
            
            if question:
                print("\n🔍 Researching...\n")
                try:
                    response = assistant.ask_question(question)
                    print("="*80)
                    print("RESPONSE:")
                    print("="*80)
                    print(response)
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
        
        elif choice == "2":
            # Search case laws
            print("\n" + "="*80)
            print("CASE LAW SEARCH")
            print("="*80)
            topic = input("\nEnter topic/issue: ").strip()
            court = input("Enter court (optional, press Enter to skip): ").strip() or None
            year_input = input("Enter year (optional, press Enter to skip): ").strip()
            year = int(year_input) if year_input else None
            
            if topic:
                print("\n🔍 Searching case laws...\n")
                try:
                    response = assistant.search_case_law(topic, court, year)
                    print("="*80)
                    print("CASE LAWS FOUND:")
                    print("="*80)
                    print(response)
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
        
        elif choice == "3":
            # Explain section
            print("\n" + "="*80)
            print("SECTION EXPLANATION")
            print("="*80)
            act_name = input("\nEnter Act name (e.g., 'CGST Act 2017'): ").strip()
            section = input("Enter section number: ").strip()
            
            if act_name and section:
                print("\n🔍 Analyzing section...\n")
                try:
                    response = assistant.explain_section(act_name, section)
                    print("="*80)
                    print("SECTION EXPLANATION:")
                    print("="*80)
                    print(response)
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
        
        elif choice == "4":
            # Draft document
            print("\n" + "="*80)
            print("DOCUMENT DRAFTING")
            print("="*80)
            print("\nDocument Types:")
            print("1. Petition")
            print("2. Reply to Notice")
            print("3. Legal Notice")
            print("4. Legal Opinion")
            
            doc_type = input("\nEnter document type: ").strip()
            
            print("\nEnter document details:")
            facts = input("Facts (brief summary): ").strip()
            parties = input("Parties involved: ").strip()
            relief = input("Relief sought: ").strip()
            
            details = {
                "facts": facts,
                "parties": parties,
                "relief_sought": relief
            }
            
            print("\n📝 Drafting document...\n")
            try:
                response = assistant.draft_document(doc_type, details)
                print("="*80)
                print("DRAFTED DOCUMENT:")
                print("="*80)
                print(response)
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        elif choice == "5":
            # Run examples
            run_examples(assistant)
        
        elif choice == "6":
            # Exit
            print("\n" + "="*80)
            print("Thank you for using Legal AI Assistant!")
            print("="*80)
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        input("\n\nPress Enter to continue...")


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                       LEGAL AI ASSISTANT - SETUP                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

BEFORE RUNNING:

1. Install required package:
   pip install openai        (for OpenAI)
   OR
   pip install anthropic     (for Anthropic Claude)

2. Set your API key:
   
   Option A - In this file (line 16-23):
   Replace "your_openai_key_here" or "your_anthropic_key_here" with actual key
   
   Option B - Environment variable (recommended):
   export OPENAI_API_KEY="your_key_here"     (Mac/Linux)
   OR
   set OPENAI_API_KEY="your_key_here"        (Windows)

3. Run the script:
   python legal_assistant_test.py

═══════════════════════════════════════════════════════════════════════════
""")
    
    input("Press Enter to start the Legal AI Assistant...")
    main()
