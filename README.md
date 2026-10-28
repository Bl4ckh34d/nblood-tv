# NBlood â€” Android TV libretro integration

Android ARMv7 build and controller improvements for the NBlood libretro port. Designed for 32-bit RetroArch on Android TV, with native execution, dual-stick aiming, native quicksave/load and reliable movie input.

## Build

The supported build host is Windows with Python 3.10+, Git for Windows and Android NDK r27d. Output is ARMv7 for 32-bit RetroArch, not arm64. Set `ANDROID_NDK_HOME` to the NDK directory if it is not `C:/tools/android/android-ndk-r27d`.

```powershell
python scripts/fetch_sources.py
python scripts/build_nblood_tv.py
```

`dependencies.json` locks each upstream revision and patch hash. `vendored.json` records the provenance and SHA-256 of copied headers. Fetching and building refuse a different checkout revision or origin and never reset existing work. Builds apply the recorded patches if needed. `PORT_SOURCES_DIR` can point to an existing source directory with exactly these dependencies. Additional local edits are preserved; a clean pinned checkout plus the patches is required to reproduce the published source state.

The resulting library is `release/blood_libretro_android.so`. Generated sources, objects, binaries and logs are ignored. No original game data or player saves are included.

## RetroArch setup

Install the resulting core into a 32-bit Android RetroArch installation using its supported core installation mechanism. Put your own game files in a readable directory; choose a separate writable save directory. `profiles/android-example.json` contains a playlist entry and per-game configuration/remap examples. Replace `YOUR_USB_ID` and adapt the paths and app package for your device. It is a reference profile, not an automatic installer.

The Xbox labels below match the tested TV mapping. Configure physical L2 as RetroArch fast-forward. Leave L3/R3 unbound from RetroArch generic Save State/Load State: the core handles native game saves on those buttons. Guide opens the RetroArch Quick Menu. Reset restarts the engine; Close Content returns to RetroArch. Fast-forward has no fixed multiplier and depends on CPU capacity. Native saves are separate from generic serialized RetroArch save states, which these cores do not implement.

Preview images belong in RetroArch's thumbnail folders under the playlist name, using the exact entry label. Screenshots and commercial cover art are not part of this source repository.

## Verification

See [verification notes](docs/verification.md) for the recorded checks and their limits. `tests/native_probe.cpp` is a small Android libretro host for isolated video/audio, input and lifecycle checks. Tests must use a separate writable save directory. Its `--lifecycle` mode is specifically for cores that reject a second load into the same module; it is not a universal core compliance test.

Git for Windows supplies the POSIX build tools. The default shell is `C:/Progra~1/Git/bin/sh.exe`; override `GIT_SH` if needed. Its `usr/bin` and `bin` tools must be available on PATH for a non-default installation. The upstream `TESTS=1` build includes a diagnostic state API used by the upstream smoke-test frontend. Normal play is driven by RetroArch input.

## Game data

Load `BLOOD.INI` from your own Blood 1.11 data set, alongside `BLOOD.RFF`, `SOUNDS.RFF`, ART files and the other original assets. Supply the matching upstream `nblood.pk3` support archive as required by NBlood (the build copies it into `build/nblood-tv`). Preserve CD music and movie files and their INI paths if those features are wanted. No original files or support archive binaries are included here.

A writable save directory is required. Set both `savefiles_in_content_dir` and `savestates_in_content_dir` to false, as in the example. An unwritable USB content directory can otherwise leave startup black.

## Changes

* ARM-safe access to unaligned 32/64-bit data in the Build engine.
* Xbox-oriented input descriptors and mapping, including native F6/F9 quicksave/load on L3/R3 using slot 9.
* L2 reserved for the frontend; right-stick free aim and non-inverted vertical look.
* Movie input is consumed before the 24 FPS presentation gate and cleared before yielding, so short Start presses can skip movies reliably.

## Controller

Left stick moves, right stick aims. A jumps, B crouches, X activates, Y uses alternate fire. R2 fires; LB/RB change weapons. View opens the map, Start opens the menu or skips a movie. D-pad handles inventory and centering the view. L3 saves and R3 loads native slot 9. Reset restarts the game/movie flow; press Start to skip, then load the native save.

## Licensing and provenance

The root GPL-2.0 license applies to GPL-covered changes, not as a blanket relicense of every upstream component. NBlood/EDuke32 and the original Build engine have distinct terms. The Build license and libsmacker notice are preserved in `licenses/`; all other original notices remain in the fetched pinned source.

"Build Engine & Tools" Copyright (c) 1993-1997 Ken Silverman. Ken Silverman's official web site: http://www.advsys.net/ken . See `licenses/BUILDLIC.TXT` for its license terms. Modified upstream files and this patch set retain the relevant author notices. The vendored libretro API header retains its own MIT notice.
