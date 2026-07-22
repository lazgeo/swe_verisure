# Automation examples

Replace every `event.example_*`, `sensor.example_*`, and `camera.example_*`
entity ID with an entity selected from your own Home Assistant instance. These
examples contain no real account or device data.

## Notify on an intrusion event

```yaml
alias: Verisure intrusion notification
triggers:
  - trigger: state
    entity_id: event.example_security_alarm
conditions:
  - condition: template
    value_template: >-
      {{ trigger.to_state is not none
         and trigger.to_state.attributes.event_type == 'intrusion' }}
actions:
  - action: persistent_notification.create
    data:
      title: Verisure security event
      message: >-
        Intrusion event reported at
        {{ trigger.to_state.attributes.event_time | default('unknown time') }}.
mode: queued
```

## Handle several urgent categories

```yaml
alias: Verisure urgent security events
triggers:
  - trigger: state
    entity_id: event.example_security_alarm
conditions:
  - condition: template
    value_template: >-
      {{ trigger.to_state is not none
         and trigger.to_state.attributes.event_type
             in ['intrusion', 'fire', 'sos', 'water'] }}
actions:
  - action: notify.notify
    data:
      title: Verisure alert
      message: >-
        Type: {{ trigger.to_state.attributes.event_type }}
        Area: {{ trigger.to_state.attributes.area | default('not supplied') }}
mode: queued
```

## Record arm and disarm activity

```yaml
alias: Verisure arm activity
triggers:
  - trigger: state
    entity_id: event.example_alarm_activity
conditions:
  - condition: template
    value_template: >-
      {{ trigger.to_state is not none
         and trigger.to_state.attributes.event_type in ['arm', 'disarm'] }}
actions:
  - action: logbook.log
    data:
      name: Verisure
      message: >-
        Alarm activity: {{ trigger.to_state.attributes.event_type }}
mode: queued
```

## Warn when the SMS balance is low

```yaml
alias: Verisure low SMS balance
triggers:
  - trigger: numeric_state
    entity_id: sensor.example_remaining_sms
    below: 5
actions:
  - action: persistent_notification.create
    data:
      title: Verisure SMS balance
      message: The Verisure SMS balance is low.
mode: single
```

## Request a new camera image

```yaml
actions:
  - action: swe_verisure.capture_smartcam
    target:
      entity_id: camera.example_smartcam
```

## Safety note

This integration polls an unofficial cloud API. Automations can be delayed by
the configured interval, Verisure ingestion time, network failures, or rate
limiting. Do not use Home Assistant as the only path for life-safety, burglary,
fire, water, SOS, or emergency notifications; keep Verisure's official alarm
and monitoring channels enabled.
