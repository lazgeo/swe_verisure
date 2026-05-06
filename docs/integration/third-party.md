# Third-party automation

Any platform capable of calling REST **Home Assistant Web API** `/api/services/<domain>/<service>` can operate Verisure remotely:

```http
POST /api/services/my_verisure/arm_away
Authorization: Bearer <token>
Content-Type: application/json

{"installation_id":"123456"}
```

Security requirements:

- Long-lived access tokens scoped minimally.  
- HTTPS termination trusted by client.  

Alternative: MQTT bridging via HA automation publishing state snapshots.
