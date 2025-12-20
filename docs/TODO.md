# NOTE-hack2 開発 TODO

## 概要

このドキュメントは、NOTE-hack2 プロジェクトの未実装機能と改善タスクをまとめたものです。優先順位に基づいて整理されています。

最終更新: 2024-12-20

---

## 優先度: 🔴 高（すぐに実装すべき）

### 1. プロジェクト構造の整備

#### 1.1 ディレクトリ構造の作成

-   [ ] `data/` ディレクトリを作成
    -   [ ] `data/raw/` - スクレイピングした生データ
    -   [ ] `data/processed/` - 加工済みデータ
    -   [ ] `data/exports/` - エクスポート結果（CSV、Excel 等）
-   [ ] `notebooks/` ディレクトリを作成（Jupyter Notebook 用）
-   [ ] `tests/` ディレクトリを作成（テストコード用）
-   [ ] `src/analysis/` ディレクトリを作成（データ解析モジュール用）
-   [ ] `reports/` ディレクトリを作成（生成されたレポート用）
-   [ ] `research/` ディレクトリを作成（content-researcher スキル用）

#### 1.2 設定ファイルの更新

**requirements.txt の拡充:**

```
playwright
pandas>=2.0.0
openpyxl>=3.1.0
matplotlib>=3.7.0
seaborn>=0.12.0
janome>=0.5.0
scikit-learn>=1.3.0
jupyter>=1.0.0
pytest>=7.4.0
```

-   [ ] requirements.txt に必要なライブラリを追加
-   [ ] 各ライブラリのバージョン指定

**.gitignore の拡充:**

```
# Environment
.env
.DS_Store
.mcp.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Testing
.pytest_cache/
.coverage
htmlcov/

# Data files
data/raw/*.json
data/processed/*.json
*.csv
*.xlsx

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Exports
exports/

# IDE
.vscode/
.idea/
```

-   [ ] .gitignore に Python 関連ファイルを追加
-   [ ] データファイルの除外設定
-   [ ] キャッシュファイルの除外設定

### 2. ドキュメントの拡充

#### 2.1 README.md の改善

-   [ ] プロジェクト概要の詳細説明
-   [ ] 機能一覧の記載
-   [ ] セットアップ手順の詳細化
    -   [ ] Python 環境のセットアップ
    -   [ ] 依存パッケージのインストール
    -   [ ] Playwright のインストール（`playwright install chromium`）
-   [ ] 使い方の例（コマンド例）
-   [ ] ディレクトリ構造の説明
-   [ ] ライセンス情報
-   [ ] 注意事項（note.com 利用規約遵守など）

#### 2.2 その他のドキュメント

-   [ ] `docs/SETUP.md` - 詳細なセットアップガイド
-   [ ] `docs/USAGE.md` - 詳細な使い方ガイド
-   [ ] `docs/API.md` - コード API ドキュメント
-   [ ] `docs/CONTRIBUTING.md` - 貢献ガイドライン（チーム開発の場合）

### 3. データエクスポート機能の実装（Phase 1-1）

#### 3.1 CSV エクスポート

-   [ ] `.claude/skills/data-export/scripts/export_csv.py` を作成
    -   [ ] JSON から CSV への変換
    -   [ ] UTF-8 BOM エンコーディング対応（Excel 互換）
    -   [ ] カスタムフィールド選択機能
    -   [ ] タグのカンマ区切り変換
    -   [ ] コマンドライン引数対応

**実装機能:**

```python
# 基本的なエクスポート
python .claude/skills/data-export/scripts/export_csv.py input.json output.csv

# フィールド選択
python .claude/skills/data-export/scripts/export_csv.py input.json output.csv --fields url,title,date,likes
```

#### 3.2 Excel エクスポート

-   [ ] `.claude/skills/data-export/scripts/export_excel.py` を作成
    -   [ ] JSON から Excel への変換
    -   [ ] 複数シート対応（記事データ、統計、Top 記事、タグ分析）
    -   [ ] 列幅の自動調整
    -   [ ] フィルター機能の有効化
    -   [ ] 日付・数値フォーマットの適用

**シート構成:**

