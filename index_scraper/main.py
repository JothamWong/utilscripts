import argparse
import os
import re
from urllib.parse import unquote, urljoin, urlparse

import bs4
import requests

DEFAULT_EXTENSIONS = "pdf,md"
DEFAULT_FILENAME = "downloaded_file.html"
CHUNK_SIZE = 8192
REQUEST_TIMEOUT_PAGE = 10
REQUEST_TIMEOUT_FILE = 20

# Ignore Apache-style directory listings
IGNORE_LINK_TEXTS = frozenset(
    [
        "Name",
        "Last modified",
        "Size",
        "Description",
        "Parent Directory",
        "Parent directory",
    ]
)
IGNORE_HREF_PATTERNS = ("?C=N", "?C=M", "?C=S", "?C=D")


def sanitize_filename(filename, default_name="downloaded_file.html"):
    if not filename:
        return default_name
    # Decodes URL-encoded characters (e.g.: %20 -> space)
    name = unquote(filename)
    # Replace invalid chars with underscores
    name = re.sub(r"[^\w.\-_]", "_", name)
    # Collapse multiple underscores into a single underscore
    name = re.sub(r"_+", "_", name)
    # Removes leading/trailing underscores, dots, and spaces
    name = name.strip("._ ")
    return name


def main():
    parser = argparse.ArgumentParser(description="Scrape an index site.")
    parser.add_argument(
        "--url", "-u", type=str, required=True, help="URL of the index site to scrape"
    )
    parser.add_argument(
        "--extensions",
        "-e",
        type=str,
        required=False,
        help="File extensions to get, comma separated",
        default=DEFAULT_EXTENSIONS,
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        required=True,
        help="Path to the output dir to save the scraped data",
    )
    args = parser.parse_args()

    base_url = args.url
    extensions = set(args.extensions.split(","))

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(base_url, timeout=REQUEST_TIMEOUT_PAGE)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        exit(1)

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    for i, link_tag in enumerate(links):
        href = link_tag.get("href")
        link_text = link_tag.get_text(strip=True)

        print(f"Link {i + 1} text: {link_text} raw href: {href}")
        if not href:
            print("No href found, skipping...")
            continue

        if link_text in IGNORE_LINK_TEXTS:
            print(f"Skipping link with text: {link_text}")
            continue

        matches_skip_href_pattern = any(
            href.startswith(pattern) for pattern in IGNORE_HREF_PATTERNS
        )
        if matches_skip_href_pattern:
            print(f"Skipping href with pattern: {href}")
            continue

        if href.startswith("#"):
            print(f"Skipping internal page anchor: {href}")
            continue

        if href.lower().startswith("javascript:"):
            print(f"Skipping javascript link: {href}")
            continue

        if href.lower().split(".")[-1] not in extensions:
            print(f"Skipping due to extension: {href}")
            continue

        # Construct full URL for link using urljoin, which handles both relative
        # and absolute file links
        download_url = urljoin(base_url, href)
        parsed_download_url = urlparse(download_url)
        # Skip non-HTTP/HTTPs links
        if parsed_download_url.scheme not in ["http", "https"]:
            continue

        try:
            print(f"Trying to download {download_url} ({i + 1}/{len(links)})")
            link_response = requests.get(
                download_url, timeout=REQUEST_TIMEOUT_FILE, stream=True
            )
            link_response.raise_for_status()
            # Determine pathname for downloaded content
            path_component = parsed_download_url.path
            filename = os.path.basename(path_component)
            if not filename:
                filename = "index.html"
            sanitized_filename = sanitize_filename(filename)
            # Handle potential collisions
            final_output_path = os.path.join(output_dir, sanitized_filename)
            counter = 1
            temp_filename_base, temp_filename_ext = os.path.splitext(sanitized_filename)
            while os.path.exists(final_output_path):
                final_output_path = os.path.join(
                    output_dir,
                    f"{temp_filename_base}_{counter}{temp_filename_ext}",
                )
                counter += 1
            with open(final_output_path, "wb") as f:
                for chunk in link_response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
            print(f"Downloaded {download_url} to {final_output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {download_url}: {e}")
            continue
        except IOError as e:
            print(f"Error writing to file {final_output_path}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue
        finally:
            print("-" * 30)
    print(f"Finished processing {base_url}")


if __name__ == "__main__":
    main()
