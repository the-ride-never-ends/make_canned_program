# Make Canned Program

## Overview
This program creates a skeleton framework for a new program based on customizable modules and configurations. It streamlines the process of setting up a new project by handling directory creation, module selection, and file management.

## NOTE
This program relies on a custom module folder that is not included in this repo due to privacy reasons.
A sanitized version of this folder is forthcoming.

## Key Features
- Interactive program naming
- Custom module selection
- Automatic directory creation
- Module copying and unpacking
- Requirements file concatenation
- README generation
- Debug and I/O folder setup

## Dependencies
This program relies on Python's 3.12 standard library and does not require external dependencies.
The program is only tested on WSL, but should work in Windows as well. Batch files are forthcoming.

## Usage
To use this program, run it as follows:
```bash
cd path/to/make_canned_program
python main.py
```
Or
```bash
~/.bashrc export PATH=$PATH:/path/to/make_canned_program/start.sh
