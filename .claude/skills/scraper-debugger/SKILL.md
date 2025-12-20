---
name: scraper-debugger
description: Debug and troubleshoot note.com scraping issues including selector problems, network errors, and data extraction failures. Use when scraping fails, selectors don't work, or data is not extracted correctly.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__playwright__*, mcp__filesystem__*, mcp__sequential-thinking__*
---

# Scraper Debugger Skill

note.comスクレイピングのデバッグとトラブルシューティングを支援するスキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- スクレイピングが失敗する時
- セレクタが機能しない時
- データが正しく取得できない時
- エラーメッセージの解析が必要な時
- スクレイピング結果の検証が必要な時
- パフォーマンス問題の診断時

## Instructions

### 1. 問題の特定

#### MCP Sequential Thinkingツールを使用
複雑なデバッグ問題には `mcp__sequential-thinking__sequentialthinking` を活用:
- 段階的に問題を切り分け
- 複数の原因候補を検証
- 解決策を論理的に導出

**問題のカテゴリー**:
- **収集件数が0**: セレクタ、URL、フィルタ条件の問題
- **データ欠損**: 特定フィールドのセレクタ問題
- **エラー発生**: ネットワーク、タイムアウト、構文エラー
- **パフォーマンス**: 遅い、メモリ不足

### 2. デバッグツールの実行

#### MCP Playwrightツールを使用（推奨）
直接ブラウザでデバッグ:
```
mcp__playwright__playwright_navigate でnote.comページにアクセス
- url: "https://note.com/問題のURL"
- headless: false  # デバッグモード
- browserType: "chromium"

mcp__playwright__playwright_screenshot でスクリーンショット取得
- name: "debug_page"
- savePng: true
- downloadsDir: "debug/screenshots"

mcp__playwright__playwright_get_visible_html でHTML構造を確認
- selector: ".m-tagList__item"  # 問題のセレクタ
- removeScripts: true

mcp__playwright__playwright_console_logs でコンソールログを確認
- type: "error"
```

#### 従来のPythonデバッグスクリプト
```bash
python src/debug_selectors.py  # セレクタの検証
python src/debug_tag_list.py   # タグページ構造の確認
```

### 3. 段階的なデバッグ

#### MCP Playwrightでインタラクティブにデバッグ
```
# 1. ページに移動
mcp__playwright__playwright_navigate

# 2. 要素の存在確認
mcp__playwright__playwright_get_visible_text

# 3. クリックやフォーム入力をテスト
mcp__playwright__playwright_click

# 4. エラーログを確認
mcp__playwright__playwright_console_logs
```

#### Level 1: ブラウザ表示モードで実行（従来の方法）
```bash
python src/note_scraper.py --tag test --no-headless
```
ブラウザを表示して動作を目視確認

#### Level 2: ログ出力の追加
```python
# スクレイパーにログを追加
print(f"DEBUG: Found {len(elements)} elements")
print(f"DEBUG: Element text: {element.inner_text()}")
```

#### Level 3: 個別要素の確認
```python
# 特定の要素をインタラクティブに調査
element = page.query_selector('.m-tagList__item a')
if element:
    print(f"Found: {element.inner_text()}")
    print(f"HTML: {element.inner_html()}")
else:
    print("NOT FOUND")
```

### 4. よくある問題のチェックリスト
- [ ] セレクタが最新のHTML構造に対応しているか
- [ ] wait_for_load_state()で十分に待機しているか
- [ ] JavaScriptレンダリングが完了しているか
- [ ] ネットワーク接続が安定しているか
- [ ] note.comの仕様変更がないか

### 5. 修正と検証
- 問題を特定したら修正
- 小規模テストで検証
- 本番データで再実行

## Common Issues and Solutions

### Issue 1: 収集件数が0件

**原因の可能性**:
1. タグ名が間違っている
2. セレクタがnote.comの変更により無効
3. since日付が新しすぎる
4. min-likesが高すぎる

**デバッグ手順**:
```bash
# 1. ブラウザ表示モードで確認
python src/note_scraper.py --tag python --no-headless

# 2. デバッグスクリプトで構造確認
python src/debug_tag_list.py

# 3. フィルタ条件を緩和
python src/note_scraper.py --tag python --min-likes 0
```

**解決策**:
- タグ名の確認（#不要、スペース→ハイフン）
- セレクタの更新
- フィルタ条件の調整

### Issue 2: タイトルや本文が取得できない

**原因の可能性**:
1. セレクタが古い
2. 記事タイプが想定外（有料記事など）
3. 待機時間不足

**デバッグ手順**:
```bash
# 特定のURLでセレクタ確認
python src/debug_selectors.py
# → debug_selectors.py内のURLを問題の記事URLに変更
```

**解決策**:
```python
# フォールバック セレクタを追加
title = None
for selector in [
    'meta[property="og:title"]',
    'h1',
    'title'
]:
    element = page.query_selector(selector)
    if element:
        title = extract_title(element)
        break
```

### Issue 3: スキ数が0になる

