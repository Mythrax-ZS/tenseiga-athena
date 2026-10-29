# Samurai

Samurai is custom job **4500**, based on the Assassin Cross lineage, for the
sibling Rust **roclient** project. Server registration, statistics, equipment,
eight skills, status effects and the job trainer are included. The earlier
Ember Ronin body and matching katana assets are bundled with that client.

Source and staged Release/x64 binaries are provided in `build/samurai`.
The running executables in the repository root have **not** been replaced or
restarted. Deploy the client and server changes together during a coordinated
restart. Both **char-server and map-server must be updated together**:
`MAX_SKILL` increased from 1641 to 1649, changing their shared character data
layout. A full solution build produces a matching set of binaries.

This setup depends on the existing `MAX_LEVEL 999` setting and local packet
version **20250402**. The job's tracked data supplies base levels through 999
and job levels through 500 without depending on ignored local EXP overrides.
It copies the effective Assassin Cross EXP progression, original job bonuses
and level 1–99 HP/SP; later HP/SP use the server's existing formulas. The
two-handed sword base ASPD is 55.

For a fresh checkout, set `#define PACKETVER 20250402` in
`src/custom/defines_pre.hpp` before building to match this roclient setup.

## Installation and entry

Build `rAthena.sln` in **Release/x64**, staging outputs into `build/samurai`.
Keep the tracked `db/custom/samurai` files and footer imports in `db/*.yml`,
and the trainer entry in `npc/scripts_custom.conf`. No new SQL schema is
required. Local `db/import` overrides still load after the custom databases.

To activate the staged build, close the game client and gracefully stop the
login, char and map servers. Copy the matching `login-server.exe`,
`char-server.exe` and `map-server.exe` from `build/samurai` into the repository
root, then start them using your usual launcher. Launch the rebuilt
`roclient/target/release/ro-client.exe`. Do not replace only one side of the
char/map pair while the other still runs the old build.

Build the sibling roclient and include its `overlays/samurai` folder beside
the packaged client. See the client's
[`overlays/samurai/README.md`](../../../roclient/overlays/samurai/README.md)
for installation and artwork limits. This release supplies the male body;
female artwork, independently animated offhand weapons and stock headgear
attachments are not included. It does not patch a separate Gravity client.

The **Samurai Mentor** stands in **Prontera, 164,179**. Male Assassin Cross
characters require base level 99 and job level 70. They keep base level,
assigned stats, learned skills and unused skill points; Samurai job level
starts at 1 and job EXP resets to zero. Each character can claim one starter
katana. Administrators can also use `@jobchange 4500` for testing.

Samurai can equip daggers, one-handed swords, two-handed swords and katars.
Daggers and one-handed swords can be dual wielded; axes are rejected.
Assassin gear remains available, and swords also accept Swordman-family job
masks. Other level, sex and class-tier equipment restrictions still apply.

The starter **Samurai Initiate's Katana** is item **900000**,
`Samurai_Katana`: one-handed sword, 160 ATK, weapon level 3, weight 100,
minimum base level 99, refineable, no slots, Samurai only. Its client view is
2. A separate item job-mask bit keeps Samurai-only equipment from being
usable by Assassin Cross characters.

## Kusanagi and Muramasa

