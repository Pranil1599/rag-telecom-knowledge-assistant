---
title: LTE Roaming Architecture: Home Routing, Local Breakout and the IPX
source: Original study notes based on GSMA IR.88 and 3GPP TS 23.401 concepts (verify against the documents)
---

# LTE Roaming Architecture

## Key nodes
- MME (visited network): handles attach, authentication and mobility for the roaming device.
- HSS (home network): stores the subscription and authentication data.
- SGW (Serving Gateway, visited network): anchors the user plane in the visited network.
- PGW (PDN Gateway): connects to the APN / internet. Its location depends on the architecture.
- DEA / DRA: Diameter Edge Agent or Routing Agent at the network border that routes S6a traffic.
- IPX provider: carries Diameter signalling and GTP user-plane traffic between operators.

## Home routed (HR)
The PGW is in the home network. User traffic goes from the visited SGW over the S8 interface (GTP)
across the IPX to the home PGW. Benefits: the home operator keeps control of policy, charging and
services. Downsides: extra latency and IPX transport cost. Home routing is the most common data
roaming architecture.

## Local breakout (LBO)
The PGW is in the visited network and traffic breaks out locally. This lowers latency, but it needs
agreements on charging and policy (for example S9 between PCRFs) and is less common.

## S8 Home Routing for VoLTE (S8HR)
For VoLTE roaming, S8HR routes the IMS APN traffic home over S8 like data. The IMS core, including the
P-CSCF, stays in the home network. This simplifies deployment because the visited network needs no IMS
roaming functions. Emergency calls and lawful interception need special handling.

## Interfaces to remember
| Interface | Between | Protocol | Purpose |
|---|---|---|---|
| S6a | Visited MME and home HSS | Diameter | Authentication, location update, subscription |
| S8 | Visited SGW and home PGW | GTPv2-C / GTP-U | Session control and user data (home routed) |
| S10 | MME and MME | GTPv2-C | Mobility between MMEs |
| Gp | Visited SGSN and home GGSN | GTPv1 | 2G/3G packet data roaming |

## Typical points of failure
- S6a: missing Diameter realm routes at the DEA or IPX, or peers not connected (results 3002 / 3003).
- S8: GTP tunnel creation fails because of firewall rules, wrong PGW IP ranges or DNS (APN FQDN
  resolution on the IPX).
- DNS: the APN-OI or PGW FQDN of the partner cannot be resolved on the GRX/IPX DNS.
