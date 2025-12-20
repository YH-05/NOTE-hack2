---
name: data-versioning
description: Manage version control for scraped data and analysis results using Git. Use when user wants to track data changes, create snapshots, compare versions, or maintain data history. Ensures data integrity and enables rollback.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__git__*, mcp__filesystem__*, mcp__time__*
---

# Data Versioning Skill

収集データと分析結果をGitでバージョン管理するスキル

## When to Use This Skill

このスキルは以下の場合に自動的に起動します:
- データ収集後にバージョン管理したい時
- データの変更履歴を追跡したい時
- 過去のデータと比較したい時
- データのスナップショットを保存したい時
- チーム間でデータを共有したい時
- データのロールバックが必要な時

## Instructions

### 1. データディレクトリの準備

#### MCPファイルシステムツールで構造を確認
```
mcp__filesystem__directory_tree でディレクトリ構造を確認
- path: "."
- excludePatterns: ["node_modules", ".git", "__pycache__"]

mcp__filesystem__list_directory_with_sizes でデータファイルを確認
- path: "data/raw"
- sortBy: "size"
```

#### ディレクトリ構造の推奨
```
data/
├── raw/           # 生データ（スクレイピング結果）
├── processed/     # 加工済みデータ
└── exports/       # エクスポート結果
```

### 2. Gitリポジトリの状態確認

#### MCP Gitツールを使用
```
mcp__git__git_status でGit状態を確認
- repo_path: "."

mcp__git__git_log で最近のコミット履歴を確認
- repo_path: "."
- max_count: 10
- start_timestamp: "1 week ago"  # オプション

mcp__git__git_branch でブランチを確認
- repo_path: "."
- branch_type: "local"
```

### 3. データファイルのステージング

#### MCP Gitツールでファイルを追加
```
mcp__git__git_add で新しいデータファイルをステージング
- repo_path: "."
- files: [
    "data/raw/articles_tag_python_20241220.json",
    "data/processed/analysis_20241220.json"
  ]

または、特定ディレクトリ全体を追加
- files: ["data/raw/"]
```

### 4. データのコミット

#### MCP Gitツールでコミット
```
mcp__git__git_commit でコミットを作成
- repo_path: "."
- message: 適切なコミットメッセージ

例: スクレイピングデータのコミット
- message: "Add scraped articles for #Python tag (120 articles, 2024-12-20)"

例: 分析結果のコミット
- message: "Add trend analysis results (2024-12 dataset)"
```

#### コミットメッセージのベストプラクティス
```
[データ種別] 簡潔な説明 (詳細情報)

例:
- "[Scrape] Add articles for #Python tag (120 articles, 2024-12-20)"
- "[Analysis] Monthly trend analysis (Dec 2024)"
- "[Export] CSV export for client report (150 articles)"
- "[Update] Re-scrape articles with corrected selectors"
- "[Fix] Correct duplicate entries in dataset"
```

### 5. データのバージョン比較

#### MCP Gitツールで差分を確認
```
mcp__git__git_diff_unstaged で未ステージングの変更を確認
- repo_path: "."
- context_lines: 3  # 前後の行数

mcp__git__git_diff_staged でステージングされた変更を確認
- repo_path: "."

mcp__git__git_diff で特定のブランチやコミット間の差分を確認
- repo_path: "."
- target: "main" または "commit_hash"
```

#### 特定コミットの内容確認
```
mcp__git__git_show で特定コミットの詳細を表示
- repo_path: "."
- revision: "commit_hash" または "HEAD"
```

### 6. データバージョンの管理

#### ブランチを使用したバージョン管理
```
mcp__git__git_create_branch で新しいブランチを作成
- repo_path: "."
- branch_name: "data/december-2024"
- base_branch: "main"  # オプション

mcp__git__git_checkout でブランチを切り替え
- repo_path: "."
- branch_name: "data/december-2024"
```

#### タグを使用したスナップショット（Bashツールを使用）
```bash
# 重要なデータスナップショットにタグを付ける
git tag -a v2024.12 -m "December 2024 dataset snapshot"
git tag -l  # タグ一覧を表示
```

### 7. データの時系列管理

