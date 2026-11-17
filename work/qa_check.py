# -*- coding: utf-8 -*-
"""Verify the review-sample table in the deliverable against the extracted #US heap.

Reads only files inside the workspace. Writes work/trial-entries.csv and checks
that the space-bearing entries keep real spaces in the CSV.
"""
import io
import os
import re
import sys
import csv

ROOT = sys.argv[1]
MD = os.path.join(ROOT, 'launcher-0.4.0-beta-trial.md')
US = os.path.join(ROOT, 'work', 'us_all.tsv')
CSV = os.path.join(ROOT, 'work', 'trial-entries.csv')

us = {}
with io.open(US, encoding='utf-8') as f:
    next(f)
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) >= 3 and p[0].isdigit():
            us[int(p[0])] = (int(p[1]), p[2].replace('\\t', '\t').replace('\\n', '\n'))

rows = []
with io.open(MD, encoding='utf-8') as f:
    for line in f:
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) != 9 or not cells[0].isdigit():
            continue
        rows.append(cells)

problems = []
seen = set()
out_rows = []
for c in rows:
    n, cat, orig, usi, tok, loc, foff, trans, note = c
    usi = int(usi)
    shown = orig.replace('␠', ' ')
    trans_out = trans.replace('␠', ' ')
    out_rows.append([n, cat, usi, tok, loc, foff, shown, trans_out, note])
    if usi not in us:
        problems.append('#%s us=%d 不在字符串堆' % (n, usi))
        continue
    real_off, real = us[usi]
    if shown != real:
        problems.append('#%s 原文不一致: 表中 %r / 堆内 %r' % (n, shown, real))
    if int(foff) != real_off:
        problems.append('#%s 文件偏移不符: 表中 %s / 实际 %d' % (n, foff, real_off))
    if tok != '0x%08X' % (0x70000000 | usi):
        problems.append('#%s token 不符: %s' % (n, tok))
    if not trans_out.strip():
        problems.append('#%s 译文为空' % n)
    if usi in seen:
        problems.append('#%s us 索引重复 %d' % (n, usi))
    seen.add(usi)

# format-item expectations
by_id = {r[0]: r for r in out_rows}
if by_id.get('9', [None] * 8)[7] != ': ':
    problems.append('#9 应为保留格式项，译文须等于 ": "（ASCII 冒号加一个空格）')
if by_id.get('12', [None] * 8)[7] != '无法保存日志: ':
    problems.append('#12 译文须等于 "无法保存日志: "（ASCII 冒号加一个尾空格）')
if not by_id.get('7', [None] * 8)[7].endswith(' '):
    problems.append('#7 译文须保留尾空格')
if not by_id.get('8', [None] * 8)[7].startswith(' '):
    problems.append('#8 译文须保留首空格')

# structural checks
text = io.open(MD, encoding='utf-8').read()
sections = ['## 1 静态提取结果', '## 2 术语表初稿', '## 3 风格规则', '## 4 审阅样本与试译',
            '## 5 审阅样本 QA', '## 6 交付形态与回填路径', '## 7 未验证事项',
            '## 8 文件验收', '## 9 问题清单', '## 10 变动记录', '## 11 阶段小结',
            '## 12 试译确认', '## 项目状态看板']
for s in sections:
    if s not in text:
        problems.append('缺少章节 %s' % s)
if text.index('## 项目状态看板') < text.index('## 12 试译确认'):
    problems.append('看板未放在文末')
if '与委托方给定值一致' in text:
    problems.append('哈希表述仍写作委托方给定值')
for c in rows:
    if re.search(r'\{\d\}|%[sd]', c[2]):
        problems.append('#%s 原文列含复合占位符' % c[0])

approved_statuses = {}
if os.path.isfile(CSV):
    with io.open(CSV, encoding='utf-8-sig', newline='') as f:
        approved_statuses = {(r['entry_id'], r['original'], r['translation']): r['status']
                             for r in csv.DictReader(f)}

with io.open(CSV, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['entry_id', 'category', 'us_index', 'token', 'method_il', 'file_offset',
                'original', 'translation', 'note', 'status'])
    for r in out_rows:
        status = approved_statuses.get((r[0], r[6], r[7]), '待确认')
        w.writerow(list(r[:9]) + [status])

# read the CSV back and confirm the spaces survive on disk
with io.open(CSV, encoding='utf-8-sig', newline='') as f:
    back = {r['entry_id']: r for r in csv.DictReader(f)}
if back['9']['translation'] != ': ':
    problems.append('CSV #9 缺真实空格: %r' % back['9']['translation'])
if back['12']['translation'] != '无法保存日志: ':
    problems.append('CSV #12 缺真实尾空格: %r' % back['12']['translation'])
if not back['7']['translation'].endswith(' '):
    problems.append('CSV #7 缺真实尾空格: %r' % back['7']['translation'])
if back['12']['original'] != 'Could not save the logs: ':
    problems.append('CSV #12 原文尾空格丢失: %r' % back['12']['original'])

trial = [r for r in out_rows if r[1] != '保留格式']
print('rows:', len(out_rows), 'trial:', len(trial), 'format-kept:', len(out_rows) - len(trial))
print('unique us:', len(seen))
print('spaces on disk: #7 %r  #9 %r  #12 %r' % (back['7']['translation'], back['9']['translation'],
                                               back['12']['translation']))
print('problems:', len(problems))
for p in problems:
    print(' -', p)
print('csv written:', CSV, os.path.getsize(CSV), 'bytes')
