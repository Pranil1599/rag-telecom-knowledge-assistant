---
title: IREG Roaming Testing Overview
source: Original study notes (verify details against the official GSMA documents)
---

# IREG Roaming Testing Overview

## What IREG testing is
IREG (Interworking and Roaming Expert Group) tests are end-to-end functional tests run between two
mobile operators before a roaming relationship is opened commercially, and again when a new service
(for example LTE or VoLTE roaming) or a major network change is introduced. The goal is to prove that a
subscriber of the home network (HPMN) can register and use services on the visited network (VPMN).

IREG tests prove technical interworking. They are normally followed by TADIG testing, which proves that
billing records (TAP files) are produced and exchanged correctly. A partner is usually launched
commercially only after both IREG and TADIG testing pass.

## Main GSMA test specifications
- IR.23: organisation of international roaming tests (process, roles, test SIM exchange).
- IR.24: end-to-end functional tests for GSM (circuit-switched voice, SMS, supplementary services).
- IR.35: end-to-end functional tests for GPRS / packet-switched data.
- IR.38: LTE and EPC roaming testing (LTE attach, data sessions, related procedures).
- IR.88 is not a test specification: it is the LTE and EPC Roaming Guidelines that IR.38 tests build on.

## Inbound vs outbound testing
- Outbound roaming: our (home) subscribers roaming on the partner network. Our test SIMs are sent to,
  or are used in, the partner's network.
- Inbound roaming: the partner's subscribers roaming on our network. The partner's test SIMs are
  used in our network.
Each direction is tested separately because different elements and configuration are involved.

## Typical test flow
1. Exchange and validate IR.21 data (network codes, Global Titles, IMSI ranges, IP ranges, APNs, Diameter realms).
2. Exchange test SIM cards (or eSIM test profiles) and agree the test window.
3. Configure both networks: open IMSI ranges, update STP/DRA/DEA routing, GT and Diameter peer routing,
   firewall and IPX settings, APN and DNS records.
4. Run the test cases: location update / attach, mobile-originated and mobile-terminated calls and SMS,
   data sessions, supplementary services, CAMEL where used.
5. Record PASS / FAIL per case with traces for each failure, fix, and re-test.
6. Sign off the IREG test report, then move to TADIG testing and commercial launch.

## Typical LTE (IR.38) test cases
- LTE attach and detach, including authentication via S6a.
- Default bearer establishment on the roaming APN, with home routing (S8) or local breakout.
- Data session: browsing / throughput checks.
- Tracking area update and idle-to-connected transitions.
- Fallback to 2G/3G where LTE is not available.

## Common reasons tests fail
- IMSI range of the test SIM not opened in the visited network.
- Wrong or missing GT / Diameter realm routing at the STP, DRA or IPX provider.
- APN or DNS (GRX/IPX) misconfiguration, so the PDN connection cannot be set up.
- Roaming not allowed by subscription (operator-determined barring) on the HLR / HSS.
- Firewall rules on the GTP or Diameter interfaces blocking traffic.
