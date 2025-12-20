---
name: data-export
description: Export scraped note.com article data to various formats (CSV, Excel, JSON). Use when converting data formats, creating reports, sharing data, or preparing data for external tools like Excel, Google Sheets, or BI tools.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__filesystem__*, mcp__git__*
---

# Data Export Skill

収集したnote.com記事データを様々な形式（CSV、Excel、整形JSON）にエクスポートするスキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- JSONデータをCSVに変換したい時
- Excelファイルとしてエクスポートしたい時
- データを外部ツール（Excel、Google Sheetsなど）で使いたい時
- レポート用にデータを整形したい時
- BIツールやデータ可視化ツールにデータを渡したい時

## Instructions

### 1. エクスポート対象の確認

#### MCPファイルシステムツールを使用
```
mcp__filesystem__search_files でJSONファイルを検索
- path: "data/raw"
- pattern: "articles_*.json"

mcp__filesystem__read_text_file でJSONファイルを読み込み
- path: "data/raw/articles_xxx.json"
```

- 変換元のJSONファイルを特定
- エクスポート形式の決定（CSV, Excel, formatted JSON）
- 必要なフィールドの選択

### 2. データの前処理
- 欠損値の処理
- データ型の統一
- エンコーディングの確認（UTF-8）

### 3. エクスポート実行

#### MCPツールを使用したエクスポート
```
mcp__filesystem__create_directory でエクスポートディレクトリを作成
- path: "exports"

mcp__filesystem__write_file でエクスポート結果を保存
- path: "exports/articles_export_YYYYMMDD.csv"
- content: CSV形式のデータ

mcp__git__git_status でGit状態を確認
mcp__git__git_add でエクスポートファイルをステージング
- files: ["exports/articles_export_YYYYMMDD.csv"]

mcp__git__git_commit でコミット
- message: "Export articles data to CSV (YYYY-MM-DD)"
```

#### CSV形式
```python
import json
import csv

def export_to_csv(json_file, csv_file):
    """JSONをCSVに変換"""
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # CSVヘッダー
    fieldnames = ['url', 'title', 'date', 'likes', 'tags', 'is_paid', 'content_length', 'content_preview']

    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for article in articles:
            writer.writerow({
                'url': article.get('url', ''),
                'title': article.get('title', ''),
                'date': article.get('date', ''),
                'likes': article.get('likes', 0),
                'tags': ', '.join(article.get('tags', [])),
                'is_paid': article.get('is_paid', False),
                'content_length': len(article.get('content', '')),
                'content_preview': article.get('content', '')[:100],
            })
```

#### Excel形式
```python
import pandas as pd

def export_to_excel(json_file, excel_file):
    """JSONをExcelに変換"""
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # DataFrameに変換
    df = pd.DataFrame(articles)

    # タグをカンマ区切り文字列に変換
    df['tags'] = df['tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')

    # コンテンツ長を追加
    df['content_length'] = df['content'].apply(len)

    # Excelに出力（複数シート可能）
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Articles', index=False)

        # 統計シートも追加（オプション）
        stats = create_statistics(articles)
        stats_df = pd.DataFrame(stats)
        stats_df.to_excel(writer, sheet_name='Statistics', index=False)
```

### 4. エクスポート後の確認
- ファイルが正常に生成されているか確認
- 文字化けがないか確認（特にExcel）
- データの整合性確認

## Export Formats

### Format 1: Basic CSV
**用途**: シンプルなデータ共有、Google Sheets連携
**特徴**:
- UTF-8 BOM付き（Excelでの文字化け防止）
- タグはカンマ区切り文字列
- 本文は長さまたはプレビューのみ

**フィールド**:
```
url, title, date, likes, tags, is_paid, content_length
```

### Format 2: Detailed CSV
**用途**: 詳細分析、フルテキスト保存
**特徴**:
- 本文全文を含む
- より多くのメタデータ
- 分析用フィールド追加

**フィールド**:
```
url, title, date, likes, tags, is_paid, content, content_length, tag_count, title_length
```

### Format 3: Excel with Multiple Sheets
**用途**: レポート作成、プレゼンテーション
**シート構成**:
1. **Articles**: 全記事データ
2. **Statistics**: 統計サマリー
3. **Top Articles**: 人気記事Top 20
4. **Tag Analysis**: タグ別集計

### Format 4: Formatted JSON
**用途**: データ共有、バックアップ、API連携
**特徴**:
- インデント付きで読みやすい
- メタデータ追加
- 日本語そのまま（ensure_ascii=False）

## Best Practices

### CSVエクスポート
- **BOM付きUTF-8**: Excelでの文字化け防止のため`utf-8-sig`を使用
- **改行の扱い**: 本文中の改行は適切にエスケープ
- **カンマの扱い**: フィールドをクォートで囲む
- **リストの変換**: タグなどのリストは「,」区切りの文字列に

### Excelエクスポート
- **列幅の自動調整**: 読みやすさのため推奨
- **フィルター有効化**: データ分析のため
- **書式設定**: 日付、数値の適切なフォーマット
- **複数シート活用**: 生データと統計を分離

### データ前処理
- **欠損値**: 空文字列または0で統一
- **長いテキスト**: Excelの制限（32,767文字）に注意
- **日付フォーマット**: ISO 8601形式を維持または変換

### パフォーマンス
- **大量データ**: 分割エクスポートを検討
- **メモリ使用**: pandasのchunksizeを活用
- **圧縮**: 必要に応じてZIP圧縮

## Script Templates

### Template 1: Simple CSV Export
```python
#!/usr/bin/env python3
import json
import csv
import sys

def export_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    fieldnames = ['url', 'title', 'date', 'likes', 'tags', 'is_paid', 'content_length']

    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for article in articles:
            writer.writerow({
                'url': article.get('url', ''),
                'title': article.get('title', ''),
                'date': article.get('date', ''),
                'likes': article.get('likes', 0),
                'tags': ', '.join(article.get('tags', [])),
                'is_paid': 'Yes' if article.get('is_paid', False) else 'No',
                'content_length': len(article.get('content', '')),
            })

    print(f"Exported {len(articles)} articles to {csv_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python export_csv.py <input.json> <output.csv>")
        sys.exit(1)

    export_to_csv(sys.argv[1], sys.argv[2])
```

### Template 2: Excel Export with Stats
```python
#!/usr/bin/env python3
import json
import pandas as pd
import sys
from collections import Counter

def export_to_excel(json_file, excel_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # メインシート: 記事データ
    df = pd.DataFrame(articles)
    df['tags'] = df['tags'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
    df['content_length'] = df['content'].apply(len)
    df['title_length'] = df['title'].apply(len)

    # 統計シート
    stats_data = {
        'Metric': [
            'Total Articles',
            'Total Likes',
            'Average Likes',
            'Median Likes',
            'Max Likes',
            'Paid Articles',
            'Average Content Length'
        ],
        'Value': [
            len(articles),
            df['likes'].sum(),
            df['likes'].mean(),
            df['likes'].median(),
            df['likes'].max(),
            df['is_paid'].sum(),
            df['content_length'].mean()
        ]
    }
    stats_df = pd.DataFrame(stats_data)

    # Top記事シート
    top_articles = df.nlargest(20, 'likes')[['title', 'date', 'likes', 'tags', 'url']]

    # タグ分析シート
    all_tags = []
    for article in articles:
        all_tags.extend(article.get('tags', []))
    tag_counts = Counter(all_tags).most_common(30)
    tags_df = pd.DataFrame(tag_counts, columns=['Tag', 'Count'])

    # Excelに書き出し
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Articles', index=False)
        stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        top_articles.to_excel(writer, sheet_name='Top 20 Articles', index=False)
        tags_df.to_excel(writer, sheet_name='Tag Analysis', index=False)

    print(f"Exported {len(articles)} articles to {excel_file}")
    print(f"Created 4 sheets: Articles, Statistics, Top 20 Articles, Tag Analysis")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python export_excel.py <input.json> <output.xlsx>")
        sys.exit(1)

    export_to_excel(sys.argv[1], sys.argv[2])
```

### Template 3: Multi-format Export
```python
#!/usr/bin/env python3
import json
import csv
import pandas as pd
import sys
from pathlib import Path

def export_all_formats(json_file):
    """すべての形式でエクスポート"""
    base_name = Path(json_file).stem

    # CSV
    csv_file = f"{base_name}.csv"
    export_to_csv(json_file, csv_file)

    # Excel
    excel_file = f"{base_name}.xlsx"
    export_to_excel(json_file, excel_file)

    # Formatted JSON
    formatted_json = f"{base_name}_formatted.json"
    export_formatted_json(json_file, formatted_json)

    print(f"✅ Exported to:")
    print(f"  - {csv_file}")
    print(f"  - {excel_file}")
    print(f"  - {formatted_json}")

def export_formatted_json(input_file, output_file):
    """整形されたJSONとして再出力"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

## Common Use Cases

### Case 1: Excel分析用エクスポート
```bash
# pandasが必要
pip install pandas openpyxl

