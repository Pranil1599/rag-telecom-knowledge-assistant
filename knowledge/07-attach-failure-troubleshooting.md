---
title: Troubleshooting Checklist for Roaming Attach Failures
source: Original study notes (generic practice, adapt to your network)
---

# Troubleshooting Checklist: Roaming Attach Failures

Use this when a test SIM cannot register or attach on a partner network during IREG testing.

## Step 1: Collect facts
- Test SIM IMSI, MSISDN, and which network it belongs to (home or partner).
- Direction: outbound (our SIM abroad) or inbound (partner SIM on our network).
- What fails: CS (voice/SMS), PS (data), LTE, or all of them.
- Reject cause seen on the device or in traces (MM, GMM, EMM or ESM cause), plus any MAP error or
  Diameter result code.
- Timestamps, so both operators can match traces.

## Step 2: Check the basics both sides share
1. Is the test SIM's IMSI range opened for roaming in the visited network (VLR, SGSN, MME roaming tables)?
2. Is the subscriber provisioned with roaming allowed on the HLR / HSS (no operator-determined barring)?
3. Are both operators using the latest IR.21 of each other?

## Step 3: CS / 2G-3G registration
- Trace the MAP UpdateLocation. If there is no answer, check Global Title translation at the STPs and
  the international SCCP carrier routes for the HLR GT.
- A MAP roamingNotAllowed or unknownSubscriber answer means the home HLR rejected it. Ask the home
  operator to check the subscription.

## Step 4: PS / data
- GMM #14: data roaming is not opened for this partner.
- Attach succeeds but no data: check the APN, DNS resolution on the GRX/IPX, the GTP firewall and the
  GGSN/PGW IP ranges from the IR.21.

## Step 5: LTE
- Trace S6a AIR/ULR. Result 3002/3003 points to Diameter routing (DEA, IPX realm routes).
  Result 5004 means the HSS refused roaming. Result 5420 means no EPS subscription.
- EMM #14 means LTE roaming is not opened, while 2G/3G may still work.
- EMM #19 + ESM #27 means an APN / DNS problem on the S8 side.

## Step 6: When both CS and PS attach fail
If CS and PS both fail on the same SIM, focus on what they share: the IMSI range, the HLR/HSS
subscription and roaming flags, and signalling routing towards the home network (GT routing for MAP,
realm routing for Diameter). Fixing one shared item often fixes both.

## Step 7: Close the loop
- Retest each failed case and record PASS / FAIL with the trace reference.
- Update the IREG test report and inform the partner of any configuration changed.
