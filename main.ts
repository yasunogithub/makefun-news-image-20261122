// News-image daily entry: deliver entry.png to the output directory.
//
// The picture itself is produced by draw.py from content.json (the day's
// stories); this entrypoint is the delivery step the grader runs, so it
// first proves the file beside it is a PNG the gate accepts (at most
// 1024x1024 pixels and 1 MiB) and only then copies it, byte for byte, to
// MAKEFUN_OUTPUT_DIR (the grader's /output outside this container).
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024; // the gate's 1 MiB cap
const MAX_SIDE = 1024; // the gate's 1024x1024 cap

const source = new URL('./entry.png', import.meta.url);
const png = readFileSync(source);

// A PNG opens with this fixed 8-byte signature; the IHDR chunk follows,
// carrying width and height as big-endian uint32 at bytes 16 and 20.
const SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < SIGNATURE.length; i += 1) {
  if (png[i] !== SIGNATURE[i]) throw new Error('entry.png is not a PNG file');
}
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over the ${MAX_SIDE}x${MAX_SIDE} cap`);
}
if (png.length > MAX_BYTES) {
  throw new Error(`entry.png is ${png.length} bytes, over the ${MAX_BYTES} byte cap`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
copyFileSync(source, target);
console.log(`entry.png: ${width}x${height}, ${png.length} bytes -> ${target}`);