python scripts/export_excel.py articles_tag_python_1234567890.json output.xlsx
```

### Case 2: Google Sheets用CSV
```bash
python scripts/export_csv.py articles_creator_abc_1234567890.json output.csv
# output.csvをGoogle Sheetsにアップロード
```

### Case 3: BIツール連携
```bash
# 複数JSONをまとめてCSVに
for file in articles_*.json; do
    python scripts/export_csv.py "$file" "${file%.json}.csv"
done
```

## Advanced Features

### カスタムフィールド追加
```python
def add_custom_fields(df):
    """分析用のカスタムフィールドを追加"""
    # 人気度カテゴリ
    df['popularity'] = pd.cut(df['likes'],
                              bins=[0, 10, 50, 100, float('inf')],
                              labels=['Low', 'Medium', 'High', 'Very High'])

    # タグ数
    df['tag_count'] = df['tags'].apply(lambda x: len(x.split(', ')) if x else 0)

    # 投稿曜日
    df['day_of_week'] = pd.to_datetime(df['date']).dt.day_name()

    # 本文の読了時間（分）
    df['reading_time_min'] = (df['content_length'] / 600).round(1)

    return df
```

### データフィルタリング
```python
def export_filtered_data(json_file, excel_file, min_likes=0, tags=None):
    """条件に合う記事のみエクスポート"""
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    # フィルタリング
    filtered = [
        a for a in articles
        if a.get('likes', 0) >= min_likes
        and (not tags or any(t in a.get('tags', []) for t in tags))
    ]

    # エクスポート
    df = pd.DataFrame(filtered)
    df.to_excel(excel_file, index=False)

    print(f"Filtered {len(filtered)}/{len(articles)} articles")
```

### 集計シートの強化
```python
def create_advanced_stats(articles):
    """高度な統計シート作成"""
    df = pd.DataFrame(articles)

    # 基本統計
    basic_stats = df['likes'].describe()

    # 日付別集計
    df['date_only'] = pd.to_datetime(df['date']).dt.date
    by_date = df.groupby('date_only').agg({
        'likes': ['count', 'sum', 'mean']
    })

    # タグ別集計
    # （タグを展開して集計）

    return {
        'basic': basic_stats,
        'by_date': by_date,
    }
```

## Output Example

### CSV出力例
```csv
url,title,date,likes,tags,is_paid,content_length
https://note.com/user/n/abc123,Pythonで始めるデータ分析,2024-01-15T10:00:00+09:00,245,Python, データ分析, 初心者,No,3542
https://note.com/user/n/def456,機械学習の基礎,2024-01-20T14:30:00+09:00,189,Python, 機械学習, AI,Yes,4821
```

### Excel出力（複数シート）
**Articles シート**:
| url | title | date | likes | tags | is_paid | content_length |
|-----|-------|------|-------|------|---------|----------------|
| ... | ... | ... | ... | ... | ... | ... |

**Statistics シート**:
| Metric | Value |
|--------|-------|
| Total Articles | 150 |
| Total Likes | 5,432 |
| Average Likes | 36.2 |

**Top 20 Articles シート**:
人気記事のランキング

**Tag Analysis シート**:
タグ別の使用頻度

## Dependencies

必要なPythonパッケージ:

```bash
# CSV のみ
# 追加パッケージ不要（標準ライブラリ）

# Excel エクスポート
pip install pandas openpyxl

# 高度な分析・可視化
pip install pandas openpyxl matplotlib seaborn
```

## Validation Checklist

エクスポート実行時の確認:
- [ ] ファイルが正常に生成されている
- [ ] 文字化けがない（特にExcelで確認）
- [ ] すべてのデータが含まれている
- [ ] 日付フォーマットが正しい
- [ ] タグが適切に変換されている
- [ ] 本文の長さが正しい

## Troubleshooting

### 文字化け（Excel）
- `encoding='utf-8-sig'`を使用（CSV）
- pandasでExcel出力時は通常問題なし

### ファイルサイズが大きい
- 本文フィールドをプレビューのみに
- 複数ファイルに分割
- 圧縮（ZIP）を検討

### Excelの文字数制限
- 1セルの最大文字数: 32,767文字
- 超える場合は切り詰めまたは別ファイルに

### pandas/openpyxlのエラー
```bash
pip install --upgrade pandas openpyxl
```

### メモリ不足（大量データ）
```python
# chunksizeを使用
for chunk in pd.read_json(json_file, lines=True, chunksize=1000):
    # 処理
```
