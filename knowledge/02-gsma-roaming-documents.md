---
title: Key GSMA Roaming Documents (IR and TD series)
source: Original study notes (verify details against the official GSMA documents)
---

# Key GSMA Roaming Documents

## IR.21: Roaming Database
IR.21 describes the structure of the roaming database that every operator publishes to its roaming
partners. An operator's IR.21 contains the network information a partner needs to configure roaming,
including:
- TADIG code, MCC and MNC, network name and country.
- Numbering: E.214 / E.212 information, IMSI ranges, Global Title ranges, MSISDN ranges.
- SCCP and signalling details: GTs of HLR, MSC/VLR, SMSC and other nodes.
- Packet data: GRX/IPX providers, IP address ranges, APN operator identifier, DNS details.
- LTE: Diameter realm, S6a/S8 related information, supported LTE roaming architecture.
- Contact points for IREG and TADIG testing and for operations.
Partners must update their configuration whenever a new IR.21 version is received. An outdated IR.21
is a very common root cause of roaming faults.

## IR.23, IR.24, IR.35, IR.38: testing
- IR.23: organisation of international roaming tests.
- IR.24: GSM end-to-end functional test specification.
- IR.35: GPRS end-to-end functional test specification.
- IR.38: LTE and EPC roaming testing.

## IR.33: GPRS Roaming Guidelines
Guidelines for packet-switched roaming over GPRS/UMTS: GTP between SGSN and GGSN, APN usage and
GRX connectivity.

## IR.34: IPX Provider Guidelines
Describes the inter-operator IP backbone (GRX / IPX) that carries roaming signalling and user-plane
traffic between operators, including service levels and how IPX providers interconnect.

## IR.67: DNS / ENUM Guidelines
Covers the private inter-operator DNS used on the GRX/IPX, for example resolving APNs and the
"mnc<MNC>.mcc<MCC>.gprs" and "3gppnetwork.org" domains.

## IR.88: LTE and EPC Roaming Guidelines
The main guideline for LTE roaming. It covers the S6a interface (MME to HSS, Diameter) and the S8
interface (SGW to PGW, GTP). It also covers Diameter routing through DEA / DRA and the IPX, and
the roaming architectures (home routed vs local breakout).

## IR.92 and IR.65: VoLTE
- IR.92: IMS profile for voice and SMS (the VoLTE device and network profile).
- IR.65: IMS roaming, interconnection and interworking guidelines. These describe options such as
  S8 Home Routing (S8HR) for VoLTE roaming.

## IR.73: Steering of Roaming
Guidelines on steering of roaming: how a home operator influences which visited network its
subscribers attach to. Badly configured steering can look like a registration failure during tests.

## TD series: billing and data clearing (TADIG)
- TD.57: TAP3 (Transferred Account Procedure) file format. The visited network uses it to charge
  the home network for roaming usage.
- TD.32: RAP (Returned Account Procedure), used to reject erroneous TAP files.
- TD.35: NRTRDE (Near Real Time Roaming Data Exchange), used for fraud control.
