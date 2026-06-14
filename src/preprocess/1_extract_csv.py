import csv
import os
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from src.preprocess import RAW_CSV_PATH, WEB_SOURCE_PATH

HEADERS = ["Index", "Image", "Code", "Surname", "Middle name", "Given name"]


def load_html_content(source: Path) -> str:
    with open(source, "r", encoding="utf-8") as file:
        return file.read()


def parse_html_table(html_content: str) -> list[list[str]]:
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"id": "id"})

    if not table:
        return []

    tbody = table.find("tbody")
    if not tbody:
        return []

    def extract_row_data(tr: BeautifulSoup) -> list[str]:
        tds = tr.find_all("td")
        if len(tds) < 6:
            return []

        img_tag = tds[1].find("img")
        img_url = str(img_tag.get("src", "")) if img_tag else ""

        return [
            tds[0].get_text(strip=True),  # Index
            img_url,  # Image URL
            tds[2].get_text(strip=True),  # Student Code / Roll Number
            tds[3].get_text(strip=True),  # Surname
            tds[4].get_text(strip=True),  # Middle Name
            tds[5].get_text(strip=True),  # Given Name
        ]

    trs: Any = tbody.find_all("tr")
    row_data = list(map(extract_row_data, trs))

    return row_data


def save_to_csv(data: list[list[str]], csv_path: Path) -> None:
    os.makedirs(csv_path.parent, exist_ok=True)

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(HEADERS)
        writer.writerows(data)


def pipeline_html_to_csv(html_path: Path, csv_path: Path) -> bool:
    try:
        html_content = load_html_content(html_path)
        table_data = parse_html_table(html_content)
        save_to_csv(table_data, csv_path)
        print(f"Successful convert {html_path} to {csv_path}")
        return True
    except Exception as e:
        print(f"Failed when convert {html_path} to {csv_path}")
        print(e)
        return False


def process_on_scrape_data() -> None:
    htmls = list(WEB_SOURCE_PATH.glob("*.html"))

    for html in htmls:
        subject = html.stem

        pipeline_html_to_csv(
            WEB_SOURCE_PATH / f"{subject}.html",
            RAW_CSV_PATH / f"{subject}.csv",
        )


if __name__ == "__main__":
    process_on_scrape_data()
