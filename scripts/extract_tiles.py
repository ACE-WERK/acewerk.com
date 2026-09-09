import re, base64, os

with open('/home/illya/projects/acewerk.com/index.html', 'r') as f:
    content = f.read()

m = re.search(r'const TILE_B64="([^"]+)"', content)
if m:
    b64 = m.group(1)
    print(f'TILE_B64 length: {len(b64)}')
    raw = base64.b64decode(b64)
    pixels = len(raw) // 3
    side = int(pixels ** 0.5)
    print(f'Pixels: {pixels} ({side}x{side})')
    
    os.makedirs('/home/illya/projects/acewerk.com/data', exist_ok=True)
    with open('/home/illya/projects/acewerk.com/data/tile-data.b64', 'w') as f:
        f.write(b64)
    print('Written to data/tile-data.b64')
else:
    print('TILE_B64 not found')
