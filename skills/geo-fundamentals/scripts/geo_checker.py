#!/usr/bin/env python3
"""
GEO Checker - Generative Engine Optimization Audit
Checks content for AI citation readiness.
"""
import sys
import re
import json
from pathlib import Path

def check_html_file(file_path: Path) -> dict:
    """Check a single HTML file for GEO elements."""
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    
    issues = []
    passed = []
    
    # 1. Check for structured data (schema.org)
    if 'application/ld+json' in content:
        passed.append("✅ JSON-LD structured data found")
        # Check for specific schemas
        if '"@type":"Article"' in content or '"@type": "Article"' in content:
            passed.append("✅ Article schema present")
        if '"@type":"FAQPage"' in content or '"@type": "FAQPage"' in content:
            passed.append("✅ FAQ schema present")
        if '"@type":"Person"' in content or '"@type": "Person"' in content:
            passed.append("✅ Person/Author schema present")
    else:
        issues.append("❌ No JSON-LD structured data (AI engines prefer structured content)")
    
    # 2. Check for clear headings (H1, H2)
    h1_count = len(re.findall(r'<h1[^>]*>', content, re.I))
    h2_count = len(re.findall(r'<h2[^>]*>', content, re.I))
    if h1_count == 1:
        passed.append("✅ Single H1 heading (good for entity clarity)")
    elif h1_count == 0:
        issues.append("❌ No H1 heading found")
    else:
        issues.append(f"⚠️ Multiple H1 headings ({h1_count}) - use only one")
    
    if h2_count >= 3:
        passed.append(f"✅ Good heading structure ({h2_count} H2s)")
    else:
        issues.append("⚠️ Add more H2 subheadings for scannable content")
    
    # 3. Check for author information
    author_patterns = [
        r'author', r'byline', r'written-by', r'contributor'
    ]
    has_author = any(p in content.lower() for p in author_patterns)
    if has_author:
        passed.append("✅ Author attribution found")
    else:
        issues.append("❌ No author information (AI prefers attributed content)")
    
    # 4. Check for dates/timestamps
    date_patterns = [
        r'datetime=', r'pubdate', r'datePublished', r'dateModified',
        r'published:', r'updated:', r'last.?updated'
    ]
    has_date = any(re.search(p, content, re.I) for p in date_patterns)
    if has_date:
        passed.append("✅ Date/timestamp found")
    else:
        issues.append("❌ No publication date (freshness signals matter)")
    
    # 5. Check for FAQ section
    faq_patterns = [r'<details', r'faq', r'frequently.?asked', r'q\s*&\s*a']
    has_faq = any(re.search(p, content, re.I) for p in faq_patterns)
    if has_faq:
        passed.append("✅ FAQ section detected")
    else:
        issues.append("⚠️ Consider adding FAQ section (highly citable)")
    
    # 6. Check for statistics/data
    stat_patterns = [r'\d+%', r'\$\d+', r'million', r'billion', r'study shows', r'research']
    has_stats = any(re.search(p, content, re.I) for p in stat_patterns)
    if has_stats:
        passed.append("✅ Statistics/data found (original data gets cited)")
    
    # 7. Check for definition patterns
    definition_patterns = [r'is defined as', r'refers to', r'means that', r'<dfn']
    has_definitions = any(re.search(p, content, re.I) for p in definition_patterns)
    if has_definitions:
        passed.append("✅ Clear definitions found")
    
    # 8. Check for lists (AI loves structured content)
    list_count = len(re.findall(r'<(ul|ol)[^>]*>', content, re.I))
    if list_count >= 2:
        passed.append(f"✅ {list_count} lists found (structured content)")
    
    # 9. Check for tables
    table_count = len(re.findall(r'<table[^>]*>', content, re.I))
    if table_count >= 1:
        passed.append(f"✅ {table_count} table(s) found (comparison data)")
    
    return {
        'file': str(file_path),
        'passed': passed,
        'issues': issues,
        'score': len(passed) / (len(passed) + len(issues)) * 100 if (passed or issues) else 0
    }

def check_markdown_file(file_path: Path) -> dict:
    """Check a markdown file for GEO elements."""
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    
    issues = []
    passed = []
    
    # 1. Check for clear structure
    h1_count = len(re.findall(r'^# [^#]', content, re.M))
    h2_count = len(re.findall(r'^## [^#]', content, re.M))
    
    if h1_count == 1:
        passed.append("✅ Single H1 title")
    elif h1_count == 0:
        issues.append("❌ No H1 title found")
    
    if h2_count >= 3:
        passed.append(f"✅ Good structure ({h2_count} sections)")
    else:
        issues.append("⚠️ Add more sections for scannable content")
    
    # 2. Check for bullet/numbered lists
    list_items = len(re.findall(r'^[\-\*\d\.]\s', content, re.M))
    if list_items >= 5:
        passed.append(f"✅ {list_items} list items (structured content)")
    
    # 3. Check for code blocks (technical credibility)
    code_blocks = len(re.findall(r'```', content))
    if code_blocks >= 2:
        passed.append("✅ Code examples included")
    
    # 4. Check for tables
    if '|' in content and '---' in content:
        passed.append("✅ Tables found (comparison data)")
    
    # 5. Check for links/citations
    links = len(re.findall(r'\[.*?\]\(.*?\)', content))
    if links >= 3:
        passed.append(f"✅ {links} links/citations")
    else:
        issues.append("⚠️ Add more source citations")
    
    return {
        'file': str(file_path),
        'passed': passed,
        'issues': issues,
        'score': len(passed) / (len(passed) + len(issues)) * 100 if (passed or issues) else 0
    }

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = Path(target)
    
    print("\n" + "🤖" * 30)
    print("GEO CHECKER - Generative Engine Optimization Audit")
    print("🤖" * 30 + "\n")
    
    results = []
    
    # Find HTML and MD files
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.rglob("*.html")) + list(target_path.rglob("*.md"))
        # Exclude common non-content files
        files = [f for f in files if not any(x in str(f) for x in ['node_modules', '.git', 'dist', 'build', 'README', 'CHANGELOG'])]
    
    if not files:
        print("⚠️ No HTML or Markdown files found to check.")
        return
    
    for file_path in files[:20]:  # Limit to 20 files
        if file_path.suffix.lower() == '.html':
            result = check_html_file(file_path)
        else:
            result = check_markdown_file(file_path)
        results.append(result)
    
    # Print results
    total_score = 0
    for result in results:
        print(f"\n📄 {result['file']}")
        print(f"   Score: {result['score']:.0f}%")
        for item in result['passed']:
            print(f"   {item}")
        for item in result['issues']:
            print(f"   {item}")
        total_score += result['score']
    
    avg_score = total_score / len(results) if results else 0
    
    print("\n" + "=" * 60)
    print(f"📊 AVERAGE GEO SCORE: {avg_score:.0f}%")
    print("=" * 60)
    
    if avg_score >= 80:
        print("✅ EXCELLENT - Content is well-optimized for AI citations")
    elif avg_score >= 60:
        print("⚠️ GOOD - Some improvements recommended")
    elif avg_score >= 40:
        print("⚠️ NEEDS WORK - Add structured elements")
    else:
        print("❌ POOR - Content needs significant GEO optimization")
    
    # Exit code based on score
    sys.exit(0 if avg_score >= 60 else 1)

if __name__ == "__main__":
    main()
