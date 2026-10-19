"""iPhone ショートカット（jobcan-punch.shortcut）を生成する。

トークンは埋め込まず、読み込み時に入力してもらう。API の URL と Slack の user_id は
--url / --user-id で埋め込める（指定しなければ読み込み時に入力してもらう）。
生成したファイルは macOS で署名してから iPhone に読み込む:
    shortcuts sign --mode people-who-know-me --input jobcan-punch.shortcut --output jobcan-punch-signed.shortcut

使い方:
    python scripts/build_shortcut.py                    # shortcut/jobcan-punch.shortcut（実行時に種類を選ぶ）
    python scripts/build_shortcut.py --per-work-type \
        --user-id U0123456789 --url https://…/dev/shortcut/punch --out-dir /tmp/out   # 出勤.shortcut など
"""

import argparse
import os
import plistlib
import sys
import uuid

WORK_TYPES = ["出勤", "退勤", "外出", "再入", "出社", "退社"]
OBJ = "￼"


def text(string: str, attachments: dict | None = None) -> dict:
    return {
        "Value": {"string": string, "attachmentsByRange": attachments or {}},
        "WFSerializationType": "WFTextTokenString",
    }


def action_output(output_uuid: str, name: str) -> dict:
    return {"OutputUUID": output_uuid, "OutputName": name, "Type": "ActionOutput"}


def variable(name: str) -> dict:
    return {"VariableName": name, "Type": "Variable"}


def attachment(value: dict) -> dict:
    return {"Value": value, "WFSerializationType": "WFTextTokenAttachment"}


def dictionary(items: list[tuple[str, dict]]) -> dict:
    return {
        "Value": {
            "WFDictionaryFieldValueItems": [
                {"WFItemType": 0, "WFKey": text(key), "WFValue": value}
                for key, value in items
            ]
        },
        "WFSerializationType": "WFDictionaryFieldValue",
    }


def action(identifier: str, **params) -> dict:
    return {"WFWorkflowActionIdentifier": identifier, "WFWorkflowActionParameters": params}


def build(work_type: str | None = None, user_id: str = "", url: str = "") -> dict:
    """work_type を渡すとその打刻だけを行い、渡さないと実行時に種類を選ぶ。

    user_id・url を渡すとファイルに埋め込み、渡さないと読み込み時に入力してもらう。
    トークンは常に読み込み時に入力してもらう。
    """
    user_id_id, token_id, list_id, chosen_id, response_id, message_id = (
        str(uuid.uuid4()).upper() for _ in range(6)
    )
    actions = []
    import_questions = []

    def ask(text_: str, parameter_key: str, default: str = ""):
        import_questions.append(
            {"ActionIndex": len(actions) - 1, "Category": "Parameter", "ParameterKey": parameter_key,
             "DefaultValue": default, "Text": text_}
        )

    # 読み込み時に入力してもらう値（または埋め込んだ値）を変数に入れる
    actions.append(action("is.workflow.actions.gettext", WFTextActionText=text(user_id), UUID=user_id_id))
    if not user_id:
        ask("Slack の user_id（U から始まる ID）", "WFTextActionText")
    actions.append(
        action(
            "is.workflow.actions.setvariable",
            WFInput=attachment(action_output(user_id_id, "テキスト")),
            WFVariableName="user_id",
        )
    )
    actions.append(action("is.workflow.actions.gettext", WFTextActionText=text(""), UUID=token_id))
    ask("ショートカット用トークン（Bitwarden の JOBCAN_SHORTCUT_TOKEN）", "WFTextActionText")
    actions.append(
        action(
            "is.workflow.actions.setvariable",
            WFInput=attachment(action_output(token_id, "テキスト")),
            WFVariableName="token",
        )
    )

    # 打刻の種類（固定か、実行時に選ぶ）
    if work_type:
        work_type_value = text(work_type)
    else:
        actions.append(
            action(
                "is.workflow.actions.list",
                WFItems=[{"WFItemType": 0, "WFValue": text(w)} for w in WORK_TYPES],
                UUID=list_id,
            )
        )
        actions.append(
            action(
                "is.workflow.actions.choosefromlist",
                WFInput=attachment(action_output(list_id, "リスト")),
                WFChooseFromListActionPrompt="打刻",
                UUID=chosen_id,
            )
        )
        work_type_value = text(OBJ, {"{0, 1}": action_output(chosen_id, "選択された項目")})

    # API を呼ぶ
    actions.append(
        action(
            "is.workflow.actions.downloadurl",
            WFURL=url,
            WFHTTPMethod="POST",
            ShowHeaders=True,
            WFHTTPHeaders=dictionary(
                [("Authorization", text(f"Bearer {OBJ}", {"{7, 1}": variable("token")}))]
            ),
            WFHTTPBodyType="JSON",
            WFJSONValues=dictionary(
                [
                    ("user_id", text(OBJ, {"{0, 1}": variable("user_id")})),
                    ("work_type", work_type_value),
                ]
            ),
            UUID=response_id,
        )
    )
    if not url:
        ask("API の URL（…/dev/shortcut/punch）", "WFURL", "https://")

    # 結果を通知する
    actions.append(
        action(
            "is.workflow.actions.getvalueforkey",
            WFInput=attachment(action_output(response_id, "URLの内容")),
            WFDictionaryKey="message",
            UUID=message_id,
        )
    )
    actions.append(
        action(
            "is.workflow.actions.notification",
            WFNotificationActionTitle="JOBCAN",
            WFNotificationActionBody=text(OBJ, {"{0, 1}": action_output(message_id, "辞書の値")}),
        )
    )

    return {
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowClientVersion": "2607.0.2",
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowHasShortcutInputVariables": False,
        "WFWorkflowIcon": {"WFWorkflowIconStartColor": 4292093695, "WFWorkflowIconGlyphNumber": 59511},
        "WFWorkflowTypes": [],
        "WFQuickActionSurfaces": [],
        "WFWorkflowInputContentItemClasses": [],
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowImportQuestions": import_questions,
        "WFWorkflowActions": actions,
    }


def write(path: str, workflow: dict):
    with open(path, "wb") as f:
        plistlib.dump(workflow, f, fmt=plistlib.FMT_XML)
    print(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "shortcut"))
    parser.add_argument("--per-work-type", action="store_true", help="打刻の種類ごとのファイル（出勤.shortcut など）も作る")
    parser.add_argument("--user-id", default="", help="埋め込む Slack の user_id")
    parser.add_argument("--url", default="", help="埋め込む API の URL")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    write(os.path.join(args.out_dir, "jobcan-punch.shortcut"), build(user_id=args.user_id, url=args.url))
    if args.per_work_type:
        for w in WORK_TYPES:
            write(os.path.join(args.out_dir, f"{w}.shortcut"), build(w, args.user_id, args.url))


if __name__ == "__main__":
    main()
