from playwright.sync_api import sync_playwright

url = "https://note.com/parklabs/n/n36308b66f5c3"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")

    print("Page Title:", page.title())

    # Check Title
    h1 = page.query_selector('h1')
    if h1:
        print("H1 Text:", h1.inner_text())
        print("H1 Classes:", h1.get_attribute('class'))
    else:
        print("H1 NOT FOUND")

    # Check Likes
    like_candidates = [
        '.o-noteAction__item .o-noteAction__count',
        'button[aria-label^="スキ"]',
        '.o-noteLike__count',
        '.p-article__statusLike',
        '[data-name="like-count"]'
    ]
    for sel in like_candidates:
        el = page.query_selector(sel)
        if el:
            print(f"Like Selector '{sel}' Found.")
            print(f"  Inner Text: '{el.inner_text()}'")
            print(f"  Aria Label: '{el.get_attribute('aria-label')}'")
        else:
             print(f"Like Selector '{sel}' NOT FOUND")

    # Check Tags
    tag_candidates = [
        'a[href^="/hashtag/"]',
        '.m-tagList__item a',
        '.o-noteContentText__tag a'
    ]
    for sel in tag_candidates:
        els = page.query_selector_all(sel)
        if els:
            print(f"Tag Selector '{sel}' Found {len(els)} items. First: {els[0].inner_text()}")
        else:
            print(f"Tag Selector '{sel}' NOT FOUND")

    # Check Paid
    if "購入して" in page.content():
        print("Paid content indicator found in HTML")

    browser.close()
