# Amazon Alexa

Use Home Assistant’s Alexa integration (cloud or manual) to expose:

- **Alarm control panel** entity — voice arm/disarm where Alexa maps HA domains safely.  
- **Routines / scenes** calling HA scripts that invoke `my_verisure.*` services.

Exact utterances depend on Alexa locale + HA cloud configuration — verify in the Alexa app.

Security tip: prefer **PIN confirmation** at HA script layer if Alexa exposes sensitive actions.
