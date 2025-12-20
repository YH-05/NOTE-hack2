---
name: article-trend-analysis
description: Analyze content trends and patterns in popular note.com articles using NLP and text analysis. Use when analyzing writing styles, identifying successful content patterns, extracting keywords, or understanding what makes articles popular.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__filesystem__*, mcp__sequential-thinking__*, mcp__context7__*, mcp__wikipedia__*, mcp__memory__*
---

# Article Trend Analysis Skill

人気記事の文章傾向を自然言語処理で分析し、成功パターンを特定するスキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- 人気記事の文章パターンを分析したい時
- 成功するコンテンツの特徴を知りたい時
- タイトルや見出しの傾向を調べたい時
- キーワードや頻出表現を抽出したい時
- 記事の読みやすさを分析したい時
- 文章スタイルの特徴を理解したい時

## Instructions

### 1. 分析対象の準備
- 人気記事のデータセット特定（スキ数でフィルタ）
- 比較のため、低スキ記事のデータセットも準備
- テキストデータの前処理

### 2. 基本的なテキスト分析

#### 文章量の分析
- 総文字数
- 総単語数（形態素解析）
- 段落数
- 平均文長
- 文の数

#### タイトル分析
- タイトルの文字数分布
- 使用されている記号やEmoji
- 数字の使用頻度
- 疑問形・断定形の比率
- キーワードの出現パターン

#### 構造分析
- 見出しの数と階層
- 見出しのパターン
- リストの使用頻度
- 引用の使用状況

### 3. 自然言語処理による分析

#### MCP Context7ツールでNLPライブラリのドキュメントを取得
最新のNLPライブラリの使い方を確認:
```
mcp__context7__resolve-library-id でライブラリIDを取得
- libraryName: "janome" または "mecab-python3" または "spacy"

mcp__context7__get-library-docs でドキュメントを取得
- context7CompatibleLibraryID: "/organization/library-name"
- topic: "tokenization" または "pos tagging"
- mode: "code"
```

#### MCP Wikipediaツールで言語学的概念を調査
```
mcp__wikipedia__search_wikipedia で関連概念を検索
- query: "形態素解析" または "TF-IDF" または "自然言語処理"

mcp__wikipedia__get_summary で概要を取得
- title: "形態素解析"
```

#### 形態素解析（必要に応じてMeCabやjanomeを使用）
```python
# 形態素解析の例
import MeCab
# または
# import janome.tokenizer

def analyze_text(text):
    """テキストを形態素解析"""
    mecab = MeCab.Tagger()
    parsed = mecab.parse(text)
    # 名詞、動詞、形容詞を抽出
    # ...
```

#### キーワード抽出
- TF-IDF による重要キーワード抽出
- 頻出名詞・動詞・形容詞の抽出
- 専門用語の抽出
- 共起語の分析

#### 感情・トーン分析
- ポジティブ/ネガティブワードの比率
- 断定的 vs 控えめな表現
- 専門的 vs カジュアルな文体

### 4. 人気記事と一般記事の比較
高スキ記事（Top 20%）と低スキ記事（Bottom 20%）を比較:
- 文章量の違い
- タイトルパターンの違い
- キーワードの違い
- 構造の違い
- 文体の違い

### 5. パターンの特定と推奨事項

#### MCP Sequential Thinkingツールを使用
複雑なパターン認識には `mcp__sequential-thinking__sequentialthinking` を活用:
- 人気記事の成功要因を段階的に分析
- 複数の仮説（例: 「タイトルに数字を含むと人気が高い」）を検証
- データから論理的に推奨事項を導出

**分析項目**:
- 成功している記事の共通パターン
- 避けるべきパターン
- 具体的な執筆推奨事項

