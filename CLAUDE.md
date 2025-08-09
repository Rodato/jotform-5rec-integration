# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based JotForm API integration system for the 5REC (Reporte Empresarial Consolidado) project. It automates form prefilling, data extraction, and email notifications for multiple organizations.

## Architecture & Key Components

### Core Modules
- `conection.py` - Basic JotForm API connectivity testing
- `formMetadata.py` - Extracts form structure and fields to CSV/Excel/JSON
- `prefillTemplate.py` / `prefillTemplate_v1.py` - Generates Excel templates with form field mapping
- `prefillUpdate_sendmail.py` / `prefillUpdate_sendmail_v1.py` - Full automation pipeline for bulk processing
- `debugPrefill.py` - API troubleshooting and debugging utilities

### Data Flow Architecture
1. **Form Analysis** → Extract metadata and field structure from JotForm
2. **Template Generation** → Create Excel templates with field mapping and validation
3. **Data Processing** → Read Excel data and create prefilled submissions
4. **Email Distribution** → Send personalized emails with unique prefilled form links

## Common Commands

### Testing & Development
```bash
# Test JotForm API connection
python conection.py

# Extract form metadata
python formMetadata.py

# Generate Excel templates
python prefillTemplate.py

# Debug API issues
python debugPrefill.py
```

### Production Operations
```bash
# Process bulk data and send emails
python prefillUpdate_sendmail.py

# Alternative version with enhanced features
python prefillUpdate_sendmail_v1.py
```

## Key Technologies & Dependencies

**Core Libraries:**
- `requests` - JotForm API communication
- `pandas` - Data manipulation and Excel processing
- `openpyxl` - Excel file generation and formatting
- `fuzzywuzzy` - Fuzzy string matching for field mapping
- `smtplib` + `email.mime` - Email automation

## Critical Security Notes

⚠️ **API credentials are currently hardcoded in source files and must be moved to environment variables**

Expected environment variables:
- `JOTFORM_API_KEY` - JotForm API key
- `GMAIL_USER` - Gmail username for email sending
- `GMAIL_PASSWORD` - Gmail app password

## Form Field Mapping System

The system uses fuzzy string matching to map Excel column headers to JotForm field names. Key mapping rules:
- Automatic similarity-based matching with configurable thresholds
- Manual mapping overrides in `manual_mapping` dictionaries
- Special handling for dropdown/checkbox fields with option mapping
- Multi-language support (Spanish field names)

## Excel Template Structure

Generated templates include:
- **Instructions sheet** with usage guidelines
- **Data input sheets** with field validation and formatting
- **Field mapping reference** for troubleshooting
- **Dropdown options** for fields requiring specific values

## Email Template System

HTML email templates with:
- Organization-specific personalization
- Embedded prefilled form links
- Professional formatting with company branding
- Automatic success/failure reporting

## Debugging & Troubleshooting

Use `debugPrefill.py` for:
- Testing API connectivity and authentication
- Validating form field structures
- Checking prefill data formatting
- Troubleshooting submission failures

## Data Processing Notes

- Input Excel files should match generated template structure
- Organization names in Excel must match email distribution list
- Empty cells are handled gracefully (converted to empty strings)
- Special characters in data are properly encoded for URL parameters