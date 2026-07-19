# 画像生成TODO

まだAI生成イラストが無い要素の一覧。上から順に着手する想定（優先度順）。
プロンプトは `data/characters.yaml` / `data/areas.yaml` / `data/world.yaml`
が正（このファイルは作業用のコピー）。生成できたら該当パスに保存し、

```bash
cd ai-industry-map
uv run --with pyyaml python3 scripts/build_slides.py
```

を実行してスライドに反映する。

## 進め方の基本

1. 対象の `prompt`（無ければ後述の「要クロップ」を先に）をChatGPT (GPT Image 2)に貼る
2. 生成結果を `image_path` / `background_path` に保存
3. `generated_with` に生成日・会話リンクなどをメモしておくと後で追える
4. リビルドして確認

---

## 優先度1: AIモデル・開発環境の背景（すでにプロンプトあり・エリアが一番充実している）

| エリア | 保存先 | 状態 |
|---|---|---|
| 全体像（世界地図） | `assets/backgrounds/overview.png` | プロンプトあり (`data/world.yaml`) |
| ①AIモデル（AI頭脳学園） | `assets/backgrounds/models.png` | プロンプトあり (`data/areas.yaml`) |
| ③開発環境（AI開発者タウン） | `assets/backgrounds/devtools.png` | プロンプトあり (`data/areas.yaml`) |

## 優先度2: AIモデルの残りキャラクター（クロップ・プロンプトあり、生成のみ）

| キャラクター | 保存先 | クロップ | 備考 |
|---|---|---|---|
| GPT | `assets/characters/models/gpt.png` | `references/model-gpt-source-crop.png` | 杖の先を星→光の粒に変更する指示込み |
| Gemini | `assets/characters/models/gemini.png` | `references/model-gemini-source-crop.png` | 虫眼鏡を外し双子の星を追加する指示込み |
| Llama | `assets/characters/models/llama.png` | `references/model-llama-source-crop.png` | クロップの色(#BBA9D6)に合わせて`brand_color`を修正済み |

## 優先度3: 開発環境のキャラクター（クロップ未取得）

`イメージ画像/ChatGPT_3_AI開発者タウン.png` から切り抜きが必要。プロンプトも未作成（クロップ確認後に作成する）。

| キャラクター | 保存先 | 元イラストでの見た目（参考） |
|---|---|---|
| Claude Code | `assets/characters/devtools/claude-code.png` | 眼鏡をかけた工房の職人風キャラ |
| Codex | `assets/characters/devtools/codex.png` | 白いロボット |
| Cursor | `assets/characters/devtools/cursor.png` | ヘッドホンをした黒猫風キャラ |

## 優先度4: 残りの背景（プロンプトあり・エリアはまだ薄い）

| エリア | 保存先 |
|---|---|
| ②チャットアシスタント（AIおしゃべり広場） | `assets/backgrounds/chat.png` |
| ④ツール・サービス（MCP港） | `assets/backgrounds/tools.png` |
| ⑤クラウド（クラウド王国） | `assets/backgrounds/cloud.png` |

## 優先度5: チャットアシスタントのキャラクター（クロップ未取得・プロンプト未作成）

`イメージ画像/ChatGPT_2_AIおしゃべり広場.png`（未確認）から切り抜きが必要。

| キャラクター | 保存先 |
|---|---|
| Claude (チャット) | `assets/characters/chat/claude-chat.png` |
| ChatGPT | `assets/characters/chat/chatgpt-chat.png` |
| Gemini (チャット) | `assets/characters/chat/gemini-chat.png` |

## 優先度6: AIモデルの残り2体（クロップ未取得）

| キャラクター | 保存先 |
|---|---|
| DeepSeek | `assets/characters/models/deepseek.png` |

## 未解決の設計課題: ツール・クラウドは「マスコット」か「実ロゴ」か

`ツール・サービス`（GitHub/Notion/Slack/Google Drive）と`クラウド`（AWS/Azure/Google Cloud）は、
元イラストでは他エリアと違い、キャラクター化せず**実際のサービスロゴのアイコン**として描かれている
（作業員の動物キャラは1〜2体だけ、道具箱自体はロゴのまま）。

このプロジェクトでも同じ方針で行くなら、この7社分は**AI画像生成が不要**（公式ロゴ素材を
使うだけ）になる。逆に他エリアと統一感を出すためにマスコット化するなら、7体分のプロンプトを
新規に考える必要がある。この方針は次回相談してから決める。

| 対象 | 保存先候補 | 備考 |
|---|---|---|
| GitHub | `assets/characters/tools/github.png` | 方針未決定 |
| Notion | `assets/characters/tools/notion.png` | 方針未決定 |
| Slack | `assets/characters/tools/slack.png` | 方針未決定 |
| Google Drive | `assets/characters/tools/google-drive.png` | 方針未決定 |
| AWS | `assets/characters/cloud/aws.png` | 方針未決定 |
| Azure | `assets/characters/cloud/azure.png` | 方針未決定 |
| Google Cloud | `assets/characters/cloud/google-cloud.png` | 方針未決定 |
