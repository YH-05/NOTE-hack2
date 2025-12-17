import json
import time
import argparse
from datetime import datetime
from playwright.sync_api import sync_playwright

class NoteScraper:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def _auto_scroll(self, page):
        """Scrolls down the page to load identifying elements."""
        prev_height = -1
        max_scrolls = 100
        scroll_count = 0

        while scroll_count < max_scrolls:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)  # Wait for loading
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height
            scroll_count += 1

    def scrape_article_details(self, url):
        print(f"Scraping detailed info from: {url}")
        new_page = self.context.new_page()
        try:
            new_page.goto(url)
            new_page.wait_for_load_state("domcontentloaded")

            # Extract basic data
            # Extract basic data
            title = new_page.title()
            try:
                # Try to get from meta tag first (more reliable)
                meta_title = new_page.query_selector('meta[property="og:title"]')
                if meta_title:
                    title = meta_title.get_attribute('content')
                    # Remove "｜note" or author suffix if present
                    if '｜' in title:
                        title = title.split('｜')[0]
                else:
                    # Fallback to h1 or page title cleaning
                    h1 = new_page.query_selector('h1')
                    if h1 and h1.inner_text().strip():
                        title = h1.inner_text().strip()
                    elif '｜' in title:
                            title = title.split('｜')[0]
            except:
                pass

            # Content
            content = ""
            try:
                article_body = new_page.query_selector('.p-article__content') or new_page.query_selector('#main-article-content') or new_page.query_selector('article')
                if article_body:
                    content = article_body.inner_text()
            except:
                pass

            # Date
            publish_date = ""
            try:
                # Look for time element or meta tags
                time_el = new_page.query_selector('time')
                if time_el:
                    publish_date = time_el.get_attribute('datetime')
            except:
                pass

            # Likes
            likes = 0
            try:
                # Try to get from aria-label of the like button
                like_btn = new_page.query_selector('button[aria-label^="スキ"]')
                if like_btn:
                    aria_label = like_btn.get_attribute('aria-label')
                    # Format usually "スキ 10" or just "スキ" if 0?
                    # Extract digits
                    import re
                    match = re.search(r'\d+', aria_label)
                    if match:
                        likes = int(match.group())
                    else:
                        # Sometimes text exists inside hidden span
                        txt = like_btn.inner_text().strip()
                        if txt.isdigit():
                            likes = int(txt)
            except:
                pass

            # Tags
            tags = []
            try:
                # Verified selector
                tag_elements = new_page.query_selector_all('.m-tagList__item a')
                for tag_el in tag_elements:
                    tag_text = tag_el.inner_text().strip().replace('#', '')
                    if tag_text and tag_text not in tags:
                        tags.append(tag_text)
            except:
                pass

            # Paid Status
            is_paid = False
            try:
                # Check for indicators like "Purchased" or specific paywall classes
                # Providing a generic check for now
                if "購入して" in new_page.content() or new_page.query_selector('.p-paywall'):
                     is_paid = True
            except:
                pass

            return {
                "url": url,
                "title": title,
                "date": publish_date,
                "likes": likes,
                "tags": tags,
                "is_paid": is_paid,
                "content": content
            }

        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None
        finally:
            new_page.close()

    def get_articles_by_creator(self, creator_id):
        url = f"https://note.com/{creator_id}/all"
        print(f"Navigating to creator page: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

        self._auto_scroll(self.page)

        # Collect article URLs
        # Note list items usually in .m-noteItem or similar
        # We'll grab all links that look like article links under this creator domain
        article_links = set()

        # Specific selector for creator's article list (often in a feed)
        # We can find all 'a' tags that match the pattern /{creator_id}/n/{note_id}
        links = self.page.query_selector_all(f'a[href^="https://note.com/{creator_id}/n/"]')
        for link in links:
            href = link.get_attribute('href')
            # remove query params/hash for unicity
            href = href.split('?')[0].split('#')[0]
            article_links.add(href)

        print(f"Found {len(article_links)} articles.")

        results = []
        for link in article_links:
            data = self.scrape_article_details(link)
            if data:
                results.append(data)

        return results

    def get_articles_by_tag(self, tag, since_date=None, min_likes=0):
        # Sort by New
        target_url = f"https://note.com/hashtag/{tag}?f=new"
        print(f"Navigating to tag page: {target_url}")
        self.page.goto(target_url)
        self.page.wait_for_load_state("domcontentloaded")

        articles_data = []
        processed_urls = set()
        stop_scraping = False

        since_dt = None
        if since_date:
            try:
                since_dt = datetime.strptime(since_date, "%Y-%m-%d")
            except ValueError:
                print(f"Invalid since_date format: {since_date}")

        while not stop_scraping:
            # Verified selector for list items
            elements = self.page.query_selector_all('.m-largeNoteWrapper__link')
            if not elements:
                elements = self.page.query_selector_all('.o-noteItem__link')

            batch_urls = []
            for el in elements:
                u = el.get_attribute('href')
                if u:
                    if u.startswith('/'):
                        u = f"https://note.com{u}"

                    if u not in processed_urls:
                        batch_urls.append(u)
                        processed_urls.add(u)

            if not batch_urls:
                if not self._auto_scroll_step():
                    print("No more articles found.")
                    break
                continue

            print(f"Processing {len(batch_urls)} new articles...")

            for url in batch_urls:
                details = self.scrape_article_details(url)
                if not details:
                    continue

                # Check Date
                if since_dt and details.get('date'):
                    try:
                        # Parse simplified date portion
                        d_str = details['date'].split('T')[0]
                        d_dt = datetime.strptime(d_str, "%Y-%m-%d")
                        if d_dt < since_dt:
                            print(f"Article date {d_str} is older than {since_date}. Stopping.")
                            stop_scraping = True
                            break
                    except:
                        pass

                # Check Likes
                if details.get('likes', 0) < min_likes:
                    continue

                articles_data.append(details)
                print(f"Collected: {details.get('title')[:20]}... (Date: {details.get('date')}, Likes: {details.get('likes')})")

            if stop_scraping:
                break

            if not self._auto_scroll_step():
                break

        return articles_data

    def _auto_scroll_step(self):
        prev = self.page.evaluate("document.body.scrollHeight")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(2000)
        curr = self.page.evaluate("document.body.scrollHeight")
        return curr > prev

def main():
    parser = argparse.ArgumentParser(description="Scrape note.com articles.")
    parser.add_argument("--creator", type=str, help="Creator ID to scrape (e.g. 'user_id')")
    parser.add_argument("--tag", type=str, help="Tag to scrape (without #)")
    parser.add_argument("--since", type=str, help="Start date (YYYY-MM-DD) for tag search")
    parser.add_argument("--min-likes", type=int, default=0, help="Minimum likes for tag search")
    parser.add_argument("--headless", action='store_true', default=True, help="Run headless")
    parser.add_argument("--no-headless", action='store_false', dest='headless', help="Run with browser visible")

    args = parser.parse_args()

    scraper = NoteScraper(headless=args.headless)
    results = []

    try:
        if args.creator:
            results = scraper.get_articles_by_creator(args.creator)
        elif args.tag:
            results = scraper.get_articles_by_tag(args.tag, args.since, args.min_likes)
        else:
            print("Please specify --creator or --tag")
            return

        # Save results
        filename = f"articles_{args.creator or args.tag}_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(results)} articles to {filename}")

    finally:
        scraper.close()

if __name__ == "__main__":
    main()