#### MCP Timeツールでタイムスタンプを取得
```
mcp__time__get_current_time で正確なタイムスタンプを取得
- timezone: "Asia/Tokyo"

タイムスタンプをファイル名やコミットメッセージに使用:
- articles_tag_python_20241220_153045.json
- "[Scrape] Python tag articles (2024-12-20 15:30:45 JST)"
```

## Best Practices

### データファイルのバージョン管理
- **定期的なコミット**: データ収集後は必ずコミット
- **明確なメッセージ**: 何を、いつ、どのように収集したか明記
- **適切な粒度**: 1つのスクレイピングセッション = 1コミット
- **大容量ファイル**: Git LFSの使用を検討（100MB以上）

### コミットのタイミング
- ✅ スクレイピング完了直後
- ✅ データ加工・クリーニング後
- ✅ 分析結果の生成後
- ✅ エクスポート実行後
- ❌ 作業途中（中途半端な状態）

### ブランチ戦略
- `main`: 安定版データ
- `data/YYYY-MM`: 月別データブランチ
- `analysis/topic-name`: 特定分析用ブランチ
- `experimental`: 実験的なデータ収集

### .gitignore設定
除外すべきファイル:
```
# 一時ファイル
*.tmp
*.log
.DS_Store

# 大容量データ（Git LFS使用推奨）
*.zip
*.tar.gz

# 環境依存ファイル
.env
credentials.json

# キャッシュ
__pycache__/
.pytest_cache/
```

## Common Use Cases

### Case 1: 日次データ収集のバージョン管理
```
ワークフロー:
1. 毎日のスクレイピング実行
   - python src/note_scraper.py --tag python

2. データファイルの確認
   - mcp__filesystem__list_directory で生成ファイルを確認

3. Git追加とコミット
   - mcp__git__git_add
   - mcp__git__git_commit
     message: "[Daily] Python tag articles (2024-12-20, 15 new articles)"

4. 週次でブランチをマージ
   - git merge data/week-51
```

### Case 2: 月次分析結果の管理
```
ワークフロー:
1. 月次分析ブランチを作成
   - mcp__git__git_create_branch
     branch_name: "analysis/december-2024"

2. 分析実行と結果保存
   - データ分析実行
   - 結果をdata/processed/に保存

3. コミット
   - mcp__git__git_add
     files: ["data/processed/monthly_analysis_202412.json"]
   - mcp__git__git_commit
     message: "[Analysis] December 2024 monthly trend analysis"

4. タグ付け（重要なマイルストーン）
   - git tag -a monthly-202412 -m "December 2024 analysis snapshot"
```

### Case 3: データの比較（前月との差分）
```
ワークフロー:
1. 現在のブランチで最新データをコミット

2. 前月のデータを確認
   - mcp__git__git_log で前月のコミットハッシュを特定
   - mcp__git__git_show でコミット内容を確認

3. 差分を確認
   - mcp__git__git_diff
     target: "commit_hash_november"

4. 変化を分析
   - 記事数の増減
   - 新しいタグの出現
   - トレンドの変化
```

### Case 4: データのロールバック
```
シナリオ: 誤ったデータを収集してしまった

1. Git履歴を確認
   - mcp__git__git_log

2. 正しい状態のコミットを特定

3. ロールバック（Bashツールを使用）
   - git checkout <commit_hash> -- data/raw/problem_file.json

4. 修正をコミット
   - mcp__git__git_add
   - mcp__git__git_commit
     message: "[Fix] Revert incorrect scraping data"
```

## Advanced Workflows

### Workflow 1: 実験的データ収集
```
1. 実験ブランチを作成
   - mcp__git__git_create_branch
     branch_name: "experiment/new-scraping-method"

2. 実験的スクレイピング実行

3. 結果を検証

4. 成功した場合はmainにマージ、失敗したらブランチ削除
```

### Workflow 2: データの定期スナップショット
```
毎月1日に実行:
1. 現在のデータ状態を確認
   - mcp__git__git_status

2. すべての変更をコミット

3. 月次タグを作成
   - git tag -a snapshot-YYYYMM -m "Monthly snapshot"

4. タグをリモートにプッシュ（オプション）
   - git push origin --tags
```

### Workflow 3: チーム間でのデータ共有
```
1. データを収集してコミット

2. リモートリポジトリにプッシュ（Bashツールを使用）
   - git push origin main

3. チームメンバーがプル
   - git pull origin main

4. 競合が発生した場合は手動で解決
```

## Validation Checklist