1. Articles - 全記事データ
2. Statistics - 基本統計サマリー
3. Top 20 - 人気記事 Top 20
4. Tag Analysis - タグ別集計

#### 3.3 整形 JSON エクスポート

-   [ ] `.claude/skills/data-export/scripts/export_formatted_json.py` を作成
    -   [ ] インデント付き JSON 出力
    -   [ ] メタデータ追加（収集日時、件数など）
    -   [ ] ensure_ascii=False で日本語そのまま出力

### 4. 基本的なデータ分析機能の実装（Phase 2-1）

#### 4.1 統計分析スクリプト

-   [ ] `.claude/skills/data-analyzer/scripts/analyze_articles.py` を作成
    -   [ ] 基本統計の算出（総記事数、総スキ数、平均、中央値、標準偏差）
    -   [ ] スキ数の分布分析（四分位数、ヒストグラム）
    -   [ ] 有料/無料記事の比率
    -   [ ] 日付別の記事数とスキ数
    -   [ ] Markdown レポート生成

**出力例:**

```markdown
# データ分析レポート

## 基本統計

-   総記事数: 150
-   総スキ数: 5,432
-   平均スキ数: 36.2
-   中央値: 18
-   標準偏差: 42.1

## スキ数分布

-   10 未満: 45 件 (30%)
-   10-50: 68 件 (45%)
-   50-100: 25 件 (17%)
-   100 以上: 12 件 (8%)
```

#### 4.2 タグ分析スクリプト

-   [ ] `.claude/skills/data-analyzer/scripts/tag_analysis.py` を作成
    -   [ ] タグ別記事数の集計
    -   [ ] タグ別平均スキ数
    -   [ ] タグの共起分析（どのタグが一緒に使われるか）
    -   [ ] 人気タグ Top 20
    -   [ ] タグクラウド用データ生成（オプション）

---

## 優先度: 🟡 中（重要だが後回し可）

### 5. 複数クリエイター一括収集機能（Phase 1-2）

#### 5.1 バッチ収集スクリプト

-   [ ] `src/batch_scraper.py` を作成
    -   [ ] 複数クリエイター ID を CSV または JSON で読み込み
    -   [ ] 各クリエイターを順次スクレイピング
    -   [ ] 進捗表示（tqdm など）
    -   [ ] エラー処理（1 件失敗しても続行）
    -   [ ] 結果の個別保存 + 統合 JSON 生成

**設定ファイル例（creators.json）:**

```json
[
    { "id": "creator1", "name": "クリエイター1" },
    { "id": "creator2", "name": "クリエイター2" },
    { "id": "creator3", "name": "クリエイター3" }
]
```

#### 5.2 収集進捗の可視化

-   [ ] 進捗バーの実装（tqdm 使用）
-   [ ] ログファイルの生成
-   [ ] エラー記録とレポート

### 6. 高度なテキスト分析機能（Phase 2-2）

#### 6.1 文字数・単語数の集計

-   [ ] `.claude/skills/article-trend-analysis/scripts/text_analysis.py` を作成
    -   [ ] 総文字数の計算
    -   [ ] 形態素解析による単語数カウント（janome 使用）
    -   [ ] 平均文長の算出
    -   [ ] 段落数のカウント
    -   [ ] 読了時間の推定（文字数/600 で分換算）

#### 6.2 タイトル分析

-   [ ] `.claude/skills/article-trend-analysis/scripts/title_analysis.py` を作成
    -   [ ] タイトル長の分布
    -   [ ] 数字使用頻度（「3 つの方法」など）
    -   [ ] 疑問形/断定形の比率
    -   [ ] 記号・Emoji の使用状況
    -   [ ] タイトルとスキ数の相関分析

#### 6.3 見出し構造の分析

-   [ ] 見出し（#, ##など）の抽出
-   [ ] 見出しの階層構造分析
-   [ ] 見出し数と記事の長さの関係
-   [ ] 見出しパターンの分類

#### 6.4 キーワード抽出

-   [ ] `.claude/skills/article-trend-analysis/scripts/keyword_extraction.py` を作成
    -   [ ] TF-IDF による重要キーワード抽出（scikit-learn 使用）
    -   [ ] 品詞別の頻出語抽出（名詞、動詞、形容詞）
    -   [ ] ストップワード除去
    -   [ ] キーワードランキング生成

