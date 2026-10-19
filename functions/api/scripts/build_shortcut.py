"""iPhone ショートカット（jobcan-punch.shortcut）を生成する。

API の URL・Slack の user_id・トークンは埋め込まず、読み込み時に入力してもらう。
生成したファイルは macOS で署名してから iPhone に読み込む:
    shortcuts sign --mode people-who-know-me --input jobcan-punch.shortcut --output jobcan-punch-signed.shortcut

使い方:
    python scripts/build_shortcut.py [出力先]
"""

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


def build() -> dict:
    user_id_id, token_id, list_id, chosen_id, response_id, message_id = (
        str(uuid.uuid4()).upper() for _ in range(6)
    )

    actions = [
        # 0-3: 読み込み時に入力してもらう値を変数に入れる
        action("is.workflow.actions.gettext", WFTextActionText=text(""), UUID=user_id_id),
        action(
            "is.workflow.actions.setvariable",
            WFInput=attachment(action_output(user_id_id, "テキスト")),
            WFVariableName="user_id",
        ),
        action("is.workflow.actions.gettext", WFTextActionText=text(""), UUID=token_id),
        action(
            "is.workflow.actions.setvariable",
            WFInput=attachment(action_output(token_id, "テキスト")),
            WFVariableName="token",
        ),
        # 4-5: 打刻の種類を選ぶ
        action(
            "is.workflow.actions.list",
            WFItems=[{"WFItemType": 0, "WFValue": text(w)} for w in WORK_TYPES],
            UUID=list_id,
        ),
        action(
            "is.workflow.actions.choosefromlist",
            WFInput=attachment(action_output(list_id, "リスト")),
            WFChooseFromListActionPrompt="打刻",
            UUID=chosen_id,
        ),
        # 6: API を呼ぶ
        action(
            "is.workflow.actions.downloadurl",
            WFURL="",
            WFHTTPMethod="POST",
            ShowHeaders=True,
            WFHTTPHeaders=dictionary(
                [("Authorization", text(f"Bearer {OBJ}", {"{7, 1}": variable("token")}))]
            ),
            WFHTTPBodyType="JSON",
            WFJSONValues=dictionary(
                [
                    ("user_id", text(OBJ, {"{0, 1}": variable("user_id")})),
                    ("work_type", text(OBJ, {"{0, 1}": action_output(chosen_id, "選択された項目")})),
                ]
            ),
            UUID=response_id,
        ),
        # 7-8: 結果を通知する
        action(
            "is.workflow.actions.getvalueforkey",
            WFInput=attachment(action_output(response_id, "URLの内容")),
            WFDictionaryKey="message",
            UUID=message_id,
        ),
        action(
            "is.workflow.actions.notification",
            WFNotificationActionTitle="JOBCAN",
            WFNotificationActionBody=text(OBJ, {"{0, 1}": action_output(message_id, "辞書の値")}),
        ),
    ]

    import_questions = [
        {"ActionIndex": 0, "Category": "Parameter", "ParameterKey": "WFTextActionText",
         "DefaultValue": "", "Text": "Slack の user_id（U から始まる ID）"},
        {"ActionIndex": 2, "Category": "Parameter", "ParameterKey": "WFTextActionText",
         "DefaultValue": "", "Text": "ショートカット用トークン（Bitwarden の JOBCAN_SHORTCUT_TOKEN）"},
        {"ActionIndex": 6, "Category": "Parameter", "ParameterKey": "WFURL",
         "DefaultValue": "https://", "Text": "API の URL（…/dev/shortcut/punch）"},
    ]

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


def main():
    default = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "shortcut", "jobcan-punch.shortcut"
    )
    out = sys.argv[1] if len(sys.argv) > 1 else default
    with open(out, "wb") as f:
        plistlib.dump(build(), f, fmt=plistlib.FMT_XML)
    print(out)


if __name__ == "__main__":
    main()
