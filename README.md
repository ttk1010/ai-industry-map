# AIの世界マップ

AI業界（モデル・チャット・開発環境・ツール・クラウド）を俯瞰するスライド兼
サイト。16:9のページを「全体像 → エリア → 個別プロダクト」とドリルダウン
しながら見られる。各エリアは「AI頭脳学園」「AIおしゃべり広場」のような
世界観の名前が主役で、機能的な分類名（AIモデル、等）は添え書き程度。

`ai-second-brain` には依存しない独立プロジェクト。Vault（`../Vault`）の
News/Comparisons/Concepts ノートは読み取り専用の参照先として使う
（`data/characters.yaml` の `source_notes` に手動で記録する）。

**2系統の成果物を分けて持っている:**
- `slides/index.html` — Claude Codeで作ったHTML/CSSのサイト兼スライド（完成版）
- `claude-design/` — Claude Designでよりデザイン性の高いスライドを作る取り組み
  （進行中。`claude-design/brief.md` 参照）

## 構成

```
data/
  world.yaml          全体タイトル・タグライン・世界地図の背景
  areas.yaml           エリア定義（世界観の名前・機能名・背景プロンプト）
  characters.yaml       プロダクトごとの定義・キャラクター生成プロンプト
  comparisons.yaml      比較表（Vaultの比較ノートを転記）
assets/
  css/deck.css         16:9レターボックス表示とページ共通スタイル
  js/deck.js           パンくず・前へ/次へ・クリック遷移・全画面のロジック
  characters/          ChatGPT(GPT Image 2)で生成したキャラクター画像
  logos/               企業/サービスの公式ロゴ（Simple Icons由来）
  backgrounds/         エリアごとの背景イラスト
scripts/
  build_slides.py      yamlを読んで slides/index.html を生成
slides/
  index.html           生成された成果物（直接ブラウザで開ける）
references/            デザイン参考資料・キャラクターの元イラスト切り抜き
docs/
  image-todo.md        まだ画像生成できていない要素のTODOリスト
claude-design/
  brief.md             Claude Design用のブリーフ（コピペして使う）
```

## キャラクター画像・ロゴの仕組み

- **キャラクター**（`assets/characters/`）: `characters.yaml` の該当エントリの
  `prompt` をChatGPT（GPT Image 2、無料枠）に貼って生成し、`image_path` に保存。
  無い項目はブランドカラー＋頭文字のプレースホルダーで表示される
- **ロゴ**（`assets/logos/`）: Simple Icons（CC0）から取得済み。キャラクターが
  ある場合はバッジの右下に小さく重ねて表示（自作キャラクターと公式ロゴの共存）
- 生成/取得できたら以下でリビルド:

```bash
cd ai-industry-map
uv run --with pyyaml python3 scripts/build_slides.py
```

`characters.yaml` / `areas.yaml` を編集したら（バージョン更新、キャラクター
画像追加など）このコマンドを再実行する。今のところ自動更新はせず、手動
トリガーのみ。

## 動作確認（ローカルプレビュー）

`slides/index.html` は相対パスでCSS/JSを読むため、`file://` で直接開くと
一部ブラウザでは正しく動かないことがある。簡易サーバーで見るのが確実:

```bash
cd ai-industry-map
python3 -m http.server 8765
# http://127.0.0.1:8765/slides/index.html を開く
```

## 未対応・今後の課題

- 背景イラスト・一部キャラクター画像がまだプレースホルダー（`docs/image-todo.md` 参照）
- `claude-design/` でのスライド制作（進行中）
- Vaultのコンテンツ拡充（比較ノートの軸をLlama/DeepSeekまで広げるか等）
