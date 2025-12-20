---
name: data-analyzer
description: Analyze scraped note.com article data from JSON files. Use when analyzing article statistics, calculating metrics, finding trends, or generating insights from collected data. Provides comprehensive data analysis including likes distribution, tag analysis, and content metrics.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__filesystem__*, mcp__sequential-thinking__*, mcp__memory__*
---

# Data Analyzer Skill

収集したnote.com記事データ（JSON）を分析し、統計情報やインサイトを提供するスキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- 収集したJSONデータの分析が必要な時
- 記事のスキ数や統計情報を集計したい時
- タグの分布や人気タグを調べたい時
- 記事の傾向やパターンを見つけたい時
- データの要約レポートを作成したい時

## Instructions

### 1. データファイルの確認

#### MCPファイルシステムツールを使用（推奨）
```
mcp__filesystem__search_files でJSONファイルを検索
- path: "."
- pattern: "articles_*.json"

mcp__filesystem__list_directory_with_sizes でファイルサイズも確認
- path: "data/raw"
- sortBy: "size"
```

#### 従来のBashコマンドを使用
```bash
find . -name "articles_*.json" -type f
ls -lht *.json data/raw/*.json 2>/dev/null
```

### 2. データの読み込みと基本確認

#### MCPツールを使用
```
mcp__filesystem__read_text_file でJSONファイルを読み込み
- path: "data/raw/articles_xxx.json"

mcp__filesystem__read_multiple_files で複数ファイルを同時読み込み
- paths: ["file1.json", "file2.json", "file3.json"]
```

- 記事数を確認
- データ構造の検証（必須フィールドの存在確認）

### 3. 基本統計の算出

#### スキ数の統計
- 合計スキ数
- 平均スキ数
- 中央値
- 最大値・最小値
- 標準偏差
- 分布（四分位数）

#### 記事数の集計
- 総記事数
- 有料記事数 vs 無料記事数
- 日付別の記事数

#### タグ分析
- 使用されているタグの一覧
- タグ別の記事数
- 人気タグTop 10
- タグの共起分析

#### コンテンツ分析
- 平均文字数
- 文字数の分布
- タイトル長の統計

### 4. インサイトの抽出

#### MCP Sequential Thinkingツールを使用（複雑な分析）
複雑なパターン認識や多段階分析には `mcp__sequential-thinking__sequentialthinking` を活用:
- 複数の仮説を立てて検証
- 段階的に問題を分解
- 分析結果の妥当性を確認

**分析項目**:
- 最も人気のある記事（スキ数Top 10）
- 人気記事の共通点
- スキを集めやすいタグ
- 投稿時期と人気度の関係

#### MCP Memoryツールでインサイトを保存
分析で得られた重要なインサイトは `mcp__memory__*` ツールでナレッジグラフに保存:
```
mcp__memory__create_entities で分析結果をエンティティとして保存
- entities: [
    {
      name: "人気タグ分析_2024-12",
      entityType: "analysis_result",
      observations: ["Pythonタグは平均85スキ", "データ分析タグは平均78スキ"]
    }
  ]

mcp__memory__create_relations でデータ間の関係性を記録
- relations: [
    {from: "Pythonタグ", to: "高エンゲージメント", relationType: "results_in"}
  ]
```

### 5. レポート生成

#### MCPツールを使用
```
mcp__filesystem__write_file でMarkdownレポートを保存
- path: "reports/analysis_report_YYYYMMDD.md"
- content: 分析結果のMarkdown形式テキスト
```

分析結果を分かりやすくMarkdown形式でレポート作成

## Analysis Script Template

必要に応じて以下のような分析スクリプトを作成:

```python
import json
from collections import Counter
from statistics import mean, median, stdev

def analyze_articles(json_file):
    """記事データの基本分析"""
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # 基本統計
    total = len(articles)
    likes_list = [a['likes'] for a in articles if 'likes' in a]

    stats = {
        'total_articles': total,
        'total_likes': sum(likes_list),
        'avg_likes': mean(likes_list) if likes_list else 0,
        'median_likes': median(likes_list) if likes_list else 0,
        'max_likes': max(likes_list) if likes_list else 0,
        'min_likes': min(likes_list) if likes_list else 0,
    }

    # タグ分析
    all_tags = []
    for article in articles:
        all_tags.extend(article.get('tags', []))
    tag_counts = Counter(all_tags)

    # 有料記事
    paid_count = sum(1 for a in articles if a.get('is_paid', False))

    return {
        'stats': stats,
        'top_tags': tag_counts.most_common(10),
        'paid_ratio': paid_count / total if total > 0 else 0,
    }
```

