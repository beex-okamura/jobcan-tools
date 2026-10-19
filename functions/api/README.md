# api

## iPhone ショートカットから打刻する

`POST /shortcut/punch` で、Slack と同じ打刻処理（SQS → JOBCAN 打刻、Slack ステータス更新、
`send_punch_channels` への投稿）を受けつけます。処理結果はボットからの DM に届きます。

### 準備（初回のみ）

1. Secrets Manager の `jobcan-<stage>-secrets` に `SHORTCUT_SIGNING_SECRET` を追加する
   （例: `openssl rand -hex 32` で作ったランダム文字列）。
2. 自分の Slack user_id（`U...`）用のトークンを発行する。

   ```sh
   SECRETS_KEY_NAME=jobcan-dev-secrets python scripts/issue_shortcut_token.py U0123456789
   ```

   `SHORTCUT_SIGNING_SECRET` を変えると、発行済みのトークンはすべて無効になります。

### ショートカットの作り方

1. 「メニューから選択」で 出勤 / 退勤 / 外出 / 再入 / 出社 / 退社 を並べる
   （各項目で「テキスト」に同じ語を入れる）。
2. 「URLの内容を取得」を追加し、次のように設定する。
   - URL: `https://<API Gateway のエンドポイント>/<stage>/shortcut/punch`
   - 方法: `POST`
   - ヘッダ: `Authorization` = `Bearer <発行したトークン>`
   - 本文を要求: JSON
     - `user_id`（テキスト）: `U0123456789`
     - `work_type`（テキスト）: 手順 1 の「選択された項目」
3. 「辞書の値を取得」で `message` を取り出し、「通知を表示」で表示する。

`work_type` は「出勤」などの表示名か、`clock_in` / `clock_out` / `go_out` / `returned` /
`go_office_in` / `leave_office_in` のキーで指定できます。
出勤用・退勤用のショートカットを別々に作れば、ホーム画面や背面タップ、
「オートメーション」（例: 会社に着いたら出社）からも呼べます。

| ステータス | 意味 |
| --- | --- |
| 200 | 受けつけた（`{"message": "出勤 処理を受けつけました"}`） |
| 400 | `work_type` が不正 |
| 401 | トークンが不正 |
| 404 | user_id が未登録 |
| 503 | `SHORTCUT_SIGNING_SECRET` が未設定 |

### ショートカットファイルを読み込む

手で組み立てる代わりに `shortcut/jobcan-punch.shortcut` を使えます
（`python scripts/build_shortcut.py` で再生成できます）。
iOS は署名のないショートカットを読み込めないので、macOS で署名してから iPhone に送ります。

```sh
shortcuts sign --mode people-who-know-me --input shortcut/jobcan-punch.shortcut --output jobcan-punch-signed.shortcut
```

`--mode anyone` は Apple のサーバーが `NSURLErrorDomain error 500` を返して失敗することがあります。
`people-who-know-me` で署名したファイルは、自分と連絡先に入っている人だけが読み込めます。

署名で「正しい形式ではない」と出たら、まず `plutil -lint shortcut/jobcan-punch.shortcut` で
ファイルが壊れていないか確認してください。

読み込むときに Slack の user_id、トークン、API の URL を聞かれます。
値はファイルには入らず、iPhone のショートカットにだけ保存されます。
