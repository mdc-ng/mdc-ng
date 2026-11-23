# syntax=docker/dockerfile:1
# Upstream image + patched backend binary (prepared by .github/workflows/ghcr.yml).
ARG BASE=mdcng/mdc:latest
FROM ${BASE}
ARG TARGETARCH
COPY --chmod=755 build/${TARGETARCH}/mdc_ng_app /usr/local/bin/mdc_ng_app