### 7. 競合クリエイター分析機能（Phase 3-1）

#### 7.1 比較分析スクリプト

-   [ ] `.claude/skills/competitor-analysis/scripts/compare_creators.py` を作成
    -   [ ] 複数クリエイターのメトリクス比較
    -   [ ] エンゲージメント率の計算
    -   [ ] タグ戦略の比較
    -   [ ] コンテンツ戦略の分析
    -   [ ] ベンチマーク表の生成

#### 7.2 競合レポート自動生成

-   [ ] `.claude/skills/competitor-analysis/templates/report_template.md` を作成
-   [ ] レポート生成スクリプト
    -   [ ] エグゼクティブサマリー
    -   [ ] 定量比較表
    -   [ ] SWOT 分析
    -   [ ] 推奨アクション

**レポート例:**

```markdown
# 競合クリエイター分析レポート

## エグゼクティブサマリー

-   分析期間: 2024-12-01 〜 2024-12-20
-   対象クリエイター: 3 名
-   主要発見: Creator B が最も効率的なエンゲージメント

## 定量比較

| メトリクス | Creator A | Creator B | Creator C |
| ---------- | --------- | --------- | --------- |
| 記事数     | 120       | 85        | 200       |
| 総スキ     | 4,500     | 6,200     | 5,800     |
| 平均スキ   | 37.5      | 72.9      | 29.0      |
```

### 8. データ可視化機能（Phase 3-2）

#### 8.1 基本的なグラフ生成

-   [ ] `src/analysis/visualization.py` を作成
    -   [ ] スキ数分布のヒストグラム（matplotlib）
    -   [ ] タグ別記事数の棒グラフ
    -   [ ] 日付別トレンドの折れ線グラフ
    -   [ ] タグクラウド（wordcloud 使用、オプション）

#### 8.2 Jupyter Notebook サンプル

-   [ ] `notebooks/01_basic_analysis.ipynb` - 基本的なデータ探索
-   [ ] `notebooks/02_tag_analysis.ipynb` - タグ分析
-   [ ] `notebooks/03_trend_analysis.ipynb` - トレンド分析
-   [ ] `notebooks/04_competitor_analysis.ipynb` - 競合分析

### 9. テストコードの実装

#### 9.1 単体テスト

-   [ ] `tests/test_note_scraper.py`

    -   [ ] スクレイパーの初期化テスト
    -   [ ] URL 正規化のテスト
    -   [ ] データ抽出ロジックのテスト（モックページ使用）

-   [ ] `tests/test_data_analysis.py`

    -   [ ] 統計計算のテスト
    -   [ ] タグ集計のテスト
    -   [ ] データ検証のテスト

-   [ ] `tests/test_export.py`
    -   [ ] CSV エクスポートのテスト
    -   [ ] Excel エクスポートのテスト
    -   [ ] データフォーマットのテスト

#### 9.2 統合テスト

-   [ ] `tests/integration/test_scraping_workflow.py`
    -   [ ] スクレイピング → 保存 → 読み込みの一連のフロー
    -   [ ] エラー処理の検証

#### 9.3 テスト設定

-   [ ] `pytest.ini` の作成
-   [ ] テストデータの準備（`tests/fixtures/`）
-   [ ] CI/CD 設定（GitHub Actions など、オプション）

---

## 優先度: 🟢 低（あると良い）

### 10. MCP スキル対応の実装

#### 10.1 content-researcher スキル

-   [ ] リサーチワークフローの整備
-   [ ] リサーチノートテンプレートの作成
-   [ ] Web 検索結果の保存機能
-   [ ] ファクトチェック用スクリプト

#### 10.2 data-versioning スキル

-   [ ] Git ワークフロー自動化スクリプト
-   [ ] データコミット用ヘルパー関数
-   [ ] ブランチ戦略のドキュメント化
-   [ ] タグ付けスクリプト

### 11. 高度な NLP 機能（Phase 2-3）

#### 11.1 感情・トーン分析

