#!/usr/bin/env python3
"""Generate a simple infrastructure diagram PNG from docker_containers.txt
Produces /home/dan/ibnaas/current_infrastructure.png
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import json

INPUT = '/home/dan/ibnaas/docker_containers.txt'
OUTPUT = '/home/dan/ibnaas/current_infrastructure.png'
EXTERNAL = '/home/dan/ibnaas/external_services.json'

# Read containers
containers = []
with open(INPUT) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('|')
        name = parts[0]
        image = parts[1] if len(parts) > 1 else ''
        ports = parts[2] if len(parts) > 2 else ''
        status = parts[3] if len(parts) > 3 else ''
        containers.append({'name': name, 'image': image, 'ports': ports, 'status': status})

# Try to read external services (optional)
external = []
try:
    with open(EXTERNAL) as f:
        external = json.load(f)
except Exception:
    # default placeholders
    external = [
        {"name": "NetBox (remote)", "type": "external", "ip": "<vm-ip>", "note": "inventory"},
        {"name": "Gluware (remote)", "type": "external", "ip": "<vm-ip>", "note": "config mgmt"},
        {"name": "Batfish (missing)", "type": "missing", "ip": "", "note": "not running"},
    ]

# Define interactions (directional) - best-effort inferred defaults
interactions = [
    ("chatops-open-webui", "chatops-localai", "calls LLM"),
    ("chatops-open-webui", "NetBox (remote)", "NetBox function"),
    ("st2-docker-st2api-1", "st2-docker-mongo-1", "db"),
    ("st2-docker-st2api-1", "st2-docker-rabbitmq-1", "messaging"),
    ("st2-docker-st2api-1", "st2-docker-redis-1", "coordination"),
    ("st2-docker-st2api-1", "NetBox (remote)", "inventory API"),
    ("st2-docker-st2api-1", "Gluware (remote)", "config push"),
    ("st2-docker-st2api-1", "Batfish (missing)", "validation"),
]

# Layout: simple columns: local containers, external services
width = 1600
height = 1000
img = Image.new('RGB', (width, height), 'white')
d = ImageDraw.Draw(img)

# Fonts
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
except Exception:
    font = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Title
title = 'Current infrastructure (generated)'
d.text((10, 8), title, fill='black', font=font)

# Draw local containers in left two columns
left_x = 20
col_w = 480
pad_y = 80
start_y = 60
per_col = 8

positions = {}

for idx, c in enumerate(containers):
    col = (idx // per_col)
    row = idx % per_col
    x = left_x + col * (col_w + 20)
    y = start_y + row * 90
    box_h = 78
    box_w = col_w
    fill = '#e8f4ff'
    d.rectangle((x, y, x+box_w, y+box_h), outline='black', width=2, fill=fill)
    d.text((x+8, y+6), c['name'], fill='black', font=font_small)
    d.text((x+8, y+28), c['image'][:60], fill='black', font=font_small)
    d.text((x+8, y+48), c['ports'][:80], fill='black', font=font_small)
    positions[c['name']] = (x+box_w//2, y+box_h//2)

# Draw external services on right (centered vertically relative to containers to avoid overlap)
ext_x = left_x + 2*(col_w + 20) + 40
ext_box_w = 380
ext_box_h = 100
ext_spacing = 40

# Compute vertical placement for externals so they don't overlap the container block
if positions:
    cont_centers = [cy for (cx, cy) in positions.values()]
    cont_min_center = min(cont_centers)
    cont_max_center = max(cont_centers)
    cont_box_h = 78
    containers_top = cont_min_center - cont_box_h//2
    containers_bottom = cont_max_center + cont_box_h//2
    ext_total_h = len(external) * ext_box_h + max(0, (len(external)-1) * ext_spacing)
    # center externals inside the containers vertical span if it fits, otherwise place below containers
    available_h = containers_bottom - containers_top
    if ext_total_h <= available_h:
        ext_y = int(containers_top + (available_h - ext_total_h) / 2)
        if ext_y < start_y:
            ext_y = start_y
    else:
        ext_y = int(containers_bottom + 40)
else:
    ext_y = start_y

for i, e in enumerate(external):
    y = ext_y + i * (ext_box_h + ext_spacing)
    box_w = ext_box_w
    box_h = ext_box_h
    if e.get('type') == 'missing':
        d.rectangle((ext_x, y, ext_x+box_w, y+box_h), outline='red', width=2)
        d.text((ext_x+8, y+6), f"{e['name']}", fill='red', font=font_small)
    else:
        d.rectangle((ext_x, y, ext_x+box_w, y+box_h), outline='black', width=2, fill='#fff3cd')
        d.text((ext_x+8, y+6), f"{e['name']}", fill='black', font=font_small)
    d.text((ext_x+8, y+28), f"ip: {e.get('ip','')}", fill='black', font=font_small)
    d.text((ext_x+8, y+48), e.get('note',''), fill='black', font=font_small)
    positions[e['name']] = (ext_x+box_w//2, y+box_h//2)

# Helper to draw arrow
def draw_arrow(a, b, label=None, color='black'):
    ax, ay = a
    bx, by = b
    d.line((ax, ay, bx, by), fill=color, width=2)
    # arrowhead
    import math
    angle = math.atan2(by-ay, bx-ax)
    l = 12
    p1 = (bx - l*math.cos(angle - math.pi/6), by - l*math.sin(angle - math.pi/6))
    p2 = (bx - l*math.cos(angle + math.pi/6), by - l*math.sin(angle + math.pi/6))
    d.polygon([ (bx,by), p1, p2 ], fill=color)
    if label:
        mx = (ax+bx)/2
        my = (ay+by)/2
        d.text((mx+6, my-6), label, fill=color, font=font_small)

# Draw interactions
for src, dst, lbl in interactions:
    # map names to positions (best-effort)
    src_pos = None
    dst_pos = None
    # try exact match first
    if src in positions:
        src_pos = positions[src]
    else:
        # try startswith
        for k in positions:
            if k.startswith(src):
                src_pos = positions[k]
                break
    if dst in positions:
        dst_pos = positions[dst]
    else:
        for k in positions:
            if k.startswith(dst):
                dst_pos = positions[k]
                break
    if src_pos and dst_pos:
        color = 'red' if 'missing' in dst.lower() else 'black'
        draw_arrow(src_pos, dst_pos, lbl, color=color)

# Footer
d.text((10, height-22), 'Note: auto-generated; external services may be placeholders. Provide /home/dan/ibnaas/external_services.json for accurate info.', fill='gray', font=font_small)

img.save(OUTPUT)
print('Wrote', OUTPUT)
