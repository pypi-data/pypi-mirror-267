import argparse
import asyncio
import aiofiles
import aiohttp
import pathlib
import sys
import typing as t
from colorama import Fore, Style, init

init(autoreset=True)

WORDLIST_URL = "https://github.com/halfstackpgr/pytha-fuzz/files/14965324/wordlist.txt"


async def download_wordlist(url: str, save_path: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(save_path, "wb") as file:
                        await file.write(await response.read())
                    return True
                else:
                    print(
                        Fore.RED
                        + f"Failed to download wordlist. Status code: {response.status}"
                    )
                    return False
    except Exception as e:
        print(Fore.RED + f"An error occurred while downloading the wordlist: {e}")
        return False


def load_wordlist(wordlist_file: t.Union[pathlib.Path, str]) -> list[str]:
    if isinstance(wordlist_file, pathlib.Path):
        wordlist_path = wordlist_file
    else:
        wordlist_path = pathlib.Path(wordlist_file)

    if wordlist_path.exists() is False:
        print(Fore.YELLOW + "No wordlist provided. Downloading default wordlist...")
        download_path = "wordlist.txt"
        if not asyncio.run(download_wordlist(WORDLIST_URL, download_path)):
            print(Fore.RED + "Failed to download the default wordlist. Exiting...")
            sys.exit(1)

    try:
        with wordlist_path.open("r") as file:
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


async def save_to_file(output_file: str, text: str) -> None:
    try:
        async with aiofiles.open(output_file, "a", encoding="utf-8") as file:
            await file.write(text + "\n")
    except Exception as e:
        print(Fore.RED + f"An error occurred while saving to the output file: {e}")


async def dirsearch(
    target_url: str,
    wordlist: list[str],
    max_retries: int = 10,
    timeout: float = 10.0,
    user_agent: t.Optional[str] = None,
    follow_redirects: bool = True,
    output_file: t.Optional[str] = None,
) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            for directory in wordlist:
                url = f"{target_url}/{directory}"
                retries = 0

                while retries <= max_retries:
                    try:
                        async with session.get(
                            url,
                            timeout=timeout,
                            allow_redirects=follow_redirects,
                            headers={"User-Agent": user_agent} if user_agent else None,
                        ) as response:
                            status_code = response.status
                            result = f"{print_status_code(status_code)} {url}"
                            print(result)

                            if output_file:
                                await save_to_file(output_file, result)

                            break

                    except aiohttp.ClientError as e:
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


def main() -> None:
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

    wordlist_file = args.wordlist or "./wordlist.txt"
    wordlist = load_wordlist(pathlib.Path(wordlist_file))

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


if __name__ == "__main__":
    main()