-   [ ] ポジティブ/ネガティブワードの辞書作成
-   [ ] 感情スコアの算出
-   [ ] 文体分析（専門的 vs カジュアル）

#### 11.2 トピックモデリング

-   [ ] LDA（Latent Dirichlet Allocation）の実装
-   [ ] 潜在的なトピックの抽出
-   [ ] トピック別の記事分類

#### 11.3 類似記事の検出

-   [ ] TF-IDF ベクトル化
-   [ ] コサイン類似度の計算
-   [ ] 重複記事の検出

### 12. インタラクティブダッシュボード（Phase 3-3）

#### 12.1 Streamlit/Dash ダッシュボード

-   [ ] リアルタイムデータ表示
-   [ ] インタラクティブなフィルタリング
-   [ ] グラフのドリルダウン機能
-   [ ] レポートの PDF エクスポート

**想定ページ:**

1. ホーム: 全体サマリー
2. データ収集: スクレイピング状況
3. 統計分析: メトリクス表示
4. タグ分析: タグ別トレンド
5. 競合分析: クリエイター比較

### 13. 自動化とスケジューリング

#### 13.1 定期実行スクリプト

-   [ ] cron/スケジューラー用のシェルスクリプト
-   [ ] 日次/週次/月次スクレイピング
-   [ ] 自動レポート生成
-   [ ] メール通知機能（オプション）

#### 13.2 エラー監視

-   [ ] ログファイルの監視
-   [ ] エラー通知システム
-   [ ] 自動リトライ機能

### 14. パフォーマンス最適化

#### 14.1 スクレイピング高速化

-   [ ] 並列処理の実装（multiprocessing/asyncio）
-   [ ] ページロード最適化
-   [ ] キャッシュ機能の追加

#### 14.2 データ処理の最適化

-   [ ] 大容量データのチャンク処理
-   [ ] メモリ使用量の削減
-   [ ] データベース導入の検討（SQLite/PostgreSQL）

---

## 技術的負債・改善項目

### コード品質

-   [ ] PEP 8 準拠の確認とリファクタリング
-   [ ] 型ヒント（Type Hints）の追加
-   [ ] docstring の拡充
-   [ ] コード重複の削減
-   [ ] エラーハンドリングの改善

### セキュリティ

-   [ ] 認証情報の環境変数化（.env ファイル使用）
-   [ ] API キーの安全な管理
-   [ ] 入力値のバリデーション強化
-   [ ] スクレイピング対象サイトへの配慮（Rate Limiting）

### 保守性

-   [ ] ロギング機能の強化（logging モジュール使用）
-   [ ] 設定ファイルの外部化（config.yaml など）
-   [ ] バージョン情報の管理（**version**）
-   [ ] 変更履歴の記録（CHANGELOG.md）

---

## 完了条件チェックリスト

### Phase 1 完了条件

-   [x] 基本的なスクレイピング機能（note_scraper.py）✅
-   [ ] CSV/Excel エクスポート機能
-   [ ] 複数クリエイター一括収集
-   [ ] プロジェクト構造整備
-   [ ] ドキュメント基本整備

### Phase 2 完了条件

-   [ ] 基本統計分析
-   [ ] タグ分析
-   [ ] テキスト分析（文字数、単語数）
-   [ ] キーワード抽出
-   [ ] 単体テスト

### Phase 3 完了条件

-   [ ] 競合分析レポート自動生成
-   [ ] 基本的な可視化
-   [ ] Jupyter Notebook サンプル
-   [ ] 統合テスト

---

## 参考リソース

### 開発ツール

-   [Playwright Python](https://playwright.dev/python/)
-   [pandas](https://pandas.pydata.org/)
-   [matplotlib](https://matplotlib.org/)
-   [scikit-learn](https://scikit-learn.org/)
-   [Janome](https://mocobeta.github.io/janome/)

### ガイドライン

-   [PEP 8](https://pep8-ja.readthedocs.io/)
-   [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
-   [note.com 利用規約](https://note.com/terms)

---

## 更新履歴

-   2024-12-20: 初版作成（Sequential Thinking 分析に基づく）
-   優先度を設定: 高（すぐ実装）、中（重要）、低（あると良い）
-   各タスクに実装方針と例を追加
