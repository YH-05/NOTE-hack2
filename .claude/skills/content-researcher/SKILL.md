---
name: content-researcher
description: Research topics for note.com articles using web search and Wikipedia. Use when user needs to gather information for article writing, verify facts, find trending topics, or explore related concepts. Helps with content ideation and background research.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__tavily-mcp__*, mcp__wikipedia__*, mcp__fetch__*, mcp__memory__*, mcp__filesystem__*
---

# Content Researcher Skill

note.com記事執筆のためのリサーチを支援するスキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- 記事執筆のための情報収集が必要な時
- トレンドトピックを調査したい時
- ファクトチェックが必要な時
- 関連概念や背景知識を調べたい時
- コンテンツアイデアを探している時
- 競合記事の内容を調査したい時

## Instructions

### 1. リサーチトピックの特定
- 記事のテーマを明確にする
- リサーチの目的を定義（情報収集、ファクトチェック、トレンド調査など）
- 検索キーワードをリストアップ

### 2. Web検索による最新情報の収集

#### MCP Tavilyツールを使用（推奨）
```
mcp__tavily-mcp__tavily-search で最新情報を検索
- query: "検索キーワード"
- max_results: 10
- search_depth: "basic" または "advanced"
- topic: "general" または "news"
- time_range: "week" または "month"  # 最新情報の場合

例: トレンド調査
- query: "note.com 人気記事 2024"
- topic: "news"
- time_range: "month"

例: 技術情報収集
- query: "Python データ分析 最新ライブラリ"
- search_depth: "advanced"
- max_results: 15
```

#### 検索結果の分析
- 信頼性の高い情報源を特定
- 複数のソースで情報を確認
- トレンドやパターンを把握

### 3. Wikipedia調査による背景知識の取得

#### MCP Wikipediaツールを使用
```
mcp__wikipedia__search_wikipedia でトピックを検索
- query: "調査したい概念やキーワード"
- limit: 10

mcp__wikipedia__get_summary で概要を取得
- title: "記事タイトル"

mcp__wikipedia__get_article で詳細を取得
- title: "記事タイトル"

mcp__wikipedia__get_related_topics で関連トピックを探索
- title: "記事タイトル"
- limit: 10

mcp__wikipedia__extract_key_facts で重要な事実を抽出
- title: "記事タイトル"
- topic_within_article: "特定のセクション"  # オプション
- count: 5
```

### 4. 特定URLの内容取得

#### MCP Fetchツールを使用
```
mcp__fetch__fetch でWebページの内容を取得
- url: "https://example.com/article"
- prompt: "この記事の主要ポイントを3-5個にまとめて"

例: 競合記事の分析
- url: "https://note.com/competitor/n/article_id"
- prompt: "記事の構成、見出し、主要なポイントを抽出"

例: リファレンス情報の収集
- url: "https://docs.python.org/ja/3/library/statistics.html"
- prompt: "統計関数の使い方と例を抽出"
```

### 5. リサーチ結果の整理と保存

#### MCP Memoryツールでリサーチ内容を記憶
```
mcp__memory__create_entities でリサーチトピックを保存
- entities: [
    {
      name: "Python_データ分析_リサーチ_2024-12",
      entityType: "research_topic",
      observations: [
        "pandasが最も人気",
        "Polarsが新たなトレンド",
        "可視化にはMatplotlib/Seabornが主流"
      ]
    }
  ]

mcp__memory__create_relations でトピック間の関係を記録
- relations: [
    {from: "Python", to: "データ分析", relationType: "used_for"},
    {from: "Polars", to: "pandas", relationType: "alternative_to"}
  ]

mcp__memory__search_nodes で過去のリサーチを検索
- query: "Python リサーチ"
```

#### MCP Filesystemツールでリサーチノートを保存
```
mcp__filesystem__create_directory でリサーチディレクトリを作成
- path: "research"

mcp__filesystem__write_file でリサーチノートを保存
- path: "research/topic_YYYYMMDD.md"
- content: リサーチ結果のMarkdownテキスト
```

### 6. コンテンツアイデアの生成
リサーチ結果を基に:
- トレンドトピックの特定
- 未カバーのニッチ領域の発見
- 競合記事との差別化ポイントの抽出
- 記事の切り口やアングルの提案

## Best Practices

### 情報の信頼性確認
- 複数のソースで事実を確認
- 一次情報を優先
- 最新性を考慮（特に技術情報）
- 著者や出典の信頼性を評価

### 効率的なリサーチ
- 広く浅く → 深く掘り下げの順序
- 関連トピックを芋づる式に調査
- 検索キーワードを工夫（同義語、関連語）
- 時間制限を設ける（リサーチ沼を避ける）

### リサーチ結果の記録
- 重要な情報源のURLを保存
- 引用する可能性のある部分をメモ
- 日付を記録（情報の鮮度管理）
- カテゴリー別に整理

### 倫理的配慮
- 著作権を尊重
- 引用元を明記
- パクリ禁止（参考にして自分の言葉で）
- ファクトチェックの徹底

## Common Use Cases

### Case 1: トレンドトピックの調査
```
目的: 現在人気のあるトピックを見つける

1. Tavilyで最新ニュースを検索
   - query: "note.com 人気記事"
   - topic: "news"
   - time_range: "month"

2. 複数のトピックで検索
   - "Python 2024 トレンド"
   - "ビジネス トレンド 2024"
   - "副業 人気 2024"

3. 検索結果から共通テーマを抽出
4. Memoryツールで記録
```

