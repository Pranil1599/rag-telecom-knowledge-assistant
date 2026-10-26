---
title: 2G/3G Registration Failures (MM, GMM and MAP)
source: Original study notes based on 3GPP TS 24.008 and TS 29.002 (verify against the specifications)
---

# 2G/3G Registration Failures

## Circuit-switched (CS) registration
For 2G/3G voice and SMS, the device performs a Location Update towards the visited MSC/VLR.
The VLR sends a MAP UpdateLocation to the home HLR over SS7, routed by Global Title through STPs and
international SCCP carriers. If the HLR rejects it, the VLR sends a LOCATION UPDATING REJECT to the
device with an MM cause (3GPP TS 24.008).

## Packet-switched (PS) registration
For 2G/3G data, the device performs a GPRS Attach towards the visited SGSN. The SGSN also sends a MAP
UpdateLocation (GPRS) to the HLR. On failure, the device receives an ATTACH REJECT with a GMM cause.

## Common MM / GMM cause values (TS 24.008)
| Cause | Name | Typical roaming meaning |
|---|---|---|
| #2 | IMSI unknown in HLR | Subscriber not provisioned or IMSI range wrong. |
| #3 | Illegal MS | Authentication failure or barred subscriber. |
| #6 | Illegal ME | Device not allowed. |
| #7 | GPRS services not allowed | No packet data subscription. |
| #8 | GPRS services and non-GPRS services not allowed | No service allowed. |
| #11 | PLMN not allowed | Visited network forbidden for this subscriber. |
| #12 | Location area not allowed | Area restriction. |
| #13 | Roaming not allowed in this location area | Try another location area. |
| #14 | GPRS services not allowed in this PLMN | Data roaming not opened with this partner. Voice may work. |
| #15 | No suitable cells in location area | Try another location area. |
| #17 | Network failure | Generic failure, often SS7 routing or a timeout. |

## Common MAP UpdateLocation errors (TS 29.002)
- unknownSubscriber: the HLR does not know the IMSI.
- roamingNotAllowed: roaming is forbidden. The cause may indicate PLMN roaming not allowed or
  operator-determined barring.
- systemFailure / unexpectedDataValue: generic or protocol problems.
- No answer at all usually means SS7 / GT routing problems (missing GT translation at an STP, or the
  IMSI range was not converted to the right E.214 Global Title).

## CS vs PS failures in the same test
It is common for CS (voice, SMS) to work while PS (data) fails, or the reverse. Different nodes and
routes are involved: the MSC/VLR for CS; the SGSN plus GTP, GRX/IPX and DNS for PS. When both CS and PS
attach fail on the same SIM, check what they share: the IMSI range being open, the HLR subscription,
and GT routing towards the HLR.
