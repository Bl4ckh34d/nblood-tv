# Verification record

Publication verification: 2026-10-29. Windows, Android NDK r27d, Android 11 ARMv7 TV. The independent build and test-build scripts passed. The patch passed forward checks against a pristine index at the locked revision and reverse checks against the working source. The required Build modification notice is retained in the changed compatibility header. `verification.json` records the local binary hash; build timestamps and paths can prevent byte-identical results across rebuilds.

## Gameplay smoke test

Build with `python scripts/build_tests.py`. Upload `build/tests/blood_smoke` and the release core to a new directory under `/data/local/tmp` on an authorized Android device, and mark the executable with `chmod 755`. With absolute device paths:

```sh
./blood_smoke /data/local/tmp/your-test/core.so /path/to/Blood /data/local/tmp/your-test/saves --no-midi --resolution 320x200
```

Use your own complete Blood data and a separate disposable save directory. The test enters the first level and asserts keyboard and analog movement, horizontal and vertical aiming, native save/restore of position, L3/R3 slot-9 save/restore of position, live core-option updates, nonzero audio, changing rendered frames and Reset. It then unloads and deinitializes the core. The final publication build passed with 871 video frames, 573 distinct frames, 696800 PCM frames and 1142803 nonzero samples. MIDI was deliberately disabled in this check; it is not a MIDI verification.

The test frontend comes from the pinned upstream smoke test, with this repository's existing controller assertions and a CD-movie startup adaptation. The original startup sequence only pressed Confirm, then remained inside the optional episode movie. Both the previously installed build and the newly packaged build failed that sequence before gameplay. The published test sends Start during startup to skip the movie and passes with the same core; no runtime change was required to resolve this fixture failure. The test-state header's provenance is recorded in `vendored.json`.

The generic interactive probe also completed input, Reset and Close, but that run remained before gameplay and is not used as evidence of in-game success. Use the asserting movie-aware smoke test above for this data set. The generic probe's `--lifecycle` mode assumes same-module reload rejection and is not appropriate for NBlood's different reload contract.

Earlier tests in actual RetroArch checked native save/movement/fire/jump/load, Reset with Start to skip the movie, fast-forward and Close Content returning to RetroArch. The new publication pass runs in an isolated Android process and does not replace the installed production core or player saves. Neither test is a physical controller feel assessment or a guarantee of frame rate throughout the game. The earlier approximately 60 FPS observation is limited to its tested scene.
