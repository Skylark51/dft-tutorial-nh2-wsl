"""Build the single-file WSL installer from the reviewed lesson files."""

import base64
import io
from pathlib import Path
import tarfile


ROOT = Path(__file__).resolve().parent
FILES = {"g16": "bin/g16", "activate": "activate"}
for job in ("nh2-guess", "nh2-alter"):
    for extension in ("inp", "out"):
        name = f"data/{job}.{extension}"
        FILES[name] = name

archive = io.BytesIO()
with tarfile.open(fileobj=archive, mode="w:gz") as package:
    for name, destination in FILES.items():
        content = (ROOT / name).read_bytes()
        if name in {"g16", "activate"}:
            content = content.replace(b"\r\n", b"\n")
        entry = tarfile.TarInfo(destination)
        entry.size = len(content)
        entry.mode = 0o755 if name == "g16" else 0o644
        package.addfile(entry, io.BytesIO(content))

header = r"""#!/usr/bin/env bash
set -euo pipefail
command -v python3 >/dev/null || { echo 'Install python3 in WSL first.' >&2; exit 1; }
root="$HOME/.local/share"
target="$root/dft-nh2"
mkdir -p -- "$root"
stage=$(mktemp -d "$root/.dft-nh2.XXXXXXXX")
trap 'rm -r -- "$stage"' EXIT
mkdir -- "$stage/lesson"
base64 -d <<'NH2_PAYLOAD' | tar -xz -C "$stage/lesson"
"""
footer = r"""NH2_PAYLOAD
if ! mv -T -- "$stage/lesson" "$target"; then
    echo 'An NH2 tutorial installation already exists or could not be installed.' >&2
    exit 1
fi
printf '%s\n' 'Installed. To start: source ~/.local/share/dft-nh2/activate'
"""
installer = ROOT / "install-dft-nh2.sh"
installer.write_bytes(
    header.encode("ascii") + base64.encodebytes(archive.getvalue()) + footer.encode("ascii")
)
