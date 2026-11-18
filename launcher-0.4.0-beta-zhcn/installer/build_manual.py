"""Package the Explorer copy-and-replace edition of the Windows patch."""

import hashlib
import json
from pathlib import PureWindowsPath
import zipfile

from build import HERE, MANIFEST, PREVIEW, ROOT


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    output = ROOT / "work" / f'HellForge-{manifest["version"]}-zhcn-{manifest["commit"]}-manual.zip'
    pending = output.with_suffix(".building")
    try:
        with zipfile.ZipFile(pending, "w", zipfile.ZIP_DEFLATED) as archive:
            manual = HERE / "manual"
            for path in sorted(path for path in manual.rglob("*") if path.is_file()):
                text = path.read_text(encoding="utf-8").replace("\n", "\r\n")
                encoding = "ascii" if path.suffix == ".bat" else "utf-8-sig"
                archive.writestr(path.relative_to(manual).as_posix(), text.encode(encoding))
            hashes = []
            for name, checks in manifest["files"].items():
                payload = (PREVIEW / name).read_bytes()
                if hashlib.sha256(payload).hexdigest() != checks["patched"]:
                    raise ValueError(f"Unexpected preview payload: {name}")
                archive.writestr("payload/" + name, payload)
                hashes.append(f'{PureWindowsPath(name)} {checks["original"]} {checks["patched"]}')
            archive.writestr("support/hashes.txt", ("\r\n".join(hashes) + "\r\n").encode("ascii"))
        pending.replace(output)
    finally:
        pending.unlink(missing_ok=True)
    print(f"{output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