### Case 2: 技術記事のための情報収集
```
目的: Pythonデータ分析記事を書くための情報収集

1. Wikipediaで基礎知識を取得
   - search: "データ分析"
   - get_article: "データ分析"
   - get_related_topics

2. Tavilyで最新ライブラリを調査
   - query: "Python データ分析 ライブラリ 2024"
   - search_depth: "advanced"

3. 公式ドキュメントを確認
   - fetch: "https://pandas.pydata.org/"
   - prompt: "主要機能と使い方を抽出"

4. リサーチノートとして保存
   - filesystem: "research/python_data_analysis_2024.md"
```

### Case 3: 競合記事の分析
```
目的: 人気記事の内容と構成を分析

1. note.comの人気記事URLを収集
2. Fetchツールで各記事の内容を取得
   - prompt: "タイトル、見出し構成、主要ポイントを抽出"

3. 共通パターンを特定
4. 差別化ポイントを考案
5. Memoryツールで競合分析結果を保存
```

### Case 4: ファクトチェック
```
目的: 記事に含める情報の正確性を確認

1. 主張や統計データをリストアップ
2. Wikipediaで概要を確認
3. Tavilyで最新情報を検索
4. 複数のソースで事実確認
5. 信頼できる一次情報を引用元として記録
```

## Research Workflow

### Phase 1: 広く浅く（30分）
1. Wikipediaで基礎知識を取得
2. Tavilyで最新情報をざっと検索
3. 関連トピックを発見
4. リサーチの方向性を決定

### Phase 2: 深く掘り下げ（1-2時間）
1. 重要なトピックを選定
2. 詳細な情報を収集
3. 複数のソースで確認
4. データや統計を収集

### Phase 3: 整理と記録（30分）
1. リサーチノートを作成
2. 引用元URLをリスト化
3. Memoryツールで記録
4. コンテンツアイデアをメモ

### Phase 4: アウトライン作成（30分）
1. リサーチ内容を基に記事構成を考案
2. 見出しを作成
3. 各セクションの要点を整理

## Research Note Template

リサーチノートの推奨フォーマット:

```markdown
# リサーチノート: [トピック名]

**日付**: YYYY-MM-DD
**目的**: [リサーチの目的]

## 主要な発見

### 発見1: [タイトル]
- **情報源**: [URL]
- **要点**: ...
- **信頼性**: 高/中/低
- **日付**: YYYY-MM-DD

### 発見2: [タイトル]
...

## トレンド・パターン

- パターン1: ...
- パターン2: ...

## 関連トピック

- [関連トピック1]
- [関連トピック2]

## コンテンツアイデア

1. アイデア1: ...
2. アイデア2: ...

## TODO

- [ ] さらに調査が必要な項目
- [ ] ファクトチェックが必要な情報

## 参考URL

- [タイトル1](URL1)
- [タイトル2](URL2)
```

## Advanced Research Techniques

### クロスリファレンス
- 複数の情報源を相互参照
- 矛盾する情報を特定
- 最も信頼性の高い情報を選定

### トレンド分析
- 時系列での変化を追跡
- 検索ボリュームの推移（推測）
- 季節性やイベントの影響

### ギャップ分析
- 既存記事でカバーされていない領域を発見
- ニッチなトピックの特定
- 差別化の機会を見出す

### インサイト抽出
- データから意味のあるパターンを発見
- 意外性のある発見を強調
- 読者にとっての価値を明確化

## Output Example

```markdown
# リサーチノート: Pythonデータ分析の最新トレンド

**日付**: 2024-12-20
**目的**: note.com記事「2024年版Pythonデータ分析入門」執筆のための情報収集

## 主要な発見

### 発見1: Polarsの台頭
- **情報源**: https://www.pola.rs/
- **要点**: pandasの代替として注目。10-100倍高速。
- **信頼性**: 高（公式サイト、複数のブログで言及）
- **日付**: 2024-12-15

### 発見2: データ可視化ライブラリの多様化
- **情報源**: Wikipedia「データ可視化」
- **要点**: Matplotlib, Seaborn, Plotlyが主流。Altairも人気上昇中。
- **信頼性**: 高
- **日付**: 2024-12-20

## トレンド・パターン

- パフォーマンスへの関心が高まっている（Polars人気の理由）
- インタラクティブな可視化が求められている（Plotly）
- 初心者向けコンテンツの需要が継続

## コンテンツアイデア

1. 「pandasからPolarsへ: 移行ガイド」
2. 「データ可視化ライブラリ徹底比較」
3. 「初心者向け: Pythonデータ分析の始め方2024」

## 参考URL

- [Polars公式サイト](https://www.pola.rs/)
- [Wikipedia: データ分析](https://ja.wikipedia.org/wiki/データ分析)
```

## Validation Checklist

リサーチ完了時の確認:
- [ ] 複数の信頼できる情報源を確認した
- [ ] 最新情報を取得した（日付を確認）
- [ ] ファクトチェックを実施した
- [ ] 引用元URLを記録した
- [ ] リサーチノートを作成した
- [ ] Memoryツールで記録した
- [ ] コンテンツアイデアを整理した

## Troubleshooting

### 情報が見つからない
- 検索キーワードを変更（同義語、英語）
- 検索範囲を広げる（related topics）
- より一般的なトピックから調査

### 情報が多すぎる
- 検索を絞り込む（time_range, search_depth）
- 最も信頼性の高いソースに絞る
- リサーチの目的を再確認

### 情報源の信頼性が不明
- 著者の専門性を確認
- 出版元の評判を調査
- 複数のソースで確認
- 一次情報を探す
