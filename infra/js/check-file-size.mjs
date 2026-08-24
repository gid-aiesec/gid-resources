// Fails if any git-tracked file exceeds MAX_FILE_SIZE_KB
import { execFileSync } from "node:child_process";
import { statSync } from "node:fs";

const MAX_FILE_SIZE_KB = 500; // CONFIGURE: raise for repos that intentionally commit large assets

const files = execFileSync("git", ["ls-files"], { encoding: "utf-8" })
    .split("\n")
    .filter(Boolean);

const oversized = files
    .map((file) => ({ file, sizeKb: statSync(file).size / 1024 }))
    .filter(({ sizeKb }) => sizeKb > MAX_FILE_SIZE_KB);

if (oversized.length > 0) {
    for (const { file, sizeKb } of oversized) {
        console.error(
            `${file}: ${sizeKb.toFixed(0)}KB exceeds the ${MAX_FILE_SIZE_KB}KB limit`,
        );
    }
    process.exit(1);
}
