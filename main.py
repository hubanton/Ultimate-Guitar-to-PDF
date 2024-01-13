from util import extract_tabs, convert_to_pdf, get_full_url, fetch_html

if __name__ == "__main__":
    tab_identifier = input("Enter the complete URL or the part after /tab/: ")
    tab_url = get_full_url(tab_identifier)

    try:
        webpage = fetch_html(tab_url)

        pre_text, tabs_text, post_text = extract_tabs(webpage)

        convert_to_pdf(pre_text, tabs_text, post_text)

        print("Tab successfully downloaded and converted to PDF.")
    except Exception as e:
        print(f"Error accessing the tab: {e}")
