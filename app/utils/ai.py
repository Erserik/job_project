from typing import Any, Dict
import httpx
from app.config import settings


def build_prompt(metadata: Dict[str, Any]) -> str:
    parts = [
        f"File name: {metadata.get('file_name')}",
        f"File size: {metadata.get('file_size')} bytes",
        f"Version: {metadata.get('version')}",
        f"Extension: {metadata.get('extension')}",
        f"Uploaded at: {metadata.get('uploaded_at')}",
    ]
    return "Analyze the document based on these metadata fields and briefly describe how significant the changes look:\n" + "\n".join(parts)


async def analyze_metadata(metadata: Dict[str, Any]) -> str:
    if not settings.openai_api_key:
        size = metadata.get("file_size") or 0
        version = metadata.get("version") or 1

        if size < 50_000:
            size_desc = "небольшой"
        elif size < 500_000:
            size_desc = "средний"
        else:
            size_desc = "достаточно крупный"

        if version == 1:
            version_desc = "это первая версия файла."
        elif version == 2:
            version_desc = "изменения выглядят умеренными по сравнению с предыдущей версией."
        else:
            version_desc = "файл прошёл уже несколько итераций, изменения могут быть более существенными."

        return f"Файл {size_desc}, версия {version}. В целом {version_desc}"

    prompt = build_prompt(metadata)

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты помогаешь кратко описать значимость изменений документа по его метаданным.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 120,
            },
        )

    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
