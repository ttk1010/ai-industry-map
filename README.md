# AI業界地図

AI業界（モデル・開発環境など）を俯瞰するスライド兼サイト。16:9のページを
「全体像 → エリア → 個別プロダクト」とドリルダウンしながら見られる。

`ai-second-brain` には依存しない独立プロジェクト。Vault（`../Vault`）の
News/Comparisons/Concepts ノートは読み取り専用の参照先として使う
（`data/characters.yaml` の `source_notes` に手動で記録する）。

## 構成

```
data/
  areas.yaml        エリア定義（①モデル ②開発環境 …）
  characters.yaml    プロダクトごとの定義・現在のステータス・生成プロンプト
assets/
  css/deck.css       16:9レターボックス表示とページ共通スタイル
  js/deck.js         パンくず・前へ/次へ・クリック遷移・全画面のロジック
  characters/        ChatGPT(GPT Image 2)で生成したキャラクター画像の保存先
scripts/
  build_slides.py    yamlを読んで slides/index.html を生成
slides/
  index.html         生成された成果物（直接ブラウザで開ける）
```

## キャラクター画像の追加フロー

1. `data/characters.yaml` の該当エントリの `prompt` をコピーする
2. ChatGPT（GPT Image 2、無料枠）に貼って画像を生成する
3. 生成された画像を `image_path` に書かれたパス（例:
   `assets/characters/models/claude.png`）に保存する
4. 再生成する（下記）— 画像がある項目は自動でそれを使い、無い項目は
   ブランドカラー＋頭文字のプレースホルダーのまま表示される
5. 気に入らなければ `prompt` を調整して 2〜4 をやり直す

`generated_with` フィールドに生成日などのメモを残しておくと、後で
「いつ・どのプロンプトで作ったか」を追える。

## スライドの再生成

```bash
cd ai-industry-map
uv run --with pyyaml python3 scripts/build_slides.py
```

`characters.yaml` / `areas.yaml` を編集したら（バージョン更新、ステータス
変更、キャラクター画像追加など）このコマンドを再実行する。今のところ
自動更新はせず、手動トリガーのみ。

## 動作確認（ローカルプレビュー）

`slides/index.html` は相対パスでCSS/JSを読むため、`file://` で直接開くと
一部ブラウザでは正しく動かないことがある。簡易サーバーで見るのが確実:

```bash
cd ai-industry-map
python3 -m http.server 8765
# http://127.0.0.1:8765/slides/index.html を開く
```

## 未対応・今後の課題

- ビジュアルの全体的なテイスト（今は仮の配色）は要検討
- ②チャットアシスタント／④ツール／⑤クラウドなど、他エリアの追加
- Vaultのコンテンツ拡充（例: Geminiの Concept ノートがまだ無い）
- News ノートとステータス（updated/stable/watch）の連携を半自動化するか検討
