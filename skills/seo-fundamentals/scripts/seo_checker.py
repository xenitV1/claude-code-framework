#!/usr/bin/env python3
"""
SEO Checker - Basic SEO audit for web projects
Checks HTML files for meta tags, headings, and structured data.

Usage:
    python seo_checker.py <project_path>

Checks:
    - Title tags
    - Meta description
    - Open Graph tags
    - Heading hierarchy
    - Image alt attributes
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass


def find_html_files(project_path: Path) -> list:
    """Find all HTML/JSX/TSX files."""
    patterns = ['**/*.html', '**/*.htm', '**/*.jsx', '**/*.tsx']
    skip_dirs = {'node_modules', '.next', 'dist', 'build', '.git'}
    
    files = []
    for pattern in patterns:
        for f in project_path.glob(pattern):
            if not any(skip in f.parts for skip in skip_dirs):
                files.append(f)
    
    return files[:50]  # Limit to 50 files


def check_html_file(file_path: Path) -> dict:
    """Check a single HTML file for SEO issues."""
    issues = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Check for title tag
        if '<title>' not in content.lower() and 'Head>' not in content:
            if 'page' in file_path.name.lower() or 'index' in file_path.name.lower():
                issues.append("Missing <title> tag")
        
        # Check for meta description
        if 'meta' in content.lower() and 'description' not in content.lower():
            if '<head' in content.lower() or 'Head>' in content:
                issues.append("Missing meta description")
        
        # Check for Open Graph tags
        if 'og:' not in content and 'property="og' not in content:
            if 'page' in file_path.name.lower() or 'index' in file_path.name.lower():
                issues.append("Missing Open Graph tags (og:title, og:description)")
        
        # Check heading hierarchy
        h1_count = len(re.findall(r'<h1[>\s]', content, re.IGNORECASE))
        if h1_count > 1:
            issues.append(f"Multiple H1 tags found ({h1_count})")
        
        # Check images for alt attributes
        img_matches = re.findall(r'<img[^>]+>', content, re.IGNORECASE)
        for img in img_matches:
            if 'alt=' not in img.lower() or 'alt=""' in img or "alt=''" in img:
                issues.append("Image missing alt attribute")
                break  # Report only once per file
        
    except Exception as e:
        issues.append(f"Error reading file: {str(e)[:50]}")
    
    return {
        "file": str(file_path.name),
        "issues": issues
    }


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[SEO CHECKER] Basic SEO Audit")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    # Find HTML files
    files = find_html_files(project_path)
    print(f"Found {len(files)} HTML/JSX/TSX files")
    
    if not files:
        output = {
            "script": "seo_checker",
            "project": str(project_path),
            "files_checked": 0,
            "issues_found": 0,
            "passed": True,
            "message": "No HTML files found"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    # Check each file
    all_issues = []
    
    for f in files:
        result = check_html_file(f)
        if result["issues"]:
            all_issues.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("SEO ISSUES")
    print("="*60)
    
    if all_issues:
        for item in all_issues[:10]:  # Show max 10 files
            print(f"\n{item['file']}:")
            for issue in item["issues"]:
                print(f"  - {issue}")
        
        if len(all_issues) > 10:
            print(f"\n... and {len(all_issues) - 10} more files with issues")
    else:
        print("No SEO issues found!")
    
    total_issues = sum(len(item["issues"]) for item in all_issues)
    passed = total_issues == 0
    
    output = {
        "script": "seo_checker",
        "project": str(project_path),
        "files_checked": len(files),
        "files_with_issues": len(all_issues),
        "issues_found": total_issues,
        "passed": passed
    }
    
    print("\n" + json.dumps(output, indent=2))
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
