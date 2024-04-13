# Directory Search Tool (FUZZER)


![Ruff](https://camo.githubusercontent.com/18c26428c337f9d641fa09b629a3a03b514e8ac84b57974a0ed7d1b38e14e060/68747470733a2f2f696d672e736869656c64732e696f2f656e64706f696e743f75726c3d68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f61737472616c2d73682f727566662f6d61696e2f6173736574732f62616467652f76322e6a736f6e) 
![Passing Package](https://github.com/halfstackpgr/pytha-fuzz/actions/workflows/python-publish.yml/badge.svg)
![Static Badge](https://img.shields.io/badge/python-Strict-checking?style=plastic&logo=python&label=Type-Checking&labelColor=yellow)

![FUZZER Logo](https://static.thenounproject.com/png/2221438-200.png)



> [!IMPORTANT]
> The current author does not own the repository. It is owned by [Shivang](https://github.com/shivangmauryaa/pytha-fuzz). This is just a module distribution instead of direct source code. Kindly star the original repository if you want to.



## Introduction

FUZZER is a simple pytha-fuzz tool developed by Shivang-Maurya It helps you discover directories on a target website by probing different paths. This tool is designed for security testing, web application analysis, and penetration testing.

## Features

- Fast and efficient directory scanning
- Customizable User-Agent header
- Option to follow HTTP redirects
- Verbose mode for detailed output
- Save results to an output file
- Colorful and user-friendly command-line interface

## Installation

1. Install from Build:
   ```shell
   git clone https://github.com/shivangmauryaa/pytha-fuzz.git
   cd pytha-fuzz
   python setup.py install
   ```
2. Install from PyPi as Module (Recommended):
   ```shell
   pip install pytha-fuzz
   ```

## Usage

Use the following command-line arguments to run pytha-fuzz:
```shell
-u or --url: The target URL to search (required).
-w or --wordlist: Wordlist file containing directories to check.
-t or --timeout: Timeout for HTTP requests (default: 5.0 seconds).
-ua or --user-agent: Custom User-Agent header for HTTP requests (default: DirectorySearchBot).
-f or --follow-redirects: Follow HTTP redirects (optional).
-v or --verbose: Enable verbose mode (optional).
-o or --output: Output file to save results (optional).
```

Example usage:
```shell
fuzz -u http://example.com -w wordlist.txt -o output.txt    // Custom
fuzz -u http://example.com // Auto
```



## Author
[Shivang Maurya](https://github.com/shivangmauryaa)
[<img src="https://github.com/halfstackpgr/pytha-fuzz/assets/118044992/5c0af136-eafa-4641-ae73-4b683c582f64" width="30" style="border-radius: 50%;">](https://www.linkedin.com/in/shivangmauryaa/)


#### Dist Maintainer:
[halfstackpgr](https://github.com/halfstackpgr/pytha-fuzz)


## License

This tool is licensed under the MIT License. See the LICENSE file for details.

## Support
For bug reports, feature requests, or general inquiries, please create an issue. for more good result use your self made wordlist 
