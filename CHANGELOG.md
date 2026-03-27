# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2026-03-27
### Added
- Added signatures for:
  - Anthropic Claude tokens
  - Hugging Face tokens
  - Replicate tokens

### Changed
- Updated Google signature to catch Gemini tokens

## 2026-02-20
### Added
- Added signatures for
  - Telegram Bot tokens
  - Discord tokens
  - GitLab tokens

### Changed
- New regex to match updated token formats for:
  - AWS
  - Azure
  - Generic Tokens
  - Cloudflare
  - Twilio
  - Stripe
  - Shodan
  - NewRelic
  - Heroku
  - Google
  - GitHub

## 2024-11-29
### Changed
- Update regex for Slack Webhooks
- Update testing to include information on failed cases

## 2024-04-26
### Added
- Signatures now support Stack Overflow Watchman
  - Tests added for the new Stack Overflow Watchman format

## 2023-12-22
### Added
- Added signatures for:
  - Alibaba
  - Akamai