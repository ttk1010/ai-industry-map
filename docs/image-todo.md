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

## 解決済み: ツール・クラウドは「マスコット」か「実ロゴ」か → 実ロゴで決着

(2026-07-20 追記) [Simple Icons](https://simpleicons.org/)（CC0）から公式ロゴSVGを取得し、
`data/characters.yaml` の `logo_path` として全18エンティティに配線した。カスタムマスコットの
有無に関わらず、バッジの右下に小さくロゴが乗る（`badge_icon()` / `.badge-logo` CSS参照）。

- モデル/開発環境/チャット（マスコットあり）: マスコットが主役、ロゴは隅の小さな確認バッジ
- ツール・サービス／クラウド（マスコットなし）: 色付きイニシャル＋ロゴバッジで、元イラストの
  「実ロゴのまま」という表現に近い状態に。**この7社分はAI画像生成が無くても見た目として完成**
  している。マスコット化したくなったら後からキャラクターを追加すればよい（任意）。

取得済みロゴ一覧（`assets/logos/<slug>.svg`）: claude-model, gpt-model, gemini-model,
llama-model, deepseek-model, claude-code-devtool, codex-devtool, cursor-devtool,
claude-chat, chatgpt-chat, gemini-chat, github, notion, slack, google-drive, aws, azure,
google-cloud（出典は`references/SOURCES.md`）。