#### MCP Memoryツールでパターンを記憶
```
mcp__memory__create_entities でトレンドパターンを保存
- entities: [
    {
      name: "人気タイトルパターン_2024-12",
      entityType: "trend_pattern",
      observations: [
        "数字を含むタイトルは平均スキ数が1.8倍",
        "18-25文字が最適",
        "具体性が重要"
      ]
    }
  ]

mcp__memory__create_relations でパターン間の関係を記録
- relations: [
    {from: "数字使用", to: "高エンゲージメント", relationType: "correlates_with"}
  ]
```

## Analysis Framework

### レベル1: 基本分析（形態素解析不要）
```python
def basic_text_analysis(article):
    """基本的なテキスト分析"""
    content = article.get('content', '')
    title = article.get('title', '')

    return {
        'char_count': len(content),
        'title_length': len(title),
        'line_count': content.count('\n') + 1,
        'has_numbers_in_title': bool(re.search(r'\d', title)),
        'has_question_in_title': '?' in title or '？' in title,
        'paragraph_count': len([p for p in content.split('\n\n') if p.strip()]),
    }
```

### レベル2: 高度な分析（形態素解析使用）
```python
def advanced_text_analysis(article, mecab):
    """形態素解析を使った高度な分析"""
    content = article.get('content', '')

    # 形態素解析
    nodes = mecab.parse(content)

    # 品詞別の単語抽出
    nouns = extract_pos(nodes, '名詞')
    verbs = extract_pos(nodes, '動詞')
    adjectives = extract_pos(nodes, '形容詞')

    return {
        'noun_count': len(nouns),
        'verb_count': len(verbs),
        'adjective_count': len(adjectives),
        'unique_nouns': len(set(nouns)),
        'lexical_diversity': len(set(nouns)) / len(nouns) if nouns else 0,
    }
```

### レベル3: パターン認識
```python
def identify_patterns(high_like_articles, low_like_articles):
    """人気記事のパターンを特定"""
    # 高スキ記事の特徴
    high_features = aggregate_features(high_like_articles)

    # 低スキ記事の特徴
    low_features = aggregate_features(low_like_articles)

    # 差分を計算
    patterns = compare_features(high_features, low_features)

    return patterns
```

## Best Practices

### データ準備
- 十分なサンプルサイズ（最低30記事以上）
- 人気記事の定義を明確に（例: スキ数Top 20%）
- 同じ期間、同じジャンルで比較

### 分析の公平性
- 文字数の影響を考慮（正規化）
- アウトライヤー（外れ値）の扱い
- サンプルの偏りに注意

### 解釈の注意点
- 相関関係 ≠ 因果関係
- 多面的な視点で評価
- コンテキストを考慮

### アクション指向
- 具体的で実行可能な推奨事項
- 優先順位の明確化
- A/Bテストの提案

## Common Analysis Patterns

### Pattern 1: タイトル分析
```python
def analyze_titles(articles):
    """タイトルの傾向分析"""
    titles = [a['title'] for a in articles]

    analysis = {
        'avg_length': sum(len(t) for t in titles) / len(titles),
        'with_numbers': sum(1 for t in titles if re.search(r'\d', t)) / len(titles),
        'with_question': sum(1 for t in titles if '?' in t or '?' in t) / len(titles),
        'with_brackets': sum(1 for t in titles if '【' in t or '『' in t) / len(titles),
    }

    return analysis
```

**典型的な発見**:
- 人気記事は数字を含むタイトルが多い（例: "3つの方法"）
- 適度な長さ（15-30文字）が最適
- 具体性のあるタイトルが好まれる

### Pattern 2: コンテンツ構造分析
```python
def analyze_structure(content):
    """記事構造の分析"""
    # 見出しのパターン（#で始まる行）
    headings = re.findall(r'^#+\s+.+$', content, re.MULTILINE)

    # リストの使用
    lists = re.findall(r'^[-*\d]+\.?\s+', content, re.MULTILINE)

    return {
        'heading_count': len(headings),
        'list_count': len(lists),
        'has_clear_structure': len(headings) >= 3,
    }
```

**典型的な発見**:
- 人気記事は明確な見出し構造を持つ
- リストや箇条書きを効果的に使用
- 3-7個の主要セクションが最適

