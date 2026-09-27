from __future__ import annotations

import email
import imaplib
import re
from email.header import decode_header, make_header

from satira.config import settings
from satira.pipeline import run


FIELD_RE = re.compile(r"^(TITLE|CATEGORY|TAGS|TEXT|IMAGE|NOTES):\s*(.*)$", re.I)


def parse_body(subject: str, body: str) -> str:
    fields: dict[str, str] = {}
    current = None
    chunks: list[str] = []
    for line in body.splitlines():
        match = FIELD_RE.match(line.strip())
        if match:
            current = match.group(1).upper()
            fields[current] = match.group(2).strip()
            continue
        if current:
            fields[current] = (fields.get(current, "") + "\n" + line).strip()
        else:
            chunks.append(line)
    title = fields.get("TITLE") or subject
    text = fields.get("TEXT") or "\n".join(chunks).strip()
    extra = []
    if fields.get("CATEGORY"):
        extra.append(f"Category hint: {fields['CATEGORY']}")
    if fields.get("TAGS"):
        extra.append(f"Tags hint: {fields['TAGS']}")
    if fields.get("NOTES"):
        extra.append(f"Notes: {fields['NOTES']}")
    if fields.get("IMAGE"):
        extra.append(f"Image note: {fields['IMAGE']}")
    idea = f"{title}\n\n{text}"
    if extra:
        idea += "\n\n" + "\n".join(extra)
    return idea.strip()


def poll_once() -> list[dict]:
    if not settings.satira_email_enabled:
        return []
    results = []
    mail = imaplib.IMAP4_SSL(settings.imap_host, settings.imap_port)
    try:
        mail.login(settings.imap_user, settings.imap_password)
        mail.select(settings.imap_folder)
        _, data = mail.search(None, "UNSEEN")
        for num in data[0].split():
            _, raw = mail.fetch(num, "(RFC822)")
            message = email.message_from_bytes(raw[0][1])
            subject = str(make_header(decode_header(message.get("Subject", ""))))
            if settings.imap_subject_prefix and settings.imap_subject_prefix not in subject:
                continue
            body = _plain(message)
            idea = parse_body(subject.replace(settings.imap_subject_prefix, "").strip(), body)
            results.append(run(idea, push=True))
    finally:
        try:
            mail.logout()
        except Exception:
            pass
    return results


def _plain(message: email.message.Message) -> str:
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True) or b""
                return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
    payload = message.get_payload(decode=True) or b""
    if isinstance(payload, bytes):
        return payload.decode(errors="replace")
    return str(payload)
