"""Build the localized HellForge 0.4.0-beta launcher preview from a copy."""

import argparse
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import runpy
import struct


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "launcher-0.4.0-beta-input" / "HellForge.Launcher.dll"
VERSION = "launcher-0.4.0-beta-zhcn"
INPUT_SHA256 = "3ebfc7e270564deeb688465cc6f9613cfcb4fed67be201ec4f0d3288c06d4fe1"
STEAM_DLL = "HellForge.SteamDownload.dll"
STEAM_SHA256 = "98bb04f1edd25e52896fb8b58839f07f1047c01f6810b7ab796128ca5304101a"
PREVIEW = ROOT / "preview-0.4.0-beta-zhcn"
USER_STRING = 0x70000000


def align(value, alignment):
    return (value + alignment - 1) // alignment * alignment


def read_assembly(path):
    return runpy.run_path(
        str(Path(__file__).with_name("pe_meta.py")),
        run_name="hellforge_pe_reader",
        init_globals={"PATH": str(path)},
    )


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def locator_matches(ref, locator):
    method, at, offset = locator.rpartition("@")
    if not at or not offset.isdecimal() or ref["il_offset"] != int(offset):
        return False
    if method == ref["method"]:
        return True
    if not method.endswith("." + ref["method"]):
        return False
    qualifier = method[: -len(ref["method"]) - 1]
    types = ref["type_path"].split(".")
    size = len(qualifier.split("."))
    return any(
        ".".join(types[end - size:end]) == qualifier
        for end in range(size, len(types) + 1)
    )


def build_plan(source, project):
    refs_by_token = defaultdict(list)
    for ref in source["ldstr"]:
        refs_by_token[int(ref["token"], 16)].append(ref)

    plan = {}
    deferred = []
    for row in read_csv(project / "zh-cn-master.csv"):
        token = int(row["token"], 16)
        if source["us"](token & 0xFFFFFF) != row["original"]:
            raise ValueError(f'Source text changed for {row["item_id"]}')
        if row["translation"] == row["original"]:
            continue
        if row["status"] not in {"已译", "锁定"}:
            deferred.append({"item": row["item_id"], "reason": row["status"]})
            continue
        if not row["translation"]:
            raise ValueError(f'Empty approved translation for {row["item_id"]}')
        matches = [
            ref for ref in refs_by_token[token]
            if locator_matches(ref, row["locator"])
        ]
        if len(matches) != 1:
            deferred.append({
                "item": row["item_id"],
                "locator": row["locator"],
                "reason": f"expected one matching location, found {len(matches)}",
            })
            continue
        plan[matches[0]["operand_offset"]] = (token, row["translation"])

    plan.update(scoped_plan(refs_by_token, project / "modules" / "sync-callpoints.csv"))
    return plan, deferred


def scoped_plan(refs_by_token, path):
    plan = {}
    for row in read_csv(path):
        token = int(row["token"], 16)
        matches = [
            ref for ref in refs_by_token[token]
            if locator_matches(ref, row["method_il"]) and ref["text"] == row["original"]
        ]
        if len(matches) != 1:
            raise ValueError(f'Unresolved scoped entry {row["token"]} {row["method_il"]}')
        offset = matches[0]["operand_offset"]
        if offset in plan:
            raise ValueError(f'Duplicate scoped entry {row["token"]} {row["method_il"]}')
        plan[offset] = (token, row["callpoint_translation"])
    return plan


def encode_user_string(text):
    raw = text.encode("utf-16-le")
    special_low_bytes = {*range(1, 9), *range(14, 32), 0x27, 0x2D, 0x7F}
    marker = any(raw[1::2]) or any(byte in special_low_bytes for byte in raw[::2])
    size = len(raw) + 1
    if size < 0x80:
        prefix = bytes([size])
    elif size < 0x4000:
        prefix = struct.pack(">H", size | 0x8000)
    else:
        prefix = struct.pack(">I", size | 0xC0000000)
    return prefix + raw + bytes([marker])


