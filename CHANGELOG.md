# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- No changes yet.

## [1.0.0] - 2026-06-11

### Added

- Home Assistant custom integration for Liquid-Check (`liquid_check`)
- Config Flow setup with configurable polling interval
- Sensor entities for level, content, age, error, firmware, hardware, tank max level, uptime, pump stats, and Wi-Fi stats
- Service `liquid_check.start_measure`
- Button entity to trigger measurement from the UI
- Automatic delayed refresh (~10 seconds) after triggering a measurement
- German/English translations for entities

### Changed

- Clean initial baseline for this standalone repository
- Stable key-based `unique_id` strategy
- No legacy migration logic in this baseline
