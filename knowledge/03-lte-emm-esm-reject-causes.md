---
title: LTE Attach Reject Causes (EMM and ESM)
source: Original study notes based on 3GPP TS 24.301 cause values (verify against the specification)
---

# LTE Attach Reject Causes

When an LTE attach fails, the MME sends an ATTACH REJECT to the device with an EMM cause value.
These are defined in 3GPP TS 24.301 (NAS protocol for EPS). If the attach fails because the default
bearer (PDN connection) could not be set up, the reject carries EMM cause #19 "ESM failure" and an
ESM cause that explains the bearer problem.

## Frequently seen EMM cause values
| Cause | Name | Typical roaming meaning |
|---|---|---|
| #2 | IMSI unknown in HSS | HSS does not know the subscriber or the IMSI range is wrong. |
| #3 | Illegal UE | Authentication failure or subscriber barred. |
| #6 | Illegal ME | Device (IMEI) not allowed. |
| #7 | EPS services not allowed | Subscriber has no LTE subscription. |
| #8 | EPS services and non-EPS services not allowed | Subscriber not allowed any service. |
| #11 | PLMN not allowed | Visited network not allowed for this subscriber; device should not retry this PLMN. |
| #12 | Tracking area not allowed | Area restriction. |
| #13 | Roaming not allowed in this tracking area | Device may try another tracking area or PLMN. |
| #14 | EPS services not allowed in this PLMN | LTE roaming not opened with this partner, but 2G/3G may work. |
| #15 | No suitable cells in tracking area | Device should look for another tracking area. |
| #17 | Network failure | Generic failure, often a timeout towards the HSS or a routing problem. |
| #19 | ESM failure | Default bearer could not be set up; look at the ESM cause. |
| #22 | Congestion | Network overload. |

## Frequently seen ESM cause values
| Cause | Name | Typical roaming meaning |
|---|---|---|
| #27 | Missing or unknown APN | APN not provisioned or DNS cannot resolve it. |
| #29 | User authentication failed | Authentication at the PGW / AAA failed. |
| #31 | Request rejected, unspecified | Generic rejection by the PGW. |
| #33 | Requested service option not subscribed | APN or service not in the subscriber profile. |

## Practical reading of causes during IREG testing
- Cause #14 on a test SIM usually means LTE roaming is not yet opened for that partner in the HSS or
  in the MME roaming configuration. 2G/3G service may still be working.
- Cause #19 with ESM #27 points to APN / DNS / IPX problems, not to subscription.
- Cause #17 often comes from Diameter routing problems (for example the S6a request never reaches
  the HSS) or from timeouts.