### Pattern 3: キーワード分析
```python
from collections import Counter

def extract_keywords(articles, top_n=20):
    """頻出キーワード抽出"""
    # 全記事のテキストを結合
    all_text = ' '.join(a['content'] for a in articles)

    # 形態素解析（簡易版はスペース分割でも可）
    words = simple_tokenize(all_text)

    # ストップワード除去
    words = [w for w in words if w not in STOP_WORDS and len(w) > 1]

    # 頻出語
    return Counter(words).most_common(top_n)
```

**典型的な発見**:
- 特定のキーワードを含む記事が人気
- 専門用語の適度な使用が効果的
- トレンドワードの活用

## Detailed Analysis Examples

### 例1: タイトル長と人気度の関係
```python
import matplotlib.pyplot as plt

def title_length_correlation(articles):
    """タイトル長とスキ数の相関"""
    title_lengths = [len(a['title']) for a in articles]
    likes = [a['likes'] for a in articles]

    # 相関係数を計算
    correlation = calculate_correlation(title_lengths, likes)

    # 可視化（推奨）
    # plt.scatter(title_lengths, likes)
    # plt.xlabel('タイトル文字数')
    # plt.ylabel('スキ数')

    return correlation
```

### 例2: 文章量と人気度の関係
```python
def content_length_analysis(articles):
    """文章量の最適範囲を特定"""
    # スキ数で分類
    high_like = [a for a in articles if a['likes'] >= 100]
    medium_like = [a for a in articles if 20 <= a['likes'] < 100]
    low_like = [a for a in articles if a['likes'] < 20]

    # 各グループの平均文字数
    avg_lengths = {
        'high': sum(len(a['content']) for a in high_like) / len(high_like),
        'medium': sum(len(a['content']) for a in medium_like) / len(medium_like),
        'low': sum(len(a['content']) for a in low_like) / len(low_like),
    }

    return avg_lengths
```

### 例3: 見出し使用パターン
```python
def heading_pattern_analysis(articles):
    """見出しの使い方を分析"""
    high_performers = sorted(articles, key=lambda x: x['likes'], reverse=True)[:20]

    patterns = []
    for article in high_performers:
        headings = extract_headings(article['content'])
        patterns.append({
            'count': len(headings),
            'avg_heading_length': sum(len(h) for h in headings) / len(headings) if headings else 0,
            'first_heading_position': find_first_heading_position(article['content']),
        })

    return aggregate_patterns(patterns)
```

## Output Example

