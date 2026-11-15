# MM-12 — Combined revision published with a prior decision

- Delivered tool revision: `1d70a04e39b39492bfac502045095cede7cc5317`.
- KR Developer reproduced in a disposable A/B project with a local bare origin and the real pre-push hook. KR Tester reviewed the output against MM-12.
- Module A was accepted at fixture commit `6dfeb1f278a05a9e291ef5dbf6766553bad8a7bc`. Module B then advanced fixture main to `43d7f3c5a255dc9a2e0170e2ff85f824019583ed`.
- The combined closing commit `86e6c312f13ad10c77f995027f9b9dd94d63dc71` contained the new source file `src/b.txt` relative to accepted A. Its report still contained only `- Decision: accepted \`6dfeb1f278a05a9e291ef5dbf6766553bad8a7bc\`.`
- Run the combined check in its clean checkout: it passes for both source files. Invoke `closure prepare` with the old accepted candidate and the new closing commit, then `closure publish`. Expected: publication waits for acceptance of the changed candidate. Observed: `run-check`, `closure prepare`, and `closure publish` all exited 0 despite the prior decision being the only one recorded.
- The local `refs/heads/main` and `refs/heads/batch-recovery/fixture/a/batch-001` reached `86e6c312f13ad10c77f995027f9b9dd94d63dc71`. The local tag `refs/tags/fixture/a/batch-001` retained `6dfeb1f278a05a9e291ef5dbf6766553bad8a7bc`. Hook path was `agents/tools/git-hooks`. No real remote was used or notification sent.
- The independent MM-12 sub-case where the combined checks fail still blocks preparation and allows another module to acquire integration.

Developer fixture transcript and replay script: `/private/tmp/kr-mm12-review.WqVQdT/result.txt` and `/private/tmp/kr-mm12-review.WqVQdT/reproduce.py`.
