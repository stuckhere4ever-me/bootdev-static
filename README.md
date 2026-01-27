# bootdev-static
This is a static site generator for the [bootdev project](https://www.boot.dev/courses/build-static-site-generator-python).
Written from December 27th 2025 to January 6th 2026.

## Project Structure
Project is broken down into the following structure:
- Files:
  - build.sh -> Runs main.py with the github repo information and generates the website
  - main.sh -> Runs main.py assuming locally hosted and generates the website.  Note this is still using the docs directory
  - test.sh -> Runs all unit tests 
    - ```python3 -m unittest discover -s test``` 
    - Assumes all tests are located in the test directory 
- Directories: 
  - content/ -> Markdown files containing content to be generated
  - docs/ -> Final Website Build
  - src/ -> Application Python Code
  - static/ -> Static Website Resources
  - template/ -> HTML Template
  - test/ -> Python unit tests

## Usage
```./build.sh``` -> Will generate the files into the docs directory and assume website will be hosted at the repo root (bootdev-static) 

Final Website Location:
[Tolkein Fan Club](https://stuckhere4ever-me.github.io/bootdev-static/)