## Best Practices

### データ検証
- 分析前に必ずデータの整合性をチェック
- 欠損値（None, 空文字列）の扱いを明確にする
- 異常値（極端に大きい/小さい値）を確認

### 統計計算
- スキ数が0の記事も考慮
- 平均だけでなく中央値も確認（外れ値の影響を避ける）
- データ数が少ない場合は統計の信頼性に注意

### 可視化の推奨
- 分布グラフ（ヒストグラム）
- 時系列グラフ（日付別推移）
- タグクラウド
- Top N記事のバーチャート

### レポート構成
1. **サマリー**: 総記事数、総スキ数、平均など
2. **詳細統計**: 分布、中央値、四分位数
3. **トップ記事**: スキ数Top 10のリスト
4. **タグ分析**: 人気タグと使用頻度
5. **インサイト**: 発見した傾向やパターン

## Common Analysis Patterns

### Pattern 1: スキ数分析
```python
# スキ数でソート
sorted_by_likes = sorted(articles, key=lambda x: x.get('likes', 0), reverse=True)
top_10 = sorted_by_likes[:10]

# 分布を確認
quartiles = [
    len([a for a in articles if a['likes'] < 10]),
    len([a for a in articles if 10 <= a['likes'] < 50]),
    len([a for a in articles if 50 <= a['likes'] < 100]),
    len([a for a in articles if a['likes'] >= 100]),
]
```

### Pattern 2: タグ共起分析
```python
from itertools import combinations

# タグの組み合わせを分析
tag_pairs = []
for article in articles:
    tags = article.get('tags', [])
    if len(tags) >= 2:
        tag_pairs.extend(combinations(tags, 2))

common_pairs = Counter(tag_pairs).most_common(10)
```

### Pattern 3: 日付別トレンド
```python
from datetime import datetime
from collections import defaultdict

# 日付別の記事数とスキ数
by_date = defaultdict(lambda: {'count': 0, 'likes': 0})
for article in articles:
    date_str = article.get('date', '').split('T')[0]
    if date_str:
        by_date[date_str]['count'] += 1
        by_date[date_str]['likes'] += article.get('likes', 0)
```

## Output Example

分析レポートの例:

```markdown
# note.com 記事データ分析レポート

## 基本統計
- 総記事数: 150件
- 総スキ数: 5,432
- 平均スキ数: 36.2
- 中央値: 18
- 有料記事割合: 12%

## スキ数分布
- 10未満: 45件 (30%)
- 10-50: 68件 (45%)
- 50-100: 25件 (17%)
- 100以上: 12件 (8%)

## 人気記事 Top 5
1. [記事タイトル1] - 234スキ
2. [記事タイトル2] - 189スキ
...

## 人気タグ Top 10
1. #Python: 45記事
2. #ビジネス: 32記事
...

## インサイト
- スキ100以上の記事は全て「Python」または「データ分析」タグを含む
- 有料記事の平均スキ数(52.3)は無料記事(32.1)より高い傾向
```

## Advanced Analysis

### 文章の特徴分析
- タイトルの文字数と人気度の相関
- 見出しの数と記事の長さ
- 本文の読みやすさ指標

### 時系列分析
- 曜日別の投稿数
- 投稿時刻と反応の関係
- 期間別のトレンド変化

### セグメント分析
- スキ数で記事をグループ化
- タグ別の平均スキ数
- 有料/無料での比較

## Validation Checklist

分析実行時の確認項目:
- [ ] JSONファイルが正しく読み込めている
- [ ] 全記事のデータ構造が一貫している
- [ ] 欠損値の処理が適切
- [ ] 統計値が妥当な範囲内
- [ ] レポートが読みやすく構成されている

## Troubleshooting

### JSONの読み込みエラー
- ファイルパスの確認
- 文字エンコーディング（UTF-8）の確認
- JSON構文の検証

### 統計計算エラー
- 空リストでの計算回避（mean, medianなど）
- ゼロ除算のチェック
- データ型の確認（文字列 vs 数値）

### メモリ不足
- 大量データは分割処理
- 必要なフィールドのみ読み込み
- ジェネレータの活用
