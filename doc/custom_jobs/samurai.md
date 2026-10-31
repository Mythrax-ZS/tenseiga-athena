# Samurai

Samurai is custom job **4500**, based on the Assassin Cross lineage, for the
sibling Rust **roclient** project. Server registration, statistics, equipment,
fourteen skills (eight, plus Tenseiga's six-skill Mortal Flame line), status
effects and the job trainer are included. The earlier
Ember Ronin body and matching katana assets are bundled with that client.

Source and staged Release/x64 binaries are provided in `build/samurai`.
The running executables in the repository root have **not** been replaced or
restarted. Deploy the client and server changes together during a coordinated
restart. Both **char-server and map-server must be updated together**:
`MAX_SKILL` increased from 1641 to 1656 (one per Samurai skill),
changing their shared character data layout. A full solution build produces a matching set of binaries.

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
Their story comes from the user's *Twin Flames Saga*
([shared conversation](https://chatgpt.com/share/6ae3ebdd-c980-83ea-9535-f1e502f87ea0)):
Kusanagi-no-Tsurugi and Muramasa are the two halves of the goddess
Amaterasu-no-Mikazuki's divided flame. Muramasa was forged through the dark god
Kagutsuchi-no-Yami, who tricked the grieving Hayate Yoshida into wielding it;
Kusanagi was sealed by the goddess and freed by Tetsuya Takahashi's Sarugami
blood. Hayate defies both gods by fusing the blades into Tenseiga-no-Hayate.

| Item | ID / Aegis name | ATK | Weight | Effects |
| --- | --- | --- | --- | --- |
| Kusanagi | 900001 / `Samurai_Kusanagi` | 190 | 100 | HIT +15, CRIT +8, Max SP +5%; Heaven's Severance damage +10%; Kusanagi Guard and Moonlit Reflection SP costs -15%. |
| Muramasa | 900002 / `Samurai_Muramasa` | 210 | 120 | CRIT +5, Max HP -5%; Ashen Wind Slash and Wrath Unbound damage +10%; melee physical hits have a 3% chance to inflict Bleeding for up to 5 seconds. |

Both are neutral, weapon level 4, require base level 99, have one card slot,
and can be refined. They can be equipped in either hand or paired together.
Bleeding can be resisted or shortened by the target's normal status defenses;
the proc includes melee weapon skills as well as normal attacks. Multiple
copies add their bonuses and penalties. No life-steal or recurring weapon HP
drain is applied.

### Twin Flames (Kusanagi and Muramasa dual wielded)

Kusanagi's script adds a pair bonus when one hand holds Kusanagi and the other
Muramasa, in either order. In the story, the two halves of the goddess's flame
held together in mortal hands, so that neither god's chain holds: the step before
Tenseiga. It uses only bonuses that apply regardless of which hand runs the script.

| Effect | Story |
| --- | --- |
| Max HP +5% (cancels Muramasa's toll); immune to Curse and Bleeding | Kusanagi's light quiets Muramasa's hunger |
| Ignore 25% DEF of Angel and Demon; 10% less damage from them | Defiance of the goddess's host and Yami's demons |
| Heaven's Severance, Ashen Wind Slash and Wrath Unbound damage +15% | Each path feeds the other |
| Mortal Flame: 3% on a weapon hit, 6 s of ASPD +10%, critical damage +25%, ignore 20% DEF of all races (Izayoi effect) | The blades burn as one, Tenseiga's echo | They use the existing Samurai skills
without changing those skills' HP requirements or cooldowns.

Administrators can create them with `@item 900001 1` and `@item 900002 1`.
No drop is assigned: the Twin Flames Saga gives them, Muramasa in Chapter I and Kusanagi in
Chapter V ([twin_flames.md](twin_flames.md)), and Masaru reforges the pair into Tenseiga
(below). Their unique Aegis names avoid
the existing two-handed stock Muramasa items (1164, 1173 and 21003), which
remain unchanged. Client appearance aliases are 9001 and 9002; the modern
server packets send the actual 900001/900002 item IDs, and client item metadata
selects the corresponding custom appearance. These are first playable balance
values, including for the local base-999 progression, pending playtesting.

## Tenseiga-no-Hayate

In the saga's secret thirteenth chapter, Hayate defies both the goddess and
Yami: at the First Forge he shatters Kusanagi and Muramasa and reforges them into
**Tenseiga-no-Hayate, the Mortal Flame**, "not a relic of gods, but the first
true sword of men". Masaru, descendant of the smith who forged Muramasa, works
the forge; Kohaku's foxfire lights it, Tetsuya adds his Sarugami blood, and each
companion adds a relic.

Tenseiga is item **900003**, `Samurai_Tenseiga`: Samurai-only **two-handed**
sword, 420 ATK, weapon level 4, weight 150, two slots, minimum base level 99,
refineable, Neutral. Client view 9003. Its script maps the forging to bonuses:

| Effect | Story |
| --- | --- |
| HIT +20, CRIT +15; Heaven's Severance, Ashen Wind Slash and Wrath Unbound damage +20%; Kusanagi Guard and Moonlit Reflection SP costs -15%; 3% Bleeding on melee hits | Both blades live on in it: Kusanagi's precision, Muramasa's bite |
| Max HP +5%, Max SP +5% | Tetsuya's Sarugami essence: balance |
| +20% damage to Angel and Demon; ignore 50% of their DEF | Kohaku's foxfire: an edge that severs divine essence |
| 15% less damage from Angel monsters and Holy attacks | Brother Renga's prayer beads: resistance to divine influence |
| 15% less damage from Demon monsters; immune to Curse and Bleeding | Kiyoshi's crest: clarity against corruption; Muramasa's toll is gone |
| Immune to Blind and Confusion | Ayame's purified kunai (deception) and Lady Hanae's jade (manipulation) |
| 20% perfect hit (ignores Flee) | Chiyo's broken talisman: it cuts through illusions |
| 10% less damage from Fire and Water attacks | Taro and Jiro's twin sigils of fire and water |
| Physical damage +1% per refine level | Masaru's forge technique |
| Mortal Flame: 5% on a weapon hit, 8 s of ASPD +15%, critical damage +30%, ignore 30% DEF of all races (Izayoi effect) | Human will burns hotter than any god's fire |

While Tenseiga is equipped its wielder wears the **Mortal Flame aura**, in the
blade's colours: crimson to violet ribbons climbing around them, crimson and cyan
starbursts turning on the ground like its guard, and magenta, cyan and violet
sparks rising (the runes, the edge and the body) over a dark indigo pool. The
equip and unequip scripts turn on custom hat effect `HAT_EF_SAMURAI_TENSEIGA`
(id 2000, added after the official ids in `src/map/script.hpp`), so the server
shows it to everyone nearby and restores it on login. roclient draws it in code;
clients that don't know the id show nothing.

Tenseiga is forged in Chapter X of the Twin Flames Saga ([twin_flames.md](twin_flames.md)),
at the First Forge (Magma Dungeon 2, `Masaru#forge` in `npc/custom/twin_flames/tf_ch07_10.txt`).
A Samurai dual wielding Kusanagi and Muramasa (either hand order) brings the eight companions'
relics, Tetsuya's Sarugami Essence, **10 Oridecon** and **10 Burning Hearts**. Cards must be
removed first; the new blade takes the lower of the two refine levels. After the forging scene
the blades, relics and materials are consumed, Tenseiga is given, `SamuraiTenseigaForged` is set
and the forging is announced server-wide. **Masaru** in **Prontera, 161,179**, beside the Samurai
Mentor (`npc/custom/samurai_tenseiga.txt`), is the saga's Chapter VII smith; he no longer forges
on request. Administrators can also use `@item 900003 1`.

## Skills and balance

All eight skills have five levels, require an allowed weapon, and have a
0.3-second after-cast delay. The two branches are 7001 → 7002 → 7003 → 7004
and 7005 → 7006 → 7007 → 7008; each arrow requires level 3 of the preceding
skill. Novice, Thief, Assassin and Assassin Cross skills are inherited.

Values below show skill levels 1 through 5. Damage is an ATK ratio before
the normal combat pipeline applies defenses and modifiers.

The skills are balanced against 4th-job skills. Damage takes the 4th-job shape:
the ratio replaces the base 100% and is multiplied by base level / 100 above
level 99, as `RE_LVL_DMOD(100)` does for 4th jobs (×9.99 at level 999). Samurai
is not a trait job (no POW, P.ATK or C.RATE), so its ratios are set higher to
carry what those add to a 4th job's skills. At level 999 the spammable
Heaven's Severance sits between Eternal Slash and Abyss Dagger, and Wrath
Unbound and Destiny's Severance sit near Madness Crusher and Rush Quake.
Measured on Dummy 150 (DEF 120) at level 999: Heaven's Severance Lv 5 hits for
about 2.57 million, Destiny's Severance Lv 5 for about 18.7 million.

| ID | Skill | Effect | SP / cooldown |
| --- | --- | --- | --- |
| 7001 | Heaven's Severance | One target, 1700/2600/3500/4400/5300% × base level / 100; +25/30/35/40/45 percentage points of critical chance. | 60 / 0.7 s |
| 7002 | Kusanagi Guard | 30/35/40/45/50% physical parry chance for 30 seconds. | 40 / 30 s |
| 7003 | Moonlit Reflection | For 15 seconds, block the next physical skill; return 100/150/200/250/300% damage and restore 5/6/7/8/9% max SP. A positive incoming hit returns at least 1 damage. | 45 / 15 s |
| 7004 | Blade Harmony | +20/40/60/80/100 HIT, +1/2/3/4/5 ASPD and +4/8/12/16/20% ATK for 60 seconds. | 50 / 60 s |
| 7005 | Blood Covenant | Pay 10% max HP; next three normal attack attempts gain 60/120/180/240/300% damage. Charges expire after 30 seconds. | 30 / 12 s |
| 7006 | Muramasa's Curse | +12/24/36/48/60% attack for 30 seconds; drains 1% max HP per second and ends before a drain would kill the caster. | 50 / 30 s |
| 7007 | Ashen Wind Slash | Radius 3, 1300/2000/2700/3400/4100% × base level / 100; 15/20/25/30/35% chance of 10-second Bleeding. | 70 / 1 s |
| 7008 | Wrath Unbound | One target, 7000/11000/15000/19000/23000% × base level / 100; HP must be strictly below 30% of maximum. | 100 / 15 s |

Client buff IDs **2000–2004** correspond to Guard, Reflection, Harmony,
Covenant and Curse. These temporary effects are not saved through logout
and end when the required weapon is unequipped.

### The Mortal Flame line (Tenseiga)

Chapter 13 of the saga ends with Tenseiga "unleashing abilities that cut
through both light and shadow". Its techniques form a third line, unlocked by
the same questline as Tenseiga:

- **Mortal Flame** (7009) is a quest skill (`IsQuest`): skill points cannot
  raise it, since `quest_skill_learn` stays off. The questline grants it with
  `skill "SAM_MORTAL_FLAME",1,SKILL_PERM;` when Tenseiga is forged in Chapter X. Masaru in
  Prontera also grants it to anyone who forged Tenseiga before the saga existed
  (`SamuraiTenseigaForged`).
- The other six need Mortal Flame in the skill tree, and can be used only
  while **Tenseiga** (900003) is wielded (`skill_check_samurai_tenseiga` in
  `src/map/skill.cpp`). Otherwise they fail with "wrong weapon".
- Prerequisites: 7009 → 7010 (Lv 3) → 7011, and 7009 → 7012 (Lv 3) → 7013.
  7014 needs 7011 at Lv 5 and 7013 at Lv 3. 7015 needs 7010 at Lv 5.

| ID | Skill | Story | Effect (levels 1–5) | SP / cooldown |
| --- | --- | --- | --- | --- |
| 7009 | Mortal Flame | "powered by mortal will rather than divine essence" | Passive, 1 level. While wielding Tenseiga: ATK +10%, 15% less damage from Holy and Shadow (in Tenseiga's item script). | — |
| 7010 | Severing Heaven's Lies | "its edge cut through illusions and divine lies" | One target, 2000/3000/4000/5000/6000% × base level / 100; 30/40/50/60/70% chance to strip its buffs. | 70 / 1 s |
| 7011 | Light and Shadow | "cut through both light and shadow" | Two hits of 1900/2800/3700/4600/5500% each × base level / 100, as Holy or Shadow, whichever element the target takes more damage from. | 80 / 1.5 s |
| 7012 | Unchained Will | "Balance is not obedience. Balance is freedom." | Cures Stun, Freeze, Stone, Sleep, Silence, Curse, Blind and Confusion, then blocks them for 40/50/60/70/80 s. | 60 / 60 s |
| 7013 | Forge of Ten Souls | every companion's will lit the First Forge | Party members within 7 cells: ATK and MATK +5/10/15/20/25%, and 1/2/3/4/5% more per party member there (at most 10), for 90 s. | 100 / 120 s |
| 7014 | Destiny's Severance | "severed the bond between divinity and mortal destiny" | One target, 8000/12000/16000/20000/24000% × base level / 100, ignoring DEF; +50% against boss monsters. 1 s cast. | 150 / 20 s |
| 7015 | Crescent Gale | Hayate's will loosed from the blade as a crescent of mortal flame | Every enemy on an 11-cell path toward the target (range 9), 3 cells wide, 5500/8000/10500/13000/15500% × base level / 100. Ranged. 0.5 s cast. | 120 / 6 s |

Client buff IDs **2005** and **2006** are Unchained Will and Forge of Ten
Souls. Like the other Samurai buffs, they are not saved through logout.

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
