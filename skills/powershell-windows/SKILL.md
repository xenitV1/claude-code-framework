---
name: powershell-windows
description: PowerShell scripting patterns for Windows including common pitfalls, operator syntax, Unicode handling, and best practices. CRITICAL for writing error-free PowerShell scripts on Windows.
---

# PowerShell Windows Patterns

## Overview
This skill contains common pitfalls and correct usage patterns for Windows PowerShell. It enables AI to write error-free PowerShell scripts on Windows.

## Critical Rules

### 1. Operator Usage

Logical operators in PowerShell REQUIRE parentheses!

```powershell
# ❌ WRONG - This will throw an ERROR!
if (Test-Path "file1.txt" -or Test-Path "file2.txt") { }

# ✅ CORRECT - Each Test-Path must be in parentheses
if ((Test-Path "file1.txt") -or (Test-Path "file2.txt")) { }

# ❌ WRONG
if (Test-Path $path -and $variable -eq "value") { }

# ✅ CORRECT
if ((Test-Path $path) -and ($variable -eq "value")) { }
```

### 2. Do Not Use Unicode and Emojis

Unicode emoji characters cause ISSUES in PowerShell!

```powershell
# ❌ WRONG - Throws parser error
Write-Output "✅ Success"
Write-Output "🔴 Error"
Write-Output "⚠️ Warning"

# ✅ CORRECT - Use ASCII characters
Write-Output "[OK] Success"
Write-Output "[!] Error"
Write-Output "[*] Warning"
Write-Output "[+] Added"
Write-Output "[-] Removed"
Write-Output "[?] Question"
```

### Icon Reference Table

| Purpose | DO NOT USE | USE |
|---------|------------|-----|
| Success | ✅ ✓ | [OK] [+] |
| Error | ❌ ✗ 🔴 | [!] [X] |
| Warning | ⚠️ 🟡 | [*] [WARN] |
| Info | ℹ️ 🔵 | [i] [INFO] |
| Critical | 🔴 | [!!] [CRITICAL] |
| Progress | ⏳ | [...] |

### 3. Null Checks

Always check if variables are null:

```powershell
# ❌ WRONG - Throws error if null
if ($array.Count -gt 0) { }

# ✅ CORRECT - Check null first
if ($array -and $array.Count -gt 0) { }

# ❌ WRONG
$text.Length

# ✅ CORRECT
if ($text) { $text.Length }
```

### 4. String Interpolation

Using variables inside strings:

```powershell
# ❌ WRONG - In complex expressions
Write-Output "Duration: $($session.data.duration)"

# ✅ CORRECT - Assign to variable first
$duration = $session.data.duration
Write-Output "Duration: $duration"

# ✅ ALTERNATIVE - Format operator
Write-Output ("Duration: {0}" -f $session.data.duration)
```

### 5. ErrorActionPreference

Always specify at the beginning of the script:

```powershell
# Stop on error (development)
$ErrorActionPreference = "Stop"

# Continue on error (production hooks)
$ErrorActionPreference = "Continue"

# Silently ignore errors
$ErrorActionPreference = "SilentlyContinue"
```

### 6. Try/Catch/Finally

Correct usage:

```powershell
try {
    # Risky code
    $result = Some-RiskyOperation
    
    # DO NOT use return inside try block
    # return $result  # ❌ WRONG
}
catch {
    Write-Warning "Error: $_"
    # Action on error
}
finally {
    # Always runs - for cleanup
}

# Return should be outside the try block
return $result  # ✅ CORRECT
```

### 7. File Paths

For Windows paths:

```powershell
# ❌ WRONG - Linux style
$path = "/home/user/file.txt"

# ✅ CORRECT - Windows style
$path = "C:\Users\User\file.txt"

# ✅ CORRECT - Cross-platform (use Join-Path)
$path = Join-Path $env:USERPROFILE "Documents\file.txt"

# ✅ CORRECT - Escape inside double quotes
$path = "$env:USERPROFILE\.claude\data"
```

### 8. Array Operations

```powershell
# ❌ WRONG - When creating empty array
$array = ()

# ✅ CORRECT
$array = @()

# ❌ WRONG - Adding element to array
$array.Add($item)  # This won't work!

# ✅ CORRECT
$array += $item
# or use ArrayList
$list = [System.Collections.ArrayList]@()
$list.Add($item) | Out-Null
```

### 9. JSON Operations

```powershell
# Reading
$data = Get-Content "file.json" -Raw | ConvertFrom-Json

# Writing - Depth is critical!
$data | ConvertTo-Json -Depth 10 | Out-File "file.json" -Encoding UTF8

# ❌ WRONG - Without specifying depth
$data | ConvertTo-Json  # Nested objects will be lost!

# ✅ CORRECT - Depth 10 is usually enough
$data | ConvertTo-Json -Depth 10
```

### 10. Parameter Definition

```powershell
param(
    # Mandatory parameter
    [Parameter(Mandatory=$true)]
    [string]$RequiredParam,
    
    # Optional with default value
    [string]$OptionalParam = "default",
    
    # Optional with validation
    [ValidateSet("Option1", "Option2")]
    [string]$LimitedParam
)
```

## Common Errors and Solutions

### Error: "A parameter cannot be found that matches parameter name 'or'"

**Cause:** Incorrect usage of the `-or` operator

```powershell
# ❌ Incorrect
if (Test-Path "a" -or Test-Path "b") { }

# ✅ Solution
if ((Test-Path "a") -or (Test-Path "b")) { }
```

### Error: "Unexpected token" or "Missing terminator"

**Cause:** Unicode characters or special symbols

```powershell
# ❌ Incorrect
Write-Output "✅"

# ✅ Solution
Write-Output "[OK]"
```

### Error: "The property 'X' cannot be found on this object"

**Cause:** Missing null check

```powershell
# ❌ Incorrect
$data.property.subproperty

# ✅ Solution
if ($data -and $data.property) {
    $data.property.subproperty
}
```

### Error: "Cannot convert value to type System.String"

**Cause:** Type mismatch

```powershell
# ❌ Incorrect
[string]$value = $complexObject

# ✅ Solution
$value = $complexObject.ToString()
# or
$value = "$complexObject"
```

## Template: Secure PowerShell Script

```powershell
<#
.SYNOPSIS
    Script description
.DESCRIPTION
    Detailed description
.NOTES
    Author: 
    Version: 1.0.0
    Date: YYYY-MM-DD
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$InputParam,
    [string]$OptionalParam = "default"
)

# Strict mode - catches errors
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DataDir = "$env:USERPROFILE\.claude\data"

# Ensure directories exist
if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
}

# Main execution
try {
    # Logic goes here
    
    Write-Output "[OK] Execution completed"
    exit 0
}
catch {
    Write-Warning "Error: $_"
    exit 1
}
```

## Best Practices Summary

1. **Use parentheses** - For all operators
2. **Do not use emojis** - Use ASCII characters
3. **Perform null checks** - For every variable
4. **Specify depth** - In JSON operations
5. **Specify UTF8** - When writing files
6. **Specify ErrorAction** - At script start
7. **Use Try/Catch** - For critical operations
8. **Use Join-Path** - For file paths