**原因の可能性**:
1. like buttonのセレクタ変更
2. aria-labelの形式変更
3. スキが本当に0

**デバッグ手順**:
```python
# デバッグコードを追加
like_btn = page.query_selector('button[aria-label^="スキ"]')
if like_btn:
    print(f"DEBUG aria-label: {like_btn.get_attribute('aria-label')}")
    print(f"DEBUG inner_text: {like_btn.inner_text()}")
else:
    print("DEBUG: Like button not found")
    # 代替セレクタを試す
    for sel in LIKE_SELECTORS:
        el = page.query_selector(sel)
        if el:
            print(f"DEBUG: Found with {sel}")
```

**解決策**:
- セレクタを最新のHTML構造に合わせる
- 複数のフォールバックセレクタを用意

### Issue 4: タグが取得できない

**原因の可能性**:
1. タグリストのセレクタ変更
2. タグが存在しない記事
3. JavaScriptロード遅延

**デバッグ手順**:
```python
# タグ要素の詳細確認
tag_elements = page.query_selector_all('.m-tagList__item a')
print(f"DEBUG: Found {len(tag_elements)} tag elements")
for i, tag_el in enumerate(tag_elements[:3]):
    print(f"DEBUG Tag {i}: {tag_el.inner_text()}")
    print(f"DEBUG Tag {i} href: {tag_el.get_attribute('href')}")
```

**解決策**:
```python
# 待機時間を追加
page.wait_for_selector('.m-tagList__item a', timeout=5000)

# または代替セレクタ
tags = []
for selector in [
    '.m-tagList__item a',
    'a[href^="/hashtag/"]',
    '.o-noteContentText__tag a'
]:
    elements = page.query_selector_all(selector)
    if elements:
        tags = [el.inner_text().strip().replace('#', '') for el in elements]
        break
```

### Issue 5: タイムアウトエラー

**原因の可能性**:
1. ネットワーク遅延
2. 重いページ
3. 待機時間の設定ミス

**解決策**:
```python
# タイムアウトを延長
page.goto(url, timeout=60000)  # 60秒

# または、状態を明示的に待つ
page.wait_for_load_state("networkidle", timeout=30000)
```

### Issue 6: 記事URLが重複取得される

**原因の可能性**:
1. スクロールで同じ要素が再表示
2. URL正規化の不足

**解決策**:
```python
# URLの正規化とセット管理
def normalize_url(url):
    """URLを正規化（クエリパラメータ除去など）"""
    return url.split('?')[0].split('#')[0]

processed_urls = set()
for link in links:
    url = normalize_url(link.get_attribute('href'))
    if url not in processed_urls:
        processed_urls.add(url)
        # 処理
```

## Debug Script Templates

### Template 1: Selector Tester
```python
#!/usr/bin/env python3
"""
特定のセレクタをテストするスクリプト
"""
from playwright.sync_api import sync_playwright
import sys

def test_selector(url, selector):
    """セレクタが機能するかテスト"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        elements = page.query_selector_all(selector)
        print(f"✅ Found {len(elements)} elements with selector: {selector}")

        for i, el in enumerate(elements[:5]):  # 最初の5つのみ
            print(f"\n--- Element {i} ---")
            print(f"Text: {el.inner_text()[:100]}")
            print(f"HTML: {el.inner_html()[:200]}")

        browser.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python test_selector.py <URL> <SELECTOR>")
        print('Example: python test_selector.py "https://note.com/..." ".m-tagList__item a"')
        sys.exit(1)

    test_selector(sys.argv[1], sys.argv[2])
```

### Template 2: Network Monitor
```python
#!/usr/bin/env python3
"""
ネットワークリクエストをモニタリング
"""
from playwright.sync_api import sync_playwright

def monitor_network(url):
    """ネットワークリクエストを監視"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # リクエストをログ
        page.on("request", lambda request: print(f"→ {request.method} {request.url}"))
        page.on("response", lambda response: print(f"← {response.status} {response.url}"))

        page.goto(url)
        page.wait_for_load_state("networkidle")

        print("\n✅ Network monitoring complete")
        browser.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python monitor_network.py <URL>")
        sys.exit(1)

    monitor_network(sys.argv[1])
```

### Template 3: Data Validator
```python
#!/usr/bin/env python3
"""
スクレイピング結果を検証
"""
import json
import sys

def validate_data(json_file):
    """データの整合性を検証"""
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Total articles: {len(articles)}")

    issues = []

    for i, article in enumerate(articles):
        # 必須フィールドチェック
        required = ['url', 'title', 'date', 'likes', 'tags', 'is_paid', 'content']
        for field in required:
            if field not in article:
                issues.append(f"Article {i}: Missing field '{field}'")

        # データ型チェック
        if not isinstance(article.get('likes', 0), int):
            issues.append(f"Article {i}: 'likes' is not int")

        if not isinstance(article.get('tags', []), list):
            issues.append(f"Article {i}: 'tags' is not list")

        # 値の妥当性チェック
        if article.get('title', '') == '':
            issues.append(f"Article {i}: Empty title")

        if len(article.get('content', '')) < 10:
            issues.append(f"Article {i}: Content too short ({len(article.get('content', ''))} chars)")

    if issues:
        print(f"\n⚠️  Found {len(issues)} issues:")
        for issue in issues[:10]:  # 最初の10個のみ表示
            print(f"  - {issue}")
    else:
        print("\n✅ All data valid!")

    return len(issues) == 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <data.json>")
        sys.exit(1)

    is_valid = validate_data(sys.argv[1])
    sys.exit(0 if is_valid else 1)
```

