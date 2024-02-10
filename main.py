from src.util import extract_tabs, convert_to_pdf, get_full_url, fetch_html

if __name__ == "__main__":
    tab_identifier = input("Enter the complete URL or the part after /tab/: ")
    tab_url = get_full_url(tab_identifier)

    webpage = fetch_html(tab_url)

    text = extract_tabs(webpage)

    convert_to_pdf(tab_identifier.split('/')[-1], text)

    print("Tab successfully downloaded and converted to PDF.")

