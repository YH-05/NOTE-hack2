---
name: note-scraper
description: Execute note.com scraping tasks for collecting articles by creator or hashtag. Use when user wants to scrape note.com, collect articles, gather data from creators, or search by tags. Handles scraping execution, parameter setup, and data validation.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__playwright__*, mcp__filesystem__*, mcp__git__*, mcp__time__*
---

# Note Scraper Skill

note.comから記事データを収集するためのスクレイピング実行支援スキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- ユーザーがnote.comからデータを収集したい時
- 特定のクリエイターの記事を取得したい時
- ハッシュタグで記事を検索・収集したい時
- スクレイピングの実行やパラメータ設定が必要な時

## Instructions

### 1. 要件の確認
ユーザーの要求から以下を確認:
- **収集対象**: クリエイターID or ハッシュタグ
- **期間指定**: since日付（YYYY-MM-DD形式）
- **スキ数フィルタ**: 最小スキ数
- **実行モード**: headless（デフォルト）or ブラウザ表示

### 2. スクレイパーの実行

#### 従来のPythonスクリプトを使用
```bash
python src/note_scraper.py --creator {creator_id}
python src/note_scraper.py --tag {tag_name} [--since YYYY-MM-DD] [--min-likes N]
python src/note_scraper.py --tag {tag_name} --no-headless  # デバッグモード
```

#### MCP Playwrightツールを使用（推奨）
MCPのPlaywrightツールを使って直接スクレイピングを実行できます:

1. **ブラウザ起動とナビゲーション**
```
mcp__playwright__playwright_navigate を使用してnote.comページにアクセス
- browserType: "chromium"
- headless: true/false
- url: "https://note.com/hashtag/タグ名"
```

2. **スクリーンショット取得**（デバッグ用）
```
mcp__playwright__playwright_screenshot でページの状態を確認
```

3. **コンテンツ抽出**
```
mcp__playwright__playwright_get_visible_html または
mcp__playwright__playwright_get_visible_text で記事データを取得
```

4. **データ保存**
```
mcp__filesystem__write_file でJSONファイルに保存
- path: "data/raw/articles_tag_xxx_timestamp.json"
- content: JSON形式の記事データ
```

### 3. 実行後の確認
- 生成されたJSONファイルを確認
- 収集記事数をレポート
- エラーがあれば内容を報告

### 4. データ検証
収集されたJSONデータの構造を確認:
- 必須フィールドの存在確認（url, title, date, likes, tags, content）
- データ型の検証
- 欠損値のチェック

## Best Practices

### パラメータ設定
- **since日付**: 過去1ヶ月程度が推奨（あまり遡りすぎると時間がかかる）
- **min-likes**: 人気記事のみ収集したい場合は10以上を推奨
- **headlessモード**: 本番実行時は必ずheadless（デフォルト）を使用

### エラー対応
- ネットワークエラー: リトライを提案
- セレクタエラー: debug_selectors.pyでの確認を提案
- タイムアウト: 対象を絞る、または分割実行を提案

### データ管理
- JSONファイルは`data/raw/`ディレクトリに移動を推奨
- ファイル名から収集条件が分かるようにする
- 大量データは分割収集を検討

#### MCPツールを使用したデータ管理
- **ファイル操作**: `mcp__filesystem__write_file`, `mcp__filesystem__read_text_file`
- **ディレクトリ作成**: `mcp__filesystem__create_directory` で data/raw/ を作成
- **Gitバージョン管理**:
  - `mcp__git__git_status` で変更確認
  - `mcp__git__git_add` でファイルをステージング
  - `mcp__git__git_commit` でコミット（収集条件をコミットメッセージに記載）
- **タイムスタンプ**: `mcp__time__get_current_time` で正確なタイムスタンプを取得

## Common Use Cases

### Case 1: 競合クリエイターの記事収集
```bash
python src/note_scraper.py --creator competitor_id
```
→ 特定クリエイターの全記事を収集

### Case 2: トレンドハッシュタグの人気記事収集
```bash
python src/note_scraper.py --tag "ビジネス" --since 2024-01-01 --min-likes 50
```
→ 2024年以降のスキ50以上の記事のみ収集

### Case 3: 最新記事のみ収集
```bash
python src/note_scraper.py --tag "Python" --since 2024-12-01
```
→ 直近1ヶ月の記事を収集

## Validation Checklist

実行後に以下を確認:
- [ ] JSONファイルが正常に生成されている
- [ ] 収集記事数が妥当である（0件の場合は条件を見直す）
- [ ] 各記事データに必須フィールドが含まれている
- [ ] タイトルと本文が正しく取得できている
- [ ] スキ数とタグ情報が取得できている

## Output Format

スクレイピング結果のJSONフォーマット:
```json
[
  {
    "url": "https://note.com/creator/n/...",
    "title": "記事タイトル",
    "date": "2024-01-01T00:00:00+09:00",
    "likes": 123,
    "tags": ["タグ1", "タグ2"],
    "is_paid": false,
    "content": "記事本文..."
  }
]
```

## Troubleshooting

### 収集件数が0件
- ハッシュタグ名が正しいか確認（#は不要）
- since日付が新しすぎないか確認
- min-likesが高すぎないか確認

### セレクタエラー
```bash
python src/debug_selectors.py
```
→ セレクタの動作確認

### タグページ構造確認
```bash
python src/debug_tag_list.py
```
→ タグページのHTML構造を確認
