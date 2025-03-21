![Wagtail Content Import](docs/img/wagtail_content_import_logo_with_text.svg)

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/wagtail-content-import.svg?style=flat)](https://pypi.org/project/wagtail-content-import)
[![Build status](https://img.shields.io/github/actions/workflow/status/torchbox/wagtail-content-import/test.yml?branch=main)](https://github.com/torchbox/wagtail-content-import/actions)

Wagtail Content Import is a module for importing page content into Wagtail from third-party sources.
Page content is imported into a StreamField, using a set of customisable mappings.
Currently, it supports:

### As sources:
- Google Docs
- OneDrive/SharePoint

### As files:
- Google Docs documents with:
    - Rich text
    - Tables
    - Images
    - Headings
- Docx files with:
    - Text with bold and italics
    - Headings

### Requirements:
* Python >= 3.9
* Django >= 4.2
* Wagtail >= 6.3

For the full documentation, see: https://torchbox.github.io/wagtail-content-import/

### Note for Google Import

If using Google Docs import, for users to authenticate with Google they must either allow third party cookies or add `accounts.google.com` to their allowed domains ([Settings/Privacy and Security/Cookies and other site data in Chrome](chrome://settings/cookies) or [Preferences/Privacy & Security in Firefox](about:preferences#privacy)).
