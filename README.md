# Image Matching Framework

## Table of Contents

- [Overview](#Overview)
- [Features](#Features)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Reporting](#reporting)
- [Folder Structure](#folder-structure)
- [Coding Standards](#coding-standards)


## Overview

The Automated Image Comparison Framework is designed to facilitate the comparison of web page screenshots and thumbnails against predefined template images. Utilizing tools such as Playwright for browser automation and OpenCV for image processing, this framework enables efficient validation of visual elements on web pages.

## Features

- **Screenshot Comparison**: Captures full-page screenshots and compares them against template images to identify visual discrepancies.
- **Thumbnail Matching**: Extracts thumbnail images from web pages and compares them with predefined templates to ensure consistency.
- **Logging**: Provides detailed logging of test execution and results for easy debugging and analysis.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aswanirs23/Image-matching-framework.git
   cd Image-matching-framework
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
4. Running Tests:

   To run a Single Test File, use the following command:

   ```bash
   pytest -s test_file.py
   ```

    To run the entire suite, use the following command:

    ```bash
    pytest -s
    ```

## Allure Reporting

You can generate and view the report using:

```bash
allure serve ./allure-results
```


## Folder Structure

Purpose of key folders in project is below:

- `src/pages`: Contains modules that define page objects or components
- `src/utils`: Contains  common functionalities such as file operations, image processing, and logging, which are used across the project
- `tests`: Contains test modules organized by functionality
- `output/logs`: Stores log files generated during the execution of the application or tests. 
- `config.py` : Store configuration settings


## Who do I talk to? ###

* Aswani R S
