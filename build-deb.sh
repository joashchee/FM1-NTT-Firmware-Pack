#!/bin/bash
# build-deb.sh
#
# Builds the pack's package on this computer: build/pkg/FM1-NTT-firmware-pack.deb (package r36s-fm1ntt-firmware-gpl, architecture all), which r3i6nos's
# flash-macos.sh can copy onto the games card (deb_watcher installs it at boot). Needs only Docker (Colima on an Apple chip). The work is
# package/build-pack-deb.sh, run as root in rust:1.98-bookworm (Debian 12); it checks the pack first and verifies the package against MANIFEST.tsv afterwards.
# PACK_VERSION overrides VERSION.
set -eu
die() { echo "build-deb: $*" >&2; exit 1; }
case "${1:-}" in -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;; esac
REPO="$(cd "$(dirname "$0")" && pwd)"
command -v docker >/dev/null || die "Docker is not installed (brew install colima docker, then colima start)"
# Docker Desktop's leftover config names a credential helper that is not installed without it: pulls then fail. Use an empty config.
if [ -z "${DOCKER_CONFIG:-}" ] && grep -q '"credsStore"[[:space:]]*:[[:space:]]*"desktop"' "$HOME/.docker/config.json" 2>/dev/null \
    && ! command -v docker-credential-desktop >/dev/null; then
    if [ -z "${DOCKER_HOST:-}" ]; then
        DOCKER_HOST="$(docker context inspect --format '{{.Endpoints.docker.Host}}' 2>/dev/null || true)"
        [ -n "$DOCKER_HOST" ] && export DOCKER_HOST
    fi
    DOCKER_CONFIG="$(mktemp -d "${TMPDIR:-/tmp}/fm1ntt-pack-docker.XXXXXX")"
    echo '{}' > "$DOCKER_CONFIG/config.json"
    export DOCKER_CONFIG
    trap 'rm -rf "$DOCKER_CONFIG"' EXIT
fi
docker info >/dev/null 2>&1 || die "Docker is not running (colima start)"
docker run --rm --platform linux/arm64 -v "$REPO":/src -w /src -e PACK_VERSION="${PACK_VERSION:-}" rust:1.98-bookworm package/build-pack-deb.sh
[ -s "$REPO/build/pkg/FM1-NTT-firmware-pack.deb" ] || die "the build finished but there is no build/pkg/FM1-NTT-firmware-pack.deb"
echo "[*] Built: $REPO/build/pkg/FM1-NTT-firmware-pack.deb ($(du -h "$REPO/build/pkg/FM1-NTT-firmware-pack.deb" | cut -f1))"
