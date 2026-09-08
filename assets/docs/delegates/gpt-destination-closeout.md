# GPT destination closeout

Date: 2026-09-08

## Scope

Rechecked the four previously reported public GPT destination failures from
Actions run `34216855746`: BRG02 Starbucks, BRG05 Costco, BRG07 LVMH, and
BRG09 Coca-Cola. Used public source access only.

## Evidence

- `scripts/check-public-gpt-links.py` already classifies destination outcomes
  as `reachable`, `authentication_or_private`, `broken_or_unpublished`,
  `transient_service`, or `transient_network`.
- The script treats HTTP 404 and 410 as `broken_or_unpublished`, which is the
  correct fallback for unavailable public destinations.
- The archived probe evidence in
  `assets/docs/assessment-2026-09-05/evidence/public-gpt-probe.txt` records
  BRG02, BRG05, BRG07, and BRG09 as `broken_or_unpublished: HTTP 404`.
- A live rerun with `python3 scripts/check-public-gpt-links.py --timeout 12
  --retries 1` produced the same result for all four destinations.

## Conclusion

No repository code defect was found in the destination checker. The failure
mode is already handled correctly as an unavailable or unpublished public GPT
page, not as an auth or transient error.

## Follow-up

If the owner wants these four to become reachable again, the missing action is
on the provider side: the public ChatGPT destination URLs need to resolve to
live pages. No local repository edit can manufacture that state.
