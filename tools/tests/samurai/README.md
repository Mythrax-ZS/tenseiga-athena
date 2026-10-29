# Isolated Samurai integration fixture

This Windows fixture starts its own MariaDB container and three server processes.
It copies data/configuration into `build/samurai-test/runtime`; it never connects
to the production database or replaces running server executables.

Prerequisites: Python 3, Git, Docker Desktop with Linux containers, the
`mariadb:11` image, and a full Release/x64 solution build in `build/samurai`.
The repository root must contain its normal `libmysql.dll`, `pcre8.dll` and
`zlib.dll`. Build with the configured packet version **20250402** and
`MAX_LEVEL 999`. The companion Rust client harness uses that packet version.

From the rAthena repository root:

```powershell
py tools/tests/samurai/setup.py setup
py tools/tests/samurai/setup.py run-once
py tools/tests/samurai/setup.py start
```

From the sibling roclient repository:

```powershell
cargo run -p ro-net --example samurai_integration
```

The harness verifies the advertised loopback endpoints before proceeding.
Reserved ports are login **55120**, char **55121**, map **55122** and MariaDB
**33317**. They must be free before setup. The disposable account is
`samurai_test` / `samurai-test-only`; it is never created on production.

After the harness exits, stop this fixture:

```powershell
py tools/tests/samurai/setup.py stop
```

Stop checks each process's actual executable path against the isolated runtime
path and checks the database container's ownership label. It retains logs and
the isolated database directory for inspection. To repeat from the original
character state, run `stop`, then `setup`, `run-once` and `start` again. Setup
resets only fixture character `150000` and account `2000001` inside that
container. Do not run setup while the harness is connected.

`fixture.sql` creates a male Assassin Cross with base 99/job 70, the inherited
basic skills, 49 unused skill points, and an empty inventory at Prontera 161,179.
The harness completes the real Samurai Mentor dialogue, checks job level 1 and
one starter katana, and revisits to verify that the reward cannot be duplicated.
It also clears the claim flag and katana in this isolated fixture to verify
the already-Samurai reward path and its repeat-claim protection.
It then creates one test dagger with `@item 1201 1` for the dual-wield checks.
The eight custom skills begin unlearned. The admin group can issue commands but cannot
bypass skill or equipment rules.

`fixture_npc.txt` is loaded only by the copied runtime and defines:

| Command | Purpose |
| --- | --- |
| `@samuraimentor` | Report the production mentor GID if its name was not present in the spawn packet. |
| `@samurairewardreset` | Delete the isolated tester's katana and clear its claim flag to exercise the unclaimed reward branch. |
| `@samuraidummy` | Create a stationary, nonaggressive target with 100 million HP; report its GID. |
| `@samuraihit` | Make that target cast Bash 5 at the tester. |
| `@samurailowhp` | Set HP to one quarter of maximum. |
| `@samurai30hp` | Set HP to the ceiling of 30% of maximum, testing the strict boundary. |
| `@samuraireset` | Remove the five Samurai buffs and restore HP/SP; cooldowns remain. |

Logs are `build/samurai-test/map-run-once.log` and
`build/samurai-test/{login-server,char-server,map-server}.log`.
The client harness writes its results to standard output. No game GUI opens.