def relocate_metadata(source, plan):
    image = bytearray(source["data"])
    opt, dd, cli, coff = (source[key] for key in ("opt", "dd", "cli", "coff"))
    u32 = source["u32"]
    if (u32(dd + 32) or u32(cli + 32) or u32(cli + 64) or u32(cli + 16) != 1):
        raise ValueError("Expected an unsigned IL-only assembly without native metadata")

    file_alignment, section_alignment = u32(opt + 36), u32(opt + 32)
    sections = source["sections"]
    header = source["sec_off"] + source["num_sections"] * 40
    if len(image) != max(raw + size for _, _, _, raw, size in sections):
        raise ValueError("Unexpected data after the original PE sections")

    md, md_size, us_offset, us_size = (
        source[key] for key in ("md", "md_size", "us_off", "us_size")
    )
    metadata = bytearray(image[md:md + md_size])
    strings = bytearray(image[us_offset:us_offset + us_size])
    translations = {}
    for offset, (token, translation) in sorted(plan.items()):
        if image[offset - 1] != 0x72 or u32(offset) != token:
            raise ValueError(f"Instruction at {offset} is not the expected ldstr")
        if translation not in translations:
            if len(strings) > 0xFFFFFF:
                raise ValueError("User-string heap exceeds token address space")
            translations[translation] = USER_STRING | len(strings)
            strings.extend(encode_user_string(translation))
        struct.pack_into("<I", image, offset, translations[translation])

    stream_header = 16 + u32(md + 12)
    stream_count, = struct.unpack_from("<H", metadata, stream_header + 2)
    stream_header += 4
    for _ in range(stream_count):
        name_end = metadata.index(0, stream_header + 8)
        if metadata[stream_header + 8:name_end] == b"#US":
            strings_offset = align(len(metadata), 4)
            struct.pack_into("<II", metadata, stream_header, strings_offset, align(len(strings), 4))
            metadata.extend(b"\0" * (strings_offset - len(metadata)))
            metadata.extend(strings)
            metadata.extend(b"\0" * (align(len(metadata), 4) - len(metadata)))
            break
        stream_header = align(name_end + 1, 4)
    else:
        raise ValueError("Missing #US stream")

    raw_offset = align(len(image), file_alignment)
    raw_size = align(len(metadata), file_alignment)
    virtual_end = max(va + max(vsize, size) for _, va, vsize, _, size in sections)
    if header + 40 <= min(section[3] for section in sections):
        rva = align(virtual_end, section_alignment)
        struct.pack_into(
            "<8sIIIIIIHHI", image, header, b".hfzh", len(metadata), rva,
            raw_size, raw_offset, 0, 0, 0, 0, 0x40000040,
        )
        struct.pack_into("<H", image, coff + 2, source["num_sections"] + 1)
    else:
        # SteamDownload's section table has no spare header. Preserve its base
        # relocations and append the metadata inside the final readable section.
        name, va, vsize, raw, size = sections[-1]
        header -= 40
        if (name != ".reloc" or vsize > size or va + size != virtual_end
                or raw + size != raw_offset or u32(header + 36) != 0x42000040):
            raise ValueError("No room for preview metadata in this PE layout")
        rva = va + size
        struct.pack_into("<I", image, header + 8, size + len(metadata))
        struct.pack_into("<I", image, header + 16, size + raw_size)
        struct.pack_into("<I", image, header + 36, 0x40000040)  # Keep metadata mapped.
    struct.pack_into("<I", image, opt + 8, u32(opt + 8) + raw_size)
    struct.pack_into("<I", image, opt + 56, align(rva + len(metadata), section_alignment))
    struct.pack_into("<I", image, opt + 64, 0)
    struct.pack_into("<II", image, cli + 8, rva, len(metadata))
    image.extend(b"\0" * (raw_offset - len(image)))
    image.extend(metadata)
    image.extend(b"\0" * (raw_size - len(metadata)))
    return image


def verify_build(source, built, plan):
    if source["assembly_info"] != built["assembly_info"]:
        raise ValueError("Assembly identity changed")
    before = {ref["operand_offset"]: ref for ref in source["ldstr"]}
    after = {ref["operand_offset"]: ref for ref in built["ldstr"]}
    if before.keys() != after.keys():
        raise ValueError("IL string instruction locations changed")
    for offset, ref in before.items():
        expected = plan[offset][1] if offset in plan else ref["text"]
        if after[offset]["text"] != expected:
            raise ValueError(f"Unexpected text at IL operand {offset}")


