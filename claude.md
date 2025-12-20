# NOTE-hack2 開発ガイドライン

## プロジェクト概要

note.comの記事をスクレイピングし、以下の分析を行うプロジェクト:
- テキスト取得と記事データの収集
- 競合クリエイターのスキ（いいね）数の集計
- 人気記事の文章傾向の解析

### 主な技術スタック
- Python 3.x
- Playwright (ブラウザ自動化/スクレイピング)
- JSON (データ保存形式)

## プロジェクト構造

```
NOTE-hack2/
├── src/                    # ソースコード
│   ├── note_scraper.py    # メインスクレイパー
│   ├── debug_*.py         # デバッグ用スクリプト
│   └── analysis/          # 今後追加: データ解析モジュール
├── data/                  # 今後追加: スクレイピングデータ保存先
│   ├── raw/              # 生データ (JSON)
│   └── processed/        # 加工済みデータ
├── notebooks/            # 今後追加: Jupyter Notebook (データ解析用)
├── tests/                # 今後追加: テストコード
├── requirements.txt      # 依存パッケージ
└── README.md            # プロジェクト説明
```

## コーディング規約

### 基本原則
1. **PEP 8準拠**: Pythonの標準コーディング規約に従う
2. **明確な命名**: 関数名、変数名は英語で、その役割が明確にわかるようにする
3. **コメントは日本語可**: 複雑なロジックには日本語でコメントを記載してもよい
4. **エラーハンドリング**: スクレイピングは失敗する可能性があるため、適切にtry-exceptを使用

### コードスタイル
- インデント: スペース4つ
- 1行の最大文字数: 100文字程度
- クラス名: PascalCase (例: `NoteScraper`)
- 関数名・変数名: snake_case (例: `scrape_article_details`)
- 定数: UPPER_SNAKE_CASE (例: `MAX_SCROLLS`)

### 関数・メソッド設計
- 1つの関数は1つの責務を持つ
- 複雑な処理は小さい関数に分割する
- docstringで関数の目的、引数、戻り値を明記する

```python
def scrape_article_details(self, url):
    """
    記事の詳細情報を取得する

    Args:
        url (str): 記事のURL

    Returns:
        dict: 記事情報 (title, date, likes, tags, content等)
              取得失敗時はNone
    """
```

## スクレイピングのベストプラクティス

### 1. 負荷への配慮
- リクエスト間に適切な待機時間を設ける (`time.sleep()`, `page.wait_for_timeout()`)
- 並列処理は慎重に検討し、サーバーに過度な負荷をかけない
- 可能な限りヘッドレスモードで実行（`headless=True`）

### 2. エラー処理
- ネットワークエラー、要素取得失敗を想定
- 失敗した記事はスキップし、ログに記録
- 部分的な失敗でも収集できたデータは保存

### 3. セレクタの保守性
- CSSセレクタが変更される可能性を考慮
- 複数の候補セレクタをフォールバックとして用意
- セレクタの動作確認用デバッグスクリプトを活用

### 4. データの一貫性
- スクレイピング結果は必ず同じ構造のdictで返す
- 取得できなかったフィールドは空文字列や0、空リストなど明確なデフォルト値を設定

## データ管理

### データ保存形式
- **生データ**: JSON形式で保存
- **ファイル命名**: `articles_{creator/tag}_{timestamp}.json`
- **文字エンコーディング**: UTF-8 (`ensure_ascii=False`)

### データフィールド仕様
各記事データは以下のフィールドを持つ:
```python
{
    "url": str,          # 記事URL
    "title": str,        # タイトル
    "date": str,         # 公開日時 (ISO 8601形式)
    "likes": int,        # スキ数
    "tags": list[str],   # タグリスト
    "is_paid": bool,     # 有料記事フラグ
    "content": str       # 記事本文
}
```

## 開発ワークフロー

### 1. 機能開発
1. 新機能は`src/`配下に適切なモジュールとして作成
2. 既存の`NoteScraper`クラスを拡張するか、新しいクラスを作成
3. デバッグスクリプトで動作確認してから本体に統合

### 2. データ解析
1. 収集したデータは`data/raw/`に保存
2. 解析スクリプトは`src/analysis/`に配置
3. 可視化やレポート生成は`notebooks/`でJupyter Notebookを使用

### 3. テスト
- 重要な機能には単体テストを追加（`tests/`配下）
- スクレイピング対象サイトへの実際のアクセスを伴うテストは慎重に実施

## 今後の開発予定機能

### Phase 1: データ収集の強化
- [ ] 複数クリエイターの一括収集機能
- [ ] 収集データのCSV/Excelエクスポート機能
- [ ] 収集進捗の可視化

### Phase 2: データ解析
- [ ] スキ数の統計分析（平均、中央値、分布）
- [ ] タグ別のトレンド分析
- [ ] 記事本文の自然言語処理
  - 文字数、単語数の集計
  - 見出し構造の分析
  - キーワード抽出

### Phase 3: レポーティング
- [ ] 競合クリエイター分析レポート自動生成
- [ ] 人気記事の特徴抽出
- [ ] 可視化ダッシュボード

## 注意事項

### 法的・倫理的配慮
- note.comの利用規約を遵守
- スクレイピングはあくまで分析目的に限定
- 収集データの再配布や商用利用には注意
- robots.txtの確認（ただしJavaScriptレンダリング必要なため参考程度）

### パフォーマンス
- 大量データ収集時はメモリ使用量に注意
- 長時間実行する場合は途中保存を実装
- Playwrightのコンテキスト/ページは適切にクローズ

### セキュリティ
- 認証情報が必要な場合は環境変数で管理
- APIキーなどはコードに直接記述しない（`.env`ファイルを使用）
- `.gitignore`にデータファイルや認証情報を含むファイルを追加

## 便利なコマンド

### 環境セットアップ
```bash
pip install -r requirements.txt
playwright install chromium
```

### スクレイピング実行
```bash
# クリエイター別
python src/note_scraper.py --creator {creator_id}

# タグ別（新着順、日付・スキ数フィルタ付き）
python src/note_scraper.py --tag {tag_name} --since 2024-01-01 --min-likes 10

# ブラウザ表示モード（デバッグ用）
python src/note_scraper.py --tag {tag_name} --no-headless
```

### デバッグ
```bash
# セレクタ確認
python src/debug_selectors.py

# タグページ構造確認
python src/debug_tag_list.py
```

## 参考リソース
- [Playwright公式ドキュメント](https://playwright.dev/python/)
- [note.com](https://note.com/)
- [PEP 8 日本語版](https://pep8-ja.readthedocs.io/)
- Add to memory. タスク開始時にはtimeで現在時刻を確認してから始めること。