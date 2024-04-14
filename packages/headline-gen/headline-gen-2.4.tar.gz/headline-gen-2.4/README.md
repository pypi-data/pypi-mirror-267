
# Headline Generation Package

This is a Python package for generating headlines from Articles.

## Installation

You can install the package using pip:

```bash
pip install headline-gen
```

## Usage

```python
from headline_gen.Control import ServerCntrl, Generate

# Run this once to start the server
Server = ServerCntrl("Start")

# Generate headline from article text
headline = Generate("Your article text goes here...", Server)
print(headline)

# Stop the server when done
ServerCntrl("Stop", Server)
```

## Description

This package provides functionality to generate headlines from article text using natural language processing techniques.

## Usage Instructions

1. Import the `ServerCntrl` and `Generate` functions from the `Control` module.
2. Start the server using `ServerCntrl("Start")`. This only needs to be done once.
3. Generate headlines using the `Generate` function, passing the article text as an argument.
4. Stop the server when done using `ServerCntrl("Stop", Server)`.

## New Release Features (v2.4) and Bug Fixes

1. Fixed a corner case issue causing a ZeroDivisionError when processing irregular parameters for phrase extraction. The package now gracefully handles such scenarios without disrupting functionality.
2. Renamed the function `ServerInit` to `ServerCntrl` for improved clarity and consistency within the codebase.
3. Additionally, streamlined the dependency management by directly including `en_core_web_sm` in the downloader module.
4. Output made more Comprehensive.
