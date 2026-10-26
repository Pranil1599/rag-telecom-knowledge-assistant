---
title: Roaming Glossary
source: Original study notes
---

# Roaming Glossary

- **HPMN / VPMN**: Home and Visited Public Land Mobile Network.
- **MCC / MNC**: Mobile Country Code and Mobile Network Code. Together they identify a network (PLMN).
- **IMSI**: International Mobile Subscriber Identity, stored on the SIM. It starts with MCC + MNC.
- **MSISDN**: The subscriber's phone number.
- **TADIG code**: A 5-character code that identifies an operator in roaming billing and data exchange,
  usually 3 letters for the country plus 2 characters for the operator.
- **Global Title (GT)**: An SS7 address used to route MAP signalling between networks.
- **E.214**: A numbering plan used to turn an IMSI into a Global Title so MAP messages can be routed to the home HLR.
- **HLR / HSS**: Home Location Register (2G/3G) and Home Subscriber Server (LTE). They hold subscriber data.
- **VLR / MSC**: Visitor Location Register and Mobile Switching Centre, which serve CS roamers in the visited network.
- **SGSN / GGSN**: Serving and Gateway GPRS Support Nodes, for 2G/3G packet data.
- **MME / SGW / PGW**: LTE nodes for mobility, serving gateway and PDN gateway.
- **STP**: Signalling Transfer Point, which routes SS7 signalling.
- **DEA / DRA**: Diameter Edge Agent / Diameter Routing Agent, which route Diameter signalling.
- **GRX / IPX**: Private IP backbone networks that carry roaming data and signalling between operators.
- **APN**: Access Point Name, which identifies the data network a device connects to.
- **CAMEL**: A protocol that lets the home network control calls of roamers, for example for prepaid.
- **SMSC**: Short Message Service Centre.
- **Steering of Roaming (SoR)**: Techniques the home operator uses to steer roamers to preferred partners.
- **IREG testing**: Technical end-to-end roaming tests between two operators.
- **TADIG testing**: Billing tests that prove TAP files are created and exchanged correctly.
- **TAP / RAP / NRTRDE**: Roaming billing records, returned (rejected) billing records, and near real-time fraud data.
- **Data Clearing House (DCH)**: A company that validates and exchanges TAP files between operators.
- **Test SIM**: A SIM card exchanged between operators only for IREG/TADIG testing.
