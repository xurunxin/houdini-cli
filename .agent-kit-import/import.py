"""Temporary, digest-locked import of the reviewed local kit; never part of the final PR."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import lzma
import subprocess
import sys

ROOT = Path.cwd()
KIT = ROOT / "agent-kit"
EXPECTED_TREE = "5de353d1bcd1570122beae0b215816546b1a10ba"


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def main():
    if KIT.exists() or KIT.is_symlink():
        raise RuntimeError("Refusing to overwrite an existing agent-kit")
    if git("hash-object", "README.md") != "1992f8fdf452d0555935bad9e33c7649fb47f984":
        raise RuntimeError("README baseline changed; reconcile before import")
    chunks = [ROOT / ".agent-kit-import" / f"payload.{i:03d}" for i in range(10)]
    packed = b"".join(p.read_bytes() for p in chunks)
    if len(packed) != 79464 or hashlib.sha256(packed).hexdigest() != "0913bf3713139f3695a9ddf5cfd70cf8655b81470f41ede1176398544adbf111":
        raise RuntimeError("Payload digest or length mismatch")
    payload = json.loads(lzma.decompress(packed))
    files = payload["files"]
    if not isinstance(files, dict) or len(files) != 78:
        raise RuntimeError("Unexpected source manifest")
    for name, content in files.items():
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name or not path.parts or not isinstance(content, str):
            raise RuntimeError(f"Unsafe payload path: {name!r}")
    for name, content in files.items():
        dest = KIT / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("x", encoding="utf-8", newline="\n") as out:
            out.write(content)
    for tool in ["rebuild_wiki.py", "build_site.py"]:
        subprocess.run([sys.executable, str(KIT / "tools" / tool)], check=True)
    entries = [
        hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.relative_to(KIT).as_posix()
        for p in sorted(KIT.rglob("*"))
        if p.is_file() and p.name != "MANIFEST.sha256" and "__pycache__" not in p.parts and p.suffix != ".pyc"
    ]
    if len(entries) != 153:
        raise RuntimeError(f"Unexpected generated file count: {len(entries)}")
    (KIT / "MANIFEST.sha256").write_text("\n".join(entries) + "\n", encoding="utf-8")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    marker = "## 开发和验收\n"
    if text.count(marker) != 1 or "## Houdini Agent Wiki 与领域 Skills" in text:
        raise RuntimeError("Unexpected README insertion target")
    readme.write_text(text.replace(marker, payload["readme_insertion"] + marker), encoding="utf-8")
    subprocess.run(["git", "add", "--", "agent-kit", "README.md"], check=True)
    actual = git("write-tree", "--prefix=agent-kit/")
    if actual != EXPECTED_TREE:
        raise RuntimeError(f"Generated content differs from reviewed kit: {actual} != {EXPECTED_TREE}")
    print(json.dumps({"ok": True, "agent_kit_tree": actual, "readme_blob": git("hash-object", "README.md"), "files": 154}))


if __name__ == "__main__":
    main()