データをコミットする前の確認:
- [ ] データファイルが正しい場所に保存されている
- [ ] ファイル名に日付やタイムスタンプが含まれている
- [ ] JSONファイルの構造が正しい
- [ ] 機密情報が含まれていない
- [ ] .gitignoreが適切に設定されている
- [ ] コミットメッセージが明確で詳細
- [ ] 大容量ファイル（100MB以上）はGit LFSを使用

## Git Commands Reference (MCP)

### 基本操作
```
mcp__git__git_status        # 状態確認
mcp__git__git_add          # ステージング
mcp__git__git_commit       # コミット
mcp__git__git_log          # 履歴表示
```

### 差分確認
```
mcp__git__git_diff_unstaged  # 未ステージングの差分
mcp__git__git_diff_staged    # ステージング済みの差分
mcp__git__git_diff           # ブランチ/コミット間の差分
mcp__git__git_show           # 特定コミットの詳細
```

### ブランチ操作
```
mcp__git__git_branch         # ブランチ一覧
mcp__git__git_create_branch  # ブランチ作成
mcp__git__git_checkout       # ブランチ切り替え
```

### その他（Bashツール使用）
```bash
git reset                    # ステージング取り消し
git tag                      # タグ管理
git push/pull               # リモート同期
git merge                   # マージ
```

## Troubleshooting

### ファイルが大きすぎる
```
問題: 100MB以上のデータファイルをコミットしようとしている

解決策:
1. Git LFSをインストール
   - git lfs install

2. 大容量ファイルをトラッキング
   - git lfs track "*.json"

3. .gitattributesがコミットされていることを確認
```

### コミットメッセージを間違えた
```
問題: コミット直後にメッセージの誤りに気づいた

解決策:
# 最新のコミットメッセージを修正（Bashツール使用）
git commit --amend -m "正しいメッセージ"

注意: すでにpushした場合は慎重に
```

### 誤ったファイルをコミット
```
問題: 機密情報を含むファイルをコミットしてしまった

解決策:
1. ファイルをGit履歴から削除（Bashツール使用）
   - git rm --cached sensitive_file.json

2. .gitignoreに追加

3. 新しいコミットを作成
   - mcp__git__git_commit
     message: "[Security] Remove sensitive data file"
```

### 競合の解決
```
問題: チームメンバーとデータファイルが競合

解決策:
1. 競合ファイルを確認
   - mcp__git__git_status

2. 手動で競合を解決（ファイルを編集）

3. 解決済みとしてマーク
   - mcp__git__git_add

4. マージコミット
   - mcp__git__git_commit
     message: "Merge conflict resolution for data files"
```

## Integration with Other Skills

### note-scraperとの連携
```
スクレイピング後、自動的にバージョン管理:

1. note-scraperスキルでデータ収集
2. data-versioningスキルに切り替え
3. 収集データをコミット
```

### data-analyzerとの連携
```
分析結果のバージョン管理:

1. data-analyzerスキルで分析実行
2. 結果をdata/processed/に保存
3. data-versioningスキルでコミット
4. タグ付けしてスナップショット保存
```

### data-exportとの連携
```
エクスポート結果の管理:

1. data-exportスキルでCSV/Excel作成
2. exports/ディレクトリに保存
3. data-versioningスキルでコミット
4. クライアントへの提出履歴を記録
```

## Output Example

```bash
# Git履歴の例

commit a1b2c3d (HEAD -> main)
Author: User <user@example.com>
Date:   2024-12-20 15:30:00 +0900

    [Scrape] Python tag articles (120 articles, 2024-12-20)

    - Collected 120 articles from #Python tag
    - Date range: 2024-12-01 to 2024-12-20
    - Min likes: 10
    - File: data/raw/articles_tag_python_20241220.json

commit e4f5g6h
Author: User <user@example.com>
Date:   2024-12-19 10:00:00 +0900

    [Analysis] December 2024 trend analysis

    - Analyzed 500 articles
    - Top tags: Python, JavaScript, ビジネス
    - File: data/processed/analysis_202412.json

commit i7j8k9l
Author: User <user@example.com>
Date:   2024-12-18 16:45:00 +0900

    [Export] CSV export for monthly report

    - Exported 500 articles to CSV
    - Format: UTF-8 with BOM
    - File: exports/articles_202412.csv
```
