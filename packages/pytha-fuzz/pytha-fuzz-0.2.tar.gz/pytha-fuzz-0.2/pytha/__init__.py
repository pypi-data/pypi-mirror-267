"""
PYTHA - A Directory Fuzzer Tool

PYTHA is a Python-based directory fuzzer tool designed to aid in the discovery of hidden or sensitive directories and files on web servers. It uses an asynchronous approach for efficient scanning and supports various customization options.

Features:
- Asynchronous HTTP requests for fast scanning.
- Customizable user-agent string for HTTP requests.
- Ability to follow HTTP redirects.
- Configurable maximum number of retries for failed requests.
- Option to save results to an output file.

Usage:
You can use PYTHA directly from the terminal by providing the target URL and a wordlist containing directories to check. Additional options such as customizing the user-agent string, setting timeouts, and specifying output files are available for further customization.

Example Usage:
$ fuzz -u http://example.com -w wordlist.txt -o output.txt

Dependencies:
PYTHA relies on the following Python packages:
- httpx: A fast and friendly HTTP client for Python.
- aiofiles: An async file I/O library for Python.
- colorama: A cross-platform library for colored terminal text.


Author:
PYTHA is developed by Shivang. For inquiries, bug reports, or contributions, feel free to contact the author via email or GitHub.

Contact Information:
- Linkden: https://www.linkedin.com/in/shivangmauryaa/
- GitHub: https://github.com/shivangmauryaa/pytha-fuzz
"""

from pytha.main import main  # type: ignore
