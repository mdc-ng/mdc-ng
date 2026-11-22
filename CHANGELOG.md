# Changelog

## 2026-11-23

### Fixed
- 修复 AVbase 刮削：重写内置 AVbase 规则（`patched/providers/avbase.yaml`）以适配 avbase.net 当前页面结构，恢复标题、演员、简介、标签、厂商、厂牌、导演、系列、发售日、时长、封面、海报、剧照及搜索结果的解析。

### Added
- `patched/scripts/patch_providers.py`：替换上游 `mdc_ng_app` 二进制内嵌的刮削规则 YAML。
- `patched/scripts/test_rules.py`：用本地 HTML 页面测试规则 XPath。
- GitHub Actions（`.github/workflows/ghcr.yml`）自动构建并推送 `ghcr.io/tonghongte/mdc-ng`（amd64/arm64）。

### Changed
- README docker-compose 镜像改为 `ghcr.io/tonghongte/mdc-ng:latest`。