def write_dll(source, plan, destination):
    pending = destination.with_suffix(".dll.building")
    pending.write_bytes(relocate_metadata(source, plan))
    try:
        built = read_assembly(pending)
        verify_build(source, built, plan)
        pending.replace(destination)
    finally:
        pending.unlink(missing_ok=True)
    return built


def build_steam_text(preview, project):
    source_path = preview / "app" / "cli" / STEAM_DLL
    destination = preview / "app" / "launcher" / STEAM_DLL
    if not all(path.resolve(strict=True).is_relative_to(preview) for path in (source_path, destination)):
        raise ValueError("Steam download assembly path escapes the preview")
    source = read_assembly(source_path)
    if hashlib.sha256(source["data"]).hexdigest() != STEAM_SHA256:
        raise ValueError(f"Unexpected source version for {STEAM_DLL}")
    refs_by_token = defaultdict(list)
    for ref in source["ldstr"]:
        refs_by_token[int(ref["token"], 16)].append(ref)
    plan = scoped_plan(refs_by_token, project / "steam-download-callpoints.csv")
    built = write_dll(source, plan, destination)
    print(f"Localized {len(plan)} Steam download call points.")
    return {
        "base_sha256": STEAM_SHA256,
        "preview_sha256": hashlib.sha256(built["data"]).hexdigest(),
        "verified_ldstr": len(source["ldstr"]),
        "localized_callpoints": len(plan),
    }


def build_profile_text(preview):
    path = preview / "app" / "profile-templates.json"
    if not path.resolve(strict=True).is_relative_to(preview):
        raise ValueError("Template description target escapes the preview")
    entries_path = ROOT / VERSION / "profile-template-descriptions.json"
    entries = json.loads(entries_path.read_text(encoding="utf-8-sig"))
    original_data = path.read_bytes()
    text = original_data.decode("utf-8")
    templates = json.loads(text)["templates"]
    for key, entry in entries.items():
        original, translation = entry["original"], entry["translation"]
        current = templates[key]["description"]
        if current == translation:
            continue
        original_literal = json.dumps(original, ensure_ascii=False)
        if current != original or text.count(original_literal) != 1:
            raise ValueError(f"Unexpected template description for {key}")
        text = text.replace(original_literal, json.dumps(translation, ensure_ascii=False), 1)
    updated = text.encode("utf-8")
    if updated != original_data:
        pending = path.with_suffix(".json.building")
        pending.write_bytes(updated)
        try:
            pending.replace(path)
        finally:
            pending.unlink(missing_ok=True)
    print(f"Localized {len(entries)} profile template descriptions.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preview", type=Path, default=PREVIEW,
        help="Output folder beneath this workspace (default: %(default)s)",
    )
    parser.add_argument(
        "--profile-text", action="store_true", help="Also localize template descriptions in an installed preview",
    )
    parser.add_argument(
        "--steam-text", action="store_true", help="Also localize Steam download choices in an installed preview",
    )
    options = parser.parse_args()
    preview = options.preview.resolve()
    if not preview.is_relative_to(ROOT) or preview.is_relative_to(INPUT.parent):
        parser.error("The preview must be a separate output directory inside the workspace")

    source = read_assembly(INPUT)
    digest = hashlib.sha256(source["data"]).hexdigest()
    if digest != INPUT_SHA256:
        raise ValueError(f"Unexpected input version: {digest}")
    plan, deferred = build_plan(source, ROOT / VERSION)
    if not plan:
        raise ValueError("No localized instructions matched")

    launcher = preview / "app" / "launcher"
    launcher.mkdir(parents=True, exist_ok=True)
    destination = launcher / INPUT.name
    built = write_dll(source, plan, destination)
    report = {
        "base_sha256": digest,
        "preview_sha256": hashlib.sha256(built["data"]).hexdigest(),
        "verified_ldstr": len(source["ldstr"]),
        "localized_callpoints": len(plan),
        "deferred_rows": deferred,
    }
    if options.steam_text:
        report["steam_download"] = build_steam_text(preview, ROOT / VERSION)
    (preview / "build-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(f"Localized {len(plan)} call points; deferred {len(deferred)} rows.")
    if options.profile_text:
        build_profile_text(preview)


if __name__ == "__main__":
    main()
