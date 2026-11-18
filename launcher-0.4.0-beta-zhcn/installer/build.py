"""Compile the offline Windows installer with the system .NET Framework compiler."""

import hashlib
import json
import os
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIEW = ROOT / "preview-0.4.0-beta-zhcn"
MANIFEST = HERE / "manifest.json"


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    compiler = Path(os.environ["SystemRoot"]) / "Microsoft.NET/Framework64/v4.0.30319/csc.exe"
    output = ROOT / "work" / f'HellForge-{manifest["version"]}-zhcn-{manifest["commit"]}.exe'
    pending = output.with_suffix(".building.exe")
    references = ("System.Drawing.dll", "System.Windows.Forms.dll", "System.Web.Extensions.dll")
    command = [
        str(compiler), "/nologo", "/target:winexe", "/platform:anycpu", "/optimize+", "/codepage:65001",
        f"/out:{pending}", *(f"/reference:{name}" for name in references),
        f"/resource:{MANIFEST},manifest.json",
    ]
    for name, hashes in manifest["files"].items():
        path = PREVIEW / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != hashes["patched"]:
            raise ValueError(f"Unexpected preview payload: {path}")
        command.append(f"/resource:{path},{name}")
    try:
        subprocess.run([*command, str(HERE / "Installer.cs")], check=True)
        pending.replace(output)
    finally:
        pending.unlink(missing_ok=True)
    print(f"{output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
