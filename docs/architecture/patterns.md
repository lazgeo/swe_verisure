# Patterns

## Coordinator pattern

`MyVerisureDataUpdateCoordinator` centralizes polling and exposes imperative alarm APIs shared by entities and services.

## Repository pattern

Repositories hide GraphQL query strings and parse payloads into DTO/domain objects consumed by use cases.

## Dependency injection

Injector binds interfaces → implementations for tests and swapping API stubs.

## Translator helper

`coordinator.get_translation` bridges HA language settings with JSON translation files for notifications.
