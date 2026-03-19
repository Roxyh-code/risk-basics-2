import requests
import pandas as pd
import xml.etree.ElementTree as ET

API_URL = "https://www.treasurydirect.gov/TA_WS/securities/auctioned"
XML_BASE = "https://www.treasurydirect.gov/xml/"

def get_xml_links(start_date, end_date):
    r = requests.get(API_URL, params={"format": "json", "type": "Bond"})
    r.raise_for_status()
    data = r.json()

    start = pd.to_datetime(start_date).date()
    end = pd.to_datetime(end_date).date()

    links = []

    for row in data:
        try:
            auction_date = pd.to_datetime(row["auctionDate"]).date()
        except:
            continue

        if not (start <= auction_date <= end):
            continue

        xml_file = row.get("xmlFilenameCompetitiveResults")
        if xml_file:
            links.append(XML_BASE + xml_file)

    return links

def parse_xml(xml_url):
    r = requests.get(xml_url)
    r.raise_for_status()
    root = ET.fromstring(r.content)

    result = {"XMLUrl": xml_url}

    for e in root.iter():
        text = e.text.strip() if e.text else ""
        if text:
            result[e.tag.split("}", 1)[-1]] = text

    return result

def main(start_date, end_date, output_file):
    links = get_xml_links(start_date, end_date)

    results = []
    for link in links:
        try:
            results.append(parse_xml(link))
        except:
            pass

    pd.DataFrame(results).to_excel(output_file, index=False)
    print(f"Saved {len(results)} rows to {output_file}")

if __name__ == "__main__":
    main("2026-01-01", "2026-03-31", "bond_results.xlsx")