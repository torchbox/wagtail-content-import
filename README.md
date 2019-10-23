# Wagtail Content Import

A module for Wagtail that provides functionality for importing page content from third-party sources.
Currently supports only Google Docs. 

### Getting Started

### Basic Usage

### The Content Import Flow

The Wagtail Content Import app provides:
* **Pickers** - which select and import raw document data 
* **Parsers** - which parse the raw document data into a standard intermediate form
* **Mappers** - which convert this intermediate form into a final output (typically a Wagtail StreamField)

The typical flow is as follows, for a Page model with ContentImportMixin:

1. The Create view in the Wagtail Admin provides a button, which calls a picker.

2. The picker enables a document to be selected

### Customising Content Import

### Reference

