#!/usr/bin/env bash
# Source-only evidence rehearsal. Never pushes, merges protected refs or deploys.
set -Eeuo pipefail
export GIT_TERMINAL_PROMPT=0

usage() { echo 'Usage: bash rehearse-dealership-source-merge.sh /absolute/path/to/EMPTY/output-directory' >&2; exit 64; }
[[ $# -eq 1 && "$1" = /* && "$1" != / ]] || usage
out="${1%/}"
[[ ! -e "$out" ]] || [[ -d "$out" && -z "$(find "$out" -mindepth 1 -maxdepth 1 -print -quit)" ]] || {
  echo 'Refusing to overwrite a nonempty destination' >&2; exit 65;
}
mkdir -p "$out"

remote='https://github.com/danwiz/project0-cardealership.git'
master='90741d3abe51d9cc002aaeb1dacae27b933fba10'
short='086fbf91294f74fe4bd967256498ef94e92c501a'
candidate='0cbad314956ad1d36542d30afa6519a1bbfecdce'
mirror="$out/project0-cardealership.mirror.git"

git clone --mirror "$remote" "$mirror"
check_head() {
  local ref="$1" expected="$2" actual
  actual="$(git -C "$mirror" rev-parse --verify "$ref^{commit}")"
  if [[ "$actual" != "$expected" ]]; then
    printf 'STOP: %s changed: expected %s, got %s\n' "$ref" "$expected" "$actual" >&2
    exit 66
  fi
  printf '%s %s\n' "$ref" "$actual" >> "$out/ref-verification.txt"
}
check_head refs/heads/master "$master"
check_head refs/heads/fix/atomic-account-create-20261029 "$short"
check_head refs/heads/security/integration-candidate-master-pbkdf2-parity-20261029 "$candidate"

git -C "$mirror" fsck --full --strict > "$out/git-fsck.txt" 2>&1
git -C "$mirror" show-ref > "$out/all-refs.txt"
for key in master fix/atomic-account-create-20261029 security/integration-candidate-master-pbkdf2-parity-20261029; do
  name="${key//\//_}"
  git -C "$mirror" ls-tree -r --full-tree "refs/heads/$key" > "$out/tree-$name.txt"
done

bundle="$out/project0-cardealership-all-refs.bundle"
git -C "$mirror" bundle create "$bundle" --all
git -C "$mirror" bundle verify "$bundle" > "$out/bundle-verify.txt" 2>&1
( cd "$out" && sha256sum "$(basename "$bundle")" > bundle.sha256 )

candidate_ref='refs/heads/security/integration-candidate-master-pbkdf2-parity-20261029'
for pair in master fix/atomic-account-create-20261029; do
  left="refs/heads/$pair"
  name="${pair//\//_}"
  set +e
  git -C "$mirror" merge-tree --write-tree "$left" "$candidate_ref" > "$out/merge-tree-$name.txt" 2>&1
  result=$?
  set -e
  printf '%s merge-tree-exit=%s (0=clean, 1=reported conflict, >1=error)\n' "$pair" "$result" >> "$out/merge-summary.txt"
  if (( result > 1 )); then
    echo "STOP: unexpected git merge-tree error for $pair. See saved output." >&2
    exit 67
  fi
done

cat > "$out/SCOPE.txt" <<'EOF'
This is a local, full Git bundle and two Git merge-tree rehearsals.
It does not modify any GitHub branch, issue, pull request, environment or release.
The Git bundle includes fetched Git refs/objects but NOT GitHub PR/issue metadata,
Actions artifacts, Git LFS objects, secrets inventory or independent provenance signoff.
Review bundle.sha256 and bundle-verify.txt; securely store the bundle separately.
A conflict-free merge-tree result is NOT security acceptance or promotion approval.
EOF
printf 'Rehearsal artifacts written locally to: %s\n' "$out"
cat "$out/merge-summary.txt"
