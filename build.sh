#!/usr/bin/env bash
set -euo pipefail
kit=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo 'Usage: bash build.sh STARLING_SOURCE OUTPUT ["all" or "horizonmatica,mod_menu,..."]' >&2
  exit 1
fi
source_dir=$(cd -- "$1" && pwd)
mkdir -p -- "$2"
output_dir=$(cd -- "$2" && pwd)
mods=${3:-all}
python3 "$kit/tools/check.py" --source "$source_dir" --mods "$mods"
mapfile -t ids < <(python3 - "$kit" "$mods" <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / 'tools'))
from check import selected
lock = json.loads((Path(sys.argv[1]) / 'sources.lock.json').read_text())
print('\n'.join(selected(sys.argv[2], lock['mods'])))
PY
)
bundles=()
for id in "${ids[@]}"; do bundles+=("$kit/mixins/$id"); done
export ABI=arm64-v8a
export VARIANT=--dev
export PROFILE=fast
# Always produce the APK as well as the library, even if a caller set this.
unset NATIVE_LIBRARY_ONLY
bash "$source_dir/packaging/android/native_build.sh" \
  "$source_dir" "$output_dir" "${bundles[@]}" 2>&1 | tee "$output_dir/build.log"
cp -- "$kit/sources.lock.json" "$output_dir/sources.lock.json"
python3 - "$output_dir" "${ids[@]}" <<'PY'
import json, pathlib, sys
output = pathlib.Path(sys.argv[1])
build = json.loads((output / 'build.json').read_text())
actual = sorted(m['id'] for m in build['mods'])
expected = sorted(sys.argv[2:])
if actual != expected:
    raise SystemExit(f'Build mod list differs: {actual} != {expected}')
if not list(output.glob('*.apk')):
    raise SystemExit('Build returned without an APK')
print('APK produced with: ' + ', '.join(actual))
print('Android device testing is still required.')
PY
