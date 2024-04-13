import typing as t
import argparse
import httpx
import asyncio
import sys
import aiofiles
import pathlib
from colorama import Fore, Style, init

init(autoreset=True)


WORDLIST_URL = "https://github.com/halfstackpgr/pytha-fuzz/files/14965324/wordlist.txt"


async def download_wordlist(url: str, save_path: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            client.allow_redirects = True
            response = await client.get(url)
            if response.status_code == 200:
                async with aiofiles.open(save_path, "wb") as file:
                    await file.write(response.content)
                return True
            else:
                print(
                    Fore.RED
                    + f"Failed to download wordlist. Status code: {response.status_code}"
                )
                return False
    except Exception as e:
        print(Fore.RED + f"An error occurred while downloading the wordlist: {e}")
        return False


def load_wordlist(wordlist_file: t.Optional[t.Union[pathlib.Path, str]]) -> t.List[str]:
    if isinstance(wordlist_file, str):
        wordlist_path = pathlib.Path(wordlist_file)
    if wordlist_path.exists() is False:
        print(Fore.YELLOW + "No wordlist provided. Downloading default wordlist...")
        download_path = "wordlist.txt"
        if not asyncio.run(download_wordlist(WORDLIST_URL, download_path)):
            print(Fore.RED + "Failed to download the default wordlist. Exiting...")
            sys.exit(1)
        else:
            print(Fore.GREEN + "Default wordlist downloaded successfully.")
            wordlist_file = download_path

    try:
        with open(wordlist_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(Fore.RED + f"Wordlist file '{wordlist_file}' not found.")
        return []
    except Exception as e:
        print(Fore.RED + f"An error occurred while loading the wordlist: {e}")
        return []


def print_status_code(status_code: int) -> str:
    colors = {
        200: Fore.GREEN,
        404: Fore.RED,
        302: Fore.YELLOW,
        500: Fore.MAGENTA,
        403: Fore.BLUE,
        301: Fore.LIGHTYELLOW_EX,
    }
    stem = colors.get(status_code, Fore.WHITE)
    return f"{stem}[{status_code}]{Style.RESET_ALL}"


def print_welcome_message() -> None:
    welcome_text = r"""
██████╗ ██╗   ██╗████████╗██╗  ██╗ █████╗ 
██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔══██╗
██████╔╝ ╚████╔╝    ██║   ███████║███████║
██╔═══╝   ╚██╔╝     ██║   ██╔══██║██╔══██║
██║        ██║      ██║   ██║  ██║██║  ██║
╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
"""
    separator = "-" * 50
    print(Fore.BLUE + welcome_text)
    print(Fore.CYAN + separator)
    print(
        Fore.GREEN
        + "A PYTHA-FUZZ tool developed by Shivang. Join our telegram @pythagorex"
        + "\nLibrary distribution: halfstackpgr | GitHub"
    )
    print(Fore.GREEN + "Getting Issue? Check Github https://github.com/shivangmauryaa")
    print(Fore.CYAN + separator)


def print_farewell_message(author_name: str) -> None:
    separator = "-" * 50
    print(Fore.CYAN + separator)
    print(Fore.BLUE + f"Author: {author_name}")
    print(Fore.CYAN + separator)


async def save_to_file(output_file: t.Union[pathlib.Path, str], text: str):
    try:
        async with aiofiles.open(output_file, "a", encoding="utf-8") as file:
            await file.write(text + "\n")
    except Exception as e:
        print(Fore.RED + f"An error occurred while saving to the output file: {e}")


async def dirsearch(
    target_url: str,
    wordlist: t.List[str],
    max_retries: int = 10,
    timeout: t.Optional[int] = 10,
    user_agent: t.Optional[str] = None,
    follow_redirects: bool = True,
    output_file: t.Optional[t.Union[pathlib.Path, str]] = None,
):
    try:
        async with httpx.AsyncClient() as client:
            if user_agent is not None:
                client.headers = {"User-Agent": user_agent}

            for directory in wordlist:
                url = f"{target_url}/{directory}"
                retries = 0

                while retries <= max_retries:
                    try:
                        response = await client.get(
                            url, timeout=timeout, allow_redirects=follow_redirects
                        )

                        status_code = response.status_code
                        result = f"{print_status_code(status_code)} {url}"
                        print(result)

                        if output_file:
                            await save_to_file(output_file, result)

                        break

                    except httpx.NetworkError as e:
                        if retries < max_retries:
                            retries += 1
                            print(
                                Fore.YELLOW
                                + f"Network error (retrying {retries}/{max_retries}): {e}"
                            )
                            await asyncio.sleep(2**retries)
                        else:
                            print(
                                Fore.RED + f"Network error (max retries reached): {e}"
                            )
                            break

                    except KeyboardInterrupt:
                        print(Fore.YELLOW + "Fuzzing interrupted by user.")
                        return

                    except Exception as e:
                        print(Fore.RED + f"An error occurred: {e}")
                        break

    except asyncio.CancelledError:
        print(Fore.YELLOW + "Fuzzing task was canceled.")


print_welcome_message()


def main():
    parser = argparse.ArgumentParser(description="A Dir-Miner tool.")
    parser.add_argument("-u", "--url", required=True, help="Target URL to search.")
    parser.add_argument(
        "-w", "--wordlist", help="Wordlist file containing directories to check."
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout for HTTP requests (default: 5.0 seconds)",
    )
    parser.add_argument(
        "-ua",
        "--user-agent",
        default="DirectorySearchBot",
        help="Custom User-Agent header for HTTP requests",
    )
    parser.add_argument(
        "-f", "--follow-redirects", action="store_true", help="Follow HTTP redirects"
    )
    parser.add_argument("-o", "--output", help="Output file to save results.")
    parser.add_argument(
        "-r",
        "--retries",
        type=int,
        default=3,
        help="Maximum number of retries for failed requests",
    )

    args = parser.parse_args()

    if args.wordlist is None:
        wordlist = load_wordlist("wordlist.txt")
    else:
        wordlist = load_wordlist(args.wordlist)

    asyncio.run(
        dirsearch(
            args.url,
            wordlist,
            args.retries,
            args.timeout,
            args.user_agent,
            args.follow_redirects,
            args.output,
        )
    )

    print_farewell_message("Shivang | GitHub")

    if args.output:
        sys.exit(0)
