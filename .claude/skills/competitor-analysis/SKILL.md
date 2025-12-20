---
name: competitor-analysis
description: Compare and analyze multiple note.com creators to identify competitive advantages and content strategies. Use when comparing creators, analyzing competition, benchmarking performance, or generating competitive intelligence reports.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__filesystem__*, mcp__sequential-thinking__*, mcp__memory__*, mcp__tavily-mcp__*, mcp__fetch__*
---

# Competitor Analysis Skill

複数のnote.comクリエイターを比較分析し、競合優位性とコンテンツ戦略を明らかにするスキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- 複数のクリエイターを比較したい時
- 競合のコンテンツ戦略を分析したい時
- 自分と競合のパフォーマンスを比較したい時
- 競合インテリジェンスレポートを作成したい時
- ベンチマーク分析が必要な時

## Instructions

### 1. 比較対象の特定
- 分析対象のクリエイターIDリストを取得
- 各クリエイターのJSONデータを確認
- データ収集期間の整合性をチェック

#### MCP Memoryツールで競合情報を記憶
```
mcp__memory__search_nodes で過去の競合分析を検索
- query: "競合クリエイター"

mcp__memory__create_entities で新しい競合をエンティティとして登録
- entities: [
    {
      name: "Creator_A",
      entityType: "competitor",
      observations: ["note.com/@creator_a", "2024年12月時点で120記事"]
    }
  ]
```

### 2. データの収集

#### 最新情報の取得（MCP Tavilyツールを使用）
競合クリエイターの最新動向を調査:
```
mcp__tavily-mcp__tavily-search で競合の最新情報を検索
- query: "note.com creator_name 最新記事"
- max_results: 10

mcp__fetch__fetch で競合のnoteプロフィールページを取得
- url: "https://note.com/@creator_id"
```

#### 既存データの収集（従来の方法）
```bash
for creator in creator1 creator2 creator3; do
    python src/note_scraper.py --creator $creator
done
```

### 3. 比較分析の実行

#### 基本メトリクス比較
各クリエイターについて:
- 総記事数
- 総スキ数
- 平均スキ数
- 中央値スキ数
- 投稿頻度（記事数/期間）
- 有料記事割合

#### コンテンツ戦略分析
- 主要タグの比較
- 記事の長さ（平均文字数）
- タイトルの特徴
- 有料/無料コンテンツのバランス

#### パフォーマンス分析
- エンゲージメント率（スキ数/記事数）
- 人気記事の傾向
- 成長トレンド（時系列分析）

### 4. ベンチマーキング

#### MCP Sequential Thinkingツールを使用
複雑な比較分析には `mcp__sequential-thinking__sequentialthinking` を活用:
- 複数クリエイターの強み・弱みを段階的に分析
- 仮説（例: 「投稿頻度が高いほどエンゲージメントが高い」）を検証
- 改善ポイントを論理的に導出

**分析項目**:
- 業界平均との比較
- トップパフォーマーとの差分
- 改善ポイントの特定

#### MCP Memoryツールで競合関係を記録
```
mcp__memory__create_relations で競合間の関係性を記録
- relations: [
    {from: "Creator_A", to: "Creator_B", relationType: "competes_with"},
    {from: "Creator_B", to: "Python分野", relationType: "specializes_in"}
  ]

mcp__memory__add_observations でベンチマーク結果を追加
- observations: [
    {
      entityName: "Creator_A",
      contents: ["業界平均より30%高いエンゲージメント率", "2024年12月分析結果"]
    }
  ]
```

### 5. レポート生成

#### MCPツールを使用
```
mcp__filesystem__write_file でレポートを保存
- path: "reports/competitor_analysis_YYYYMMDD.md"
- content: 比較分析レポート（Markdown形式）

mcp__filesystem__create_directory でレポート用ディレクトリを作成
- path: "reports"
```

**レポート内容**:
- 比較表の作成
- 強み・弱みの分析
- 推奨アクションの提示

## Analysis Framework

### SWOT分析の適用
各クリエイターについて:
- **Strengths**: 強み（高いスキ数、人気タグ、投稿頻度など）
- **Weaknesses**: 弱み（低いエンゲージメント、限定的なタグなど）
- **Opportunities**: 機会（未開拓のタグ、成長トレンドなど）
- **Threats**: 脅威（競合の強み、市場変化など）

### 競争優位性の分析
- 差別化要素の特定
- コンテンツの質 vs 量
- オーディエンスエンゲージメント
- ニッチ戦略 vs 幅広い戦略

## Comparison Script Template

```python
import json
from pathlib import Path

def compare_creators(creator_files):
    """複数クリエイターの比較分析"""
    results = {}

    for file_path in creator_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)

        creator_name = Path(file_path).stem

        # 基本メトリクス
        total_articles = len(articles)
        likes_list = [a.get('likes', 0) for a in articles]

        results[creator_name] = {
            'total_articles': total_articles,
            'total_likes': sum(likes_list),
            'avg_likes': sum(likes_list) / total_articles if total_articles > 0 else 0,
            'max_likes': max(likes_list) if likes_list else 0,
            'engagement_rate': sum(likes_list) / total_articles if total_articles > 0 else 0,

            # タグ分析
            'top_tags': get_top_tags(articles, n=5),

            # コンテンツ特徴
            'avg_content_length': sum(len(a.get('content', '')) for a in articles) / total_articles if total_articles > 0 else 0,
            'paid_ratio': sum(1 for a in articles if a.get('is_paid', False)) / total_articles if total_articles > 0 else 0,
        }

    return results

def get_top_tags(articles, n=5):
    """頻出タグTop N"""
    from collections import Counter
    all_tags = []
    for article in articles:
        all_tags.extend(article.get('tags', []))
    return Counter(all_tags).most_common(n)
```