## Debugging Workflow

### Step 1: Reproduce the Issue
```bash
# 問題を再現
python src/note_scraper.py --tag test_tag --no-headless
```

### Step 2: Isolate the Problem
```bash
# 特定のURLで問題を分離
python src/debug_selectors.py  # URLを編集
```

### Step 3: Test Solutions
```python
# 修正案をテスト
# note_scraper.pyの該当箇所を編集

# 小規模テスト
python src/note_scraper.py --tag test --no-headless
```

### Step 4: Validate Fix
```bash
# 本番データで検証
python src/note_scraper.py --tag python --min-likes 10

# データ検証
python scripts/validate_data.py articles_*.json
```

## Best Practices

### プロアクティブなデバッグ
- スクレイピング後は必ずデータ検証
- 定期的にセレクタの動作確認
- エラーログを保存・分析

### ロバストなコード
- 複数のフォールバックセレクタ
- 適切なエラーハンドリング
- タイムアウトの設定

### バージョン管理
- セレクタの変更履歴を記録
- note.comの仕様変更をメモ
- 動作確認した日付を記録

### テスト環境
- 小規模データでまずテスト
- headlessとnon-headlessの両方で確認
- 異なるタグ/クリエイターで検証

## Selector Update Guide

note.comの構造が変更された場合のセレクタ更新手順:

### 1. Chrome DevToolsで調査
1. note.comの該当ページを開く
2. F12でDevToolsを開く
3. 要素を右クリック→検証
4. HTML構造とクラス名を確認

### 2. セレクタの候補を特定
```javascript
// Consoleで試す
document.querySelectorAll('.m-tagList__item a')
```

### 3. debug_selectors.pyで検証
```python
# URLを問題の記事URLに変更
url = "https://note.com/xxx/n/yyy"

# 新しいセレクタを試す
tag_elements = page.query_selector_all('.new-selector')
```

### 4. note_scraper.pyを更新
```python
# 古いセレクタ
# tag_elements = page.query_selector_all('.m-tagList__item a')

# 新しいセレクタ
tag_elements = page.query_selector_all('.new-selector')
```

### 5. テストと検証
```bash
python src/note_scraper.py --tag test --no-headless
```

## Error Messages Guide

### Playwright Errors

#### "TimeoutError: Timeout 30000ms exceeded"
**原因**: ページロードまたは要素の出現待機がタイムアウト
**解決**: タイムアウト延長、または`wait_for_load_state`の調整

#### "Error: Target page, context or browser has been closed"
**原因**: ページ/ブラウザが予期せず閉じられた
**解決**: try-finally で適切にクローズ、またはエラーハンドリング追加

#### "Error: Selector does not match any elements"
**原因**: セレクタが見つからない
**解決**: セレクタの確認、待機時間追加、フォールバック実装

### Python Errors

#### "JSONDecodeError"
**原因**: 不正なJSON形式
**解決**: JSONファイルの構文確認、ensure_ascii=False使用

#### "UnicodeDecodeError"
**原因**: 文字エンコーディングの不一致
**解決**: `encoding='utf-8'`を明示

#### "KeyError"
**原因**: 存在しないキーへのアクセス
**解決**: `.get()`メソッド使用、デフォルト値設定

## Monitoring and Logging

### ログレベルの追加
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def scrape_article_details(self, url):
    logger.info(f"Scraping: {url}")
    try:
        # ...処理
        logger.debug(f"Title: {title}")
        logger.debug(f"Likes: {likes}")
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
```

### 進捗モニタリング
```python
from tqdm import tqdm

for url in tqdm(article_urls, desc="Scraping articles"):
    data = self.scrape_article_details(url)
```

## Validation Checklist

デバッグ完了時の確認:
- [ ] 問題が特定され、原因が明確
- [ ] 修正が適用され、テスト済み
- [ ] 小規模データで検証成功
- [ ] 本番データで検証成功
- [ ] エラーログがクリーン
- [ ] パフォーマンスが許容範囲
- [ ] ドキュメント更新（セレクタ変更など）

## Troubleshooting Resources

### 公式ドキュメント
- [Playwright Python](https://playwright.dev/python/)
- [CSS Selectors Reference](https://www.w3.org/TR/selectors/)

### 内部ツール
- `src/debug_selectors.py`: セレクタ動作確認
- `src/debug_tag_list.py`: タグページ構造確認

### 外部ツール
- Chrome DevTools: HTML/CSS調査
- Browser console: JavaScriptでセレクタテスト
- Network tab: リクエスト/レスポンス確認
