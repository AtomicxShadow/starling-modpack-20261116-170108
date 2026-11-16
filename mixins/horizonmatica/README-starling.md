Experimental Horizonmatica port for Starling 0.8.0.
Changes: play_mouse and pauses_game injection targets point to game.rs.
The original Horizon revision records the upstream source base; Starling's
native_build.sh replaces bundle pins with the app's own revision.
This mod still uses game internals, so it does not declare hooks-only compatibility.
Package validation is not an Android compile or runtime test.
Horizon Android 0.7.8 has not been verified.
