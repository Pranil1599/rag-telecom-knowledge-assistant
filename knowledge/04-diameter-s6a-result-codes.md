---
title: Diameter S6a Result Codes for LTE Roaming
source: Original study notes based on IETF RFC 6733 and 3GPP TS 29.272 (verify against the specifications)
---

# Diameter S6a Result Codes

S6a is the Diameter interface between the visited network's MME and the home network's HSS.
It is specified in 3GPP TS 29.272. In roaming, S6a messages usually pass through the visited network's
DEA (Diameter Edge Agent), the IPX provider's Diameter routing, and the home network's DEA.

## Main S6a procedures
- AIR / AIA (Authentication-Information-Request / Answer): fetch authentication vectors.
- ULR / ULA (Update-Location-Request / Answer): register the subscriber in the visited MME and
  download the subscription profile.
- CLR / CLA (Cancel-Location): the HSS removes the subscriber from an old MME.
- PUR / PUA (Purge-UE) and IDR / IDA (Insert-Subscriber-Data) for later updates.

## Base Diameter result codes (Result-Code AVP)
| Code | Name | Meaning |
|---|---|---|
| 2001 | DIAMETER_SUCCESS | Request succeeded. |
| 3002 | DIAMETER_UNABLE_TO_DELIVER | Agent could not route the request to the destination. This points to routing or peer problems. |
| 3003 | DIAMETER_REALM_NOT_SERVED | Destination realm unknown to the routing agent. |
| 3004 | DIAMETER_TOO_BUSY | Peer overloaded. |
| 5012 | DIAMETER_UNABLE_TO_COMPLY | Generic failure. |

## S6a specific codes (Experimental-Result-Code AVP)
| Code | Name | Meaning |
|---|---|---|
| 4181 | DIAMETER_AUTHENTICATION_DATA_UNAVAILABLE | HSS temporarily cannot provide authentication vectors. |
| 5001 | DIAMETER_ERROR_USER_UNKNOWN | IMSI not known in the HSS. |
| 5004 | DIAMETER_ERROR_ROAMING_NOT_ALLOWED | Subscriber not allowed to roam in the visited PLMN (subscription or operator-determined barring). |
| 5420 | DIAMETER_ERROR_UNKNOWN_EPS_SUBSCRIPTION | Subscriber has no EPS (LTE) subscription. |
| 5421 | DIAMETER_ERROR_RAT_NOT_ALLOWED | The radio access type is not allowed for this subscriber. |
| 5422 | DIAMETER_ERROR_EQUIPMENT_UNKNOWN | Device identity check failed. |

## Troubleshooting hints
- 3002 or 3003 during roaming tests usually means a missing Diameter realm route at the DEA or IPX.
  The partner's realm is normally of the form epc.mnc<MNC>.mcc<MCC>.3gppnetwork.org.
- 5004 in a ULA means the home HSS refused roaming. Check the subscriber profile, roaming restrictions
  and whether LTE roaming is enabled for that partner.
- The visited MME converts the S6a result into an EMM cause for the device. The exact mapping depends
  on configuration and on TS 29.272 / TS 24.301.