Two additional Samurai-only one-handed swords implement the **Divinity /
Kusanagi** and **Cursed / Muramasa** themes from the
[shared Samurai design conversation](https://chatgpt.com/share/6ae32624-5d04-83ea-97ca-d6037adb630c).
That conversation establishes precision, critical attacks and defensive SP
techniques for Kusanagi, and bloodletting, risk and low-HP attacks for Muramasa.
The deeper project backstory was unavailable; these are initial gameplay
interpretations of those themes, not additional canon.

| Item | ID / Aegis name | ATK | Weight | Effects |
| --- | --- | --- | --- | --- |
| Kusanagi | 900001 / `Samurai_Kusanagi` | 190 | 100 | HIT +15, CRIT +8, Max SP +5%; Heaven's Severance damage +10%; Kusanagi Guard and Moonlit Reflection SP costs -15%. |
| Muramasa | 900002 / `Samurai_Muramasa` | 210 | 120 | CRIT +5, Max HP -5%; Ashen Wind Slash and Wrath Unbound damage +10%; melee physical hits have a 3% chance to inflict Bleeding for up to 5 seconds. |

Both are neutral, weapon level 4, require base level 99, have one card slot,
and can be refined. They can be equipped in either hand or paired together.
Bleeding can be resisted or shortened by the target's normal status defenses;
the proc includes melee weapon skills as well as normal attacks. Multiple
copies add their bonuses and penalties. No extra pair bonus, life-steal or
recurring weapon HP drain is applied. They use the existing Samurai skills
without changing those skills' HP requirements or cooldowns.

Administrators can create them with `@item 900001 1` and `@item 900002 1`.
No quest or drop acquisition is assigned yet. Their unique Aegis names avoid
the existing two-handed stock Muramasa items (1164, 1173 and 21003), which
remain unchanged. Client appearance aliases are 9001 and 9002; the modern
server packets send the actual 900001/900002 item IDs, and client item metadata
selects the corresponding custom appearance. These are first playable balance
values, including for the local base-999 progression, pending playtesting.

## Skills and balance

All eight skills have five levels, require an allowed weapon, and have a
0.3-second after-cast delay. The two branches are 7001 → 7002 → 7003 → 7004
and 7005 → 7006 → 7007 → 7008; each arrow requires level 3 of the preceding
skill. Novice, Thief, Assassin and Assassin Cross skills are inherited.

Values below show skill levels 1 through 5. Damage is an ATK ratio before
the normal combat pipeline applies defenses and modifiers.

| ID | Skill | Effect | SP / cooldown |
| --- | --- | --- | --- |
| 7001 | Heaven's Severance | One target, 400/500/600/700/800% damage; +25/30/35/40/45 percentage points of critical chance. | 25 / 2 s |
| 7002 | Kusanagi Guard | 25/30/35/40/45% physical parry chance for 12 seconds. | 30 / 20 s |
| 7003 | Moonlit Reflection | For 8 seconds, block the next physical skill; return 50/60/70/80/90% damage and restore 2/3/4/5/6% max SP. A positive incoming hit returns at least 1 damage. | 35 / 18 s |
| 7004 | Blade Harmony | +10/20/30/40/50 HIT and +1/2/3/4/5 ASPD for 20 seconds. | 30 / 25 s |
| 7005 | Blood Covenant | Pay 10% max HP; next three normal attack attempts gain 30/40/50/60/70% damage. Charges expire after 30 seconds. | 20 / 12 s |
| 7006 | Muramasa's Curse | +15/20/25/30/35% attack for 20 seconds; drains 1% max HP per second and ends before a drain would kill the caster. | 35 / 25 s |
| 7007 | Ashen Wind Slash | Radius 3, 300/400/500/600/700% damage; 15/20/25/30/35% chance of 10-second Bleeding. | 30 / 4 s |
| 7008 | Wrath Unbound | One target, 800/1000/1200/1400/1600% damage; HP must be strictly below 30% of maximum. | 50 / 15 s |

Client buff IDs **2000–2004** correspond to Guard, Reflection, Harmony,
Covenant and Curse. These temporary effects are not saved through logout
and end when the required weapon is unequipped.

## Verification

The full Release/x64 server solution builds successfully. An isolated
`map-server --run-once` loads the custom item, job statistics, skill tree,
eight skills, five statuses and trainer, reaches ready, and exits with zero
errors or warnings. Its logs are under `build/samurai-test`.

The companion headless client harness logs into a separate three-server
stack as an eligible Assassin Cross with an empty inventory and zero weight.
It completes the real mentor dialogue, checks job 4500 and the starter katana,
and verifies both reward paths reject repeat claims. It then tests learning the eight skills, dual equipment,
buff activation/expiry, HIT/ASPD updates, HP/SP effects, three Covenant
attacks, damage and Wrath's strict HP boundary. This tests network and
combat behavior without opening the game GUI or using a production account.
The legendary-weapon extension verifies Kusanagi's HIT, CRIT and Max SP,
Muramasa's CRIT and Max HP penalty, both orders of dual equipment, and exact
restoration after unequipping. Actual Guard/Reflection SP deductions with
Kusanagi are 25/29, down from 30/35. The randomized Bleeding frequency and
skill-specific percentage damage bonuses are not statistically measured by
this fixture; their item scripts load successfully through the normal engine.
Reproduction and fixture details are in
[`tools/tests/samurai/README.md`](../../tools/tests/samurai/README.md).

Animated client previews are separate from these gameplay checks. The
illustrated source assets provide limited poses; the client's asset README
describes the animation coverage. The eight-skill balance is an initial
playable configuration, not a completed PvP/PvE balance pass.