## Best Practices

### データの公平性
- 同じ期間のデータで比較
- 収集条件を揃える（同じスクレイピング設定）
- 欠損データの扱いを統一

### 多角的な比較
- 量的指標（記事数、スキ数）だけでなく質的指標も重視
- 平均値だけでなく中央値や分布も確認
- 時系列での変化も考慮

### コンテキストの理解
- クリエイターのジャンルや専門性を考慮
- フォロワー数などの外部要因も加味
- 投稿開始時期の違いを認識

### アクション指向
- 単なる比較で終わらず、改善アクションを提示
- 学べる点を具体的に抽出
- 実行可能な施策を推奨

## Common Comparison Patterns

### Pattern 1: パフォーマンスマトリックス
```
             記事数  総スキ  平均スキ  中央値  最大スキ
Creator A     120    4,500    37.5     25      345
Creator B      85    6,200    72.9     48      892
Creator C     200    5,800    29.0     15      456
```

### Pattern 2: タグ戦略の比較
各クリエイターの主要タグとその効果を比較:
- Creator A: #ビジネス (40記事, 平均52スキ), #マーケティング (30記事, 平均45スキ)
- Creator B: #Python (25記事, 平均85スキ), #データ分析 (20記事, 平均78スキ)

### Pattern 3: エンゲージメント効率
```
Creator A: 37.5 スキ/記事
Creator B: 72.9 スキ/記事 ← 最も効率的
Creator C: 29.0 スキ/記事
```

## Report Template

レポート構成の推奨テンプレート（[REFERENCE.md](REFERENCE.md)参照）:

### 1. エグゼクティブサマリー
- 分析対象と期間
- 主要な発見（3-5項目）
- 推奨アクション

### 2. クリエイター概要
各クリエイターの基本情報とポジショニング

### 3. 定量比較
- パフォーマンスメトリクスの比較表
- 視覚的な比較（グラフ推奨）

### 4. 定性分析
- コンテンツ戦略の違い
- 強み・弱みの分析
- 差別化ポイント

### 5. ベンチマーク分析
- 業界標準との比較
- ギャップ分析

### 6. 推奨事項
- 学ぶべき点
- 改善アクション
- 差別化戦略

## Advanced Analysis

### セグメント別比較
- 有料記事 vs 無料記事のパフォーマンス
- タグカテゴリー別の効果
- 記事の長さ別のエンゲージメント

### 時系列トレンド
- 成長率の比較
- 季節性の分析
- 直近のパフォーマンス変化

### 相関分析
- 投稿頻度とエンゲージメントの関係
- 記事の長さとスキ数の相関
- タグ数と人気度の関係

## Competitive Insights Examples

### インサイト 1: コンテンツ戦略
```
Creator Bは記事数が少ないものの、平均スキ数が2倍近く高い。
→ 質重視の戦略が効果的
→ 専門性の高いニッチなタグに集中
```

### インサイト 2: タグ戦略
```
Creator Aは幅広いタグを使用（20種類以上）
Creator Bは5つの専門タグに集中
→ Creator Bの集中戦略がエンゲージメント率で優位
```

### インサイト 3: 有料化戦略
```
Creator Cは有料記事割合が高い（35%）が、平均スキ数は低い
→ 有料化が早すぎる可能性
→ まず無料で価値提供し、関係構築が重要
```

## Output Example

```markdown
# 競合クリエイター分析レポート

## サマリー
3名のクリエイターを比較分析。Creator Bが最も効率的なエンゲージメントを獲得。

## 主要発見
1. Creator Bは記事数が少ないが、質の高いコンテンツで高いスキ数を獲得
2. ニッチなタグへの集中戦略が効果的
3. 有料化は十分なファン獲得後が望ましい

## 定量比較

| メトリクス | Creator A | Creator B | Creator C |
|-----------|-----------|-----------|-----------|
| 記事数    | 120       | 85        | 200       |
| 総スキ    | 4,500     | 6,200     | 5,800     |
| 平均スキ  | 37.5      | 72.9      | 29.0      |
| 有料記事率| 10%       | 15%       | 35%       |

## 推奨アクション
1. Creator Bのニッチ集中戦略を参考にタグを絞る
2. 記事の質を重視し、投稿頻度より価値提供を優先
3. 有料化はフォロワー基盤構築後に検討
```

## Validation Checklist

分析実行時の確認:
- [ ] すべてのクリエイターデータが揃っている
- [ ] データ収集期間が統一されている
- [ ] 比較メトリクスが公平である
- [ ] 定量・定性の両面から分析している
- [ ] 実行可能な推奨事項を含んでいる

## Troubleshooting

### データ不整合
- 収集期間の違いを調整
- 欠損データの補完または除外
- 異常値の確認

### 比較の難しさ
- ジャンルが異なる場合は相対評価を使用
- 絶対値だけでなく比率や率で比較
- コンテキストを明記

### レポートが長すぎる
- エグゼクティブサマリーで要点を絞る
- 詳細は別セクションに分離
- 視覚的な要素（表・グラフ）を活用
