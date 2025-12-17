from playwright.sync_api import sync_playwright

url = "https://note.com/hashtag/python?f=new"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000) # Wait for content

    # Try to find list items with BEM-inferred class
    articles = page.query_selector_all('.m-largeNoteWrapper')
    if not articles:
        # Fallback to generic card
        articles = page.query_selector_all('.o-card')

    print(f"Found {len(articles)} articles")

    for i, art in enumerate(articles[:5]):
        print(f"--- Article {i} ---")
        # print("HTML snippet:", art.inner_html()[:200]) # truncated

        # Title
        title_el = art.query_selector('.m-largeNoteWrapper__link')
        if title_el:
             print("Title link:", title_el.get_attribute('href'))

        # Check for time
        time_el = art.query_selector('time')
        if time_el:
            print("Time Attr:", time_el.get_attribute('datetime'))
        else:
            print("Time: NOT FOUND")

        # Check for likes
        like_el = art.query_selector('.o-noteLikeV3__iconButton') or art.query_selector('button[aria-label*="スキ"]')
        if like_el:
             print("Like Label:", like_el.get_attribute('aria-label'))
        else:
             print("Like: NOT FOUND")

    browser.close()