```markdown
# 人気記事の文章傾向分析レポート

## サマリー
100記事を分析した結果、人気記事には明確なパターンが存在。

## 主要な発見

### 1. タイトルの特徴
- **最適な長さ**: 18-25文字（平均スキ数が最も高い）
- **数字の使用**: 68%の人気記事がタイトルに数字を含む
- **具体性**: 抽象的なタイトルより具体的なタイトルが2.3倍のスキ数

**人気タイトルの例**:
- "Pythonで始めるデータ分析【3つのステップ】" (352スキ)
- "初心者でもわかる機械学習の基礎" (287スキ)
- "5分で理解できるSQL入門" (245スキ)

### 2. 文章量の最適範囲
- **高スキ記事**: 平均3,500文字（2,000-5,000文字の範囲）
- **低スキ記事**: 平均1,200文字または8,000文字以上
- **結論**: 適度なボリューム（2,000-5,000文字）が最適

### 3. 記事構造の特徴
人気記事の78%が以下の構造を持つ:
1. 導入（問題提起）
2. 3-5個の主要セクション（見出し付き）
3. まとめ/結論

**構造的特徴**:
- 見出し数: 平均5.2個
- リスト使用: 平均3.8箇所
- 明確なセクション分け: 必須

### 4. キーワードと表現
人気記事に頻出するキーワード Top 10:
1. "方法" (152回)
2. "ポイント" (128回)
3. "解説" (115回)
4. "初心者" (98回)
5. "実践" (87回)
...

**トーン**:
- 断定的な表現: 45%
- 読者に語りかける表現: 35%
- 控えめな表現: 20%

### 5. 読みやすさの指標
- **平均文長**: 40-60文字（句読点まで）
- **段落**: 3-5文ごとに改行
- **専門用語**: 適度な使用（全体の5-10%）

## 推奨事項

### 優先度: 高
1. **タイトルを最適化**
   - 18-25文字の範囲で具体的に
   - 数字を含める（例: "3つの方法"、"5分で"）
   - ターゲット読者を明示（例: "初心者向け"）

2. **明確な構造を作る**
   - 導入で問題提起
   - 3-5個の主要セクション
   - 各セクションに見出しを付ける
   - まとめで要点を再確認

3. **適切な文章量**
   - 2,000-5,000文字を目標
   - 薄すぎず、長すぎず
   - 価値のある情報を凝縮

### 優先度: 中
4. **リストと箇条書きを活用**
   - 要点は箇条書きで
   - ステップは番号付きリストで
   - 視覚的に読みやすく

5. **読者に語りかける文体**
   - "〜です"、"〜ます" 調
   - 読者の疑問を先回りして解決
   - 具体例を豊富に

6. **適度な専門性**
   - 専門用語は必要に応じて使用
   - 初出時は説明を加える
   - 初心者にも理解できる表現

## 成功パターンのチェックリスト
- [ ] タイトルに数字が含まれている
- [ ] タイトルが18-25文字
- [ ] 明確な見出し構造（3個以上）
- [ ] 文章量が2,000-5,000文字
- [ ] リストや箇条書きを使用
- [ ] 導入で問題提起している
- [ ] まとめ/結論がある
- [ ] 具体例が含まれている
- [ ] 読みやすい文長（40-60文字）
- [ ] 適度に段落分けされている
```

## Advanced Analysis Techniques

### TF-IDF分析
```python
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_analysis(articles):
    """TF-IDFでキーワード重要度を分析"""
    texts = [a['content'] for a in articles]

    vectorizer = TfidfVectorizer(max_features=50)
    tfidf_matrix = vectorizer.fit_transform(texts)

    # 重要キーワード抽出
    feature_names = vectorizer.get_feature_names_out()

    return feature_names
```

### トピックモデリング（LDA）
```python
from sklearn.decomposition import LatentDirichletAllocation

def topic_modeling(articles, n_topics=5):
    """潜在的なトピックを抽出"""
    # TF-IDF特徴量の取得
    # LDAモデルの学習
    # トピック別の代表語を抽出
    pass
```

### 感情分析
```python
def sentiment_analysis(text):
    """ポジティブ/ネガティブ分析"""
    positive_words = ['成功', '良い', '素晴らしい', '効果的', ...]
    negative_words = ['失敗', '悪い', '問題', '困難', ...]

    pos_count = sum(1 for word in positive_words if word in text)
    neg_count = sum(1 for word in negative_words if word in text)

    return {
        'positive_ratio': pos_count / (pos_count + neg_count) if (pos_count + neg_count) > 0 else 0,
        'tone': 'positive' if pos_count > neg_count else 'negative'
    }
```

## Validation Checklist

分析実行時の確認:
- [ ] 十分なサンプルサイズ（30記事以上）
- [ ] 人気記事と一般記事を比較
- [ ] 複数の指標で多角的に分析
- [ ] 統計的な裏付けがある
- [ ] 実行可能な推奨事項を含む

## Troubleshooting

### 形態素解析エラー
```bash
# MeCabのインストール
pip install mecab-python3
# または
pip install janome
```

### パフォーマンス問題
- 大量データはサンプリング
- 並列処理の活用
- キャッシュの利用

### 分析結果が不明確
- サンプルサイズを増やす
- セグメント分析（タグ別、期間別）
- 可視化で傾向を確認
