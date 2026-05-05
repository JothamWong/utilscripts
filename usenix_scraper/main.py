import argparse
from pathlib import Path
import requests
import bs4
import os
from urllib.parse import urljoin, urlparse


def parse_args():
    ap = argparse.ArgumentParser(description="Scrape a USENIX accepted papers site.")
    ap.add_argument(
        "--url",
        "-u",
        type=str,
        required=True,
        help="URL of the usenix accepted papers to scrape",
    )
    ap.add_argument(
        "--output-dir",
        "-o",
        type=str,
        required=True,
        help="Path to the output dir to save the scraped data",
    )
    ap.add_argument(
        "--media_types",
        "-m",
        nargs="+",
        choices=["slides", "pdf"],
        default=["slides", "pdf"],
        help="Media types to scrape (slides and pdf). Video not supported",
    )
    return ap.parse_args()


def get_soup(session: requests.Session, url: str) -> bs4.BeautifulSoup:
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        raise e
    return bs4.BeautifulSoup(response.text, "html.parser")


def get_links(base_url: str, soup: bs4.BeautifulSoup) -> list[str]:
    """Extract all links from accepted papers"""
    links: list[str] = []
    media_sections = soup.find_all("div", class_="group-available-media")
    for section in media_sections:
        for a in section.find_all("a", href=True):
            href = a["href"].strip()
            links.append(urljoin(base_url, href))
    return list(set(links))


def download_file(session: requests.Session, url: str, output_dir: Path):
    """output_dir already exists"""
    with session.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()

        filename = None
        cd = r.headers.get("Content-Disposition")
        if cd and "filename=" in cd:
            filename = cd.split("filename=")[-1].strip().strip('"')
        if not filename:
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or "downloaded_file"

        filepath = output_dir / filename
        if filepath.exists():
            return

        print(f"\rDownloading: {filename}", end="", flush=True)
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def extract_media(
    session: requests.Session,
    link: str,
    base_url: str,
    output_dir: Path,
    media_types: list[str],
):
    try:
        soup = get_soup(session, link)
    except requests.exceptions.RequestException as e:
        print(f"Encountered error trying to retrieve {link}: {e}")
        return

    try:
        if "pdf" in media_types:
            pdf_tag = soup.select_one(".field-name-field-presentation-pdf a[href]")
            if pdf_tag:
                pdf_url = urljoin(base_url, pdf_tag["href"])
                download_file(session, pdf_url, output_dir)
    except requests.exceptions.RequestException as e:
        print(f"Failed to get PDF for {link}: {e}")

    try:
        if "slides" in media_types:
            slides_tag = soup.select_one(".field-name-field-paper-slides a[href]")
            if slides_tag:
                slides_url = urljoin(base_url, slides_tag["href"])
                download_file(session, slides_url, output_dir)
    except requests.exceptions.RequestException as e:
        print(f"Failed to get slides for {link}: {e}")


if __name__ == "__main__":
    args = parse_args()

    full_url = args.url
    parsed_url = urlparse(full_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    session = requests.Session()

    soup = get_soup(session, args.url)
    links: list[str] = get_links(base_url, soup)

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for link in links:
        extract_media(session, link, base_url, output_dir, args.media_types)

    session.close()