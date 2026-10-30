# The Twin Flames Saga

The Samurai's quest line, adapted from the user's *Twin Flames Saga* (see
[samurai.md](samurai.md) for the job, its blades and skills). It follows Hayate Yoshida's story
in ten chapters: the player, a Samurai, takes Hayate's road from a burned house to the First
Forge. Along the way they receive **Muramasa** (Chapter I) and **Kusanagi** (Chapter V), then
forge **Tenseiga-no-Hayate** and learn **Mortal Flame** (Chapter X). Only Samurai can take it.

Masaru no longer forges Tenseiga on request in Prontera; the forging is Chapter X. Samurai who
forged Tenseiga before the saga existed keep it, and Masaru still grants them Mortal Flame.

## Files

| What | Where |
| --- | --- |
| NPCs and chapters | `npc/custom/twin_flames/` (`tf_common.txt`, `tf_ch01_03.txt`, `tf_tetsuya.txt`, `tf_ch04_06.txt`, `tf_ch07_10.txt`), and Masaru in `npc/custom/samurai_tenseiga.txt` |
| Quests | `db/custom/samurai/quest_db.yml` (900101-900192), imported by `db/quest_db.yml` |
| Monsters | `db/custom/samurai/mob_db.yml` (31900-31917), imported by `db/mob_db.yml` |
| Monster skills | `db/custom/samurai/mob_skill_db.txt`, read after db/import (`src/map/mob.cpp`, `mob_load`) |
| Relics and quest items | `db/custom/samurai/item_db.yml` (900010-900021) |
| Client: monster looks | roclient `crates/ro-client/src/saga.rs` |
| Client: quest log, item names | roclient `overlays/samurai/System/samurai_questinfo.lua`, `samurai_iteminfo.lua` |

## The chapters

`TF_STEP` (a character variable) records progress. `TF_BOND` holds a bit for each finished
side trial: 1 Kiyoshi, 2 Renga, 4 Ayame, 8 Taro and Jiro, 16 Hanae, 32 the Herald, 64 Masaru.
`TF_MERCY` and `TF_TRUST` remember choices and change Tetsuya's last words.

| Chapter | Steps | Where | What happens |
| --- | --- | --- | --- |
| I Ashes of Honor | 0-10 | Ashigaru Courier, Prontera 158,179; Oharu, Amatsu 192,94; the Hooded Kami in the field shrine (ama_in01 175,176) | The house you served is burned. A "kami of justice" (Yami in disguise) answers your prayer with **Muramasa**. Hunt 20 Ashigaru Raiders. |
| II The Wandering Ronin | 10-20 | Elder Genzo, Amatsu 185,160; the Captured Raider, 187,158 | Drive back 30 Kapha. Spare or cut down a captured raider. |
| III The Trickster's Tail | 20-30 | Tetsuya, Amatsu 192,163; War Banner, ama_dun02 45,50 | Tetsuya's riddle (the answer: a soul). Defeat **Warlord Kurogane** (Muramasa in hand). |
| IV Whispers in Steel | 30-51 | Battle Standard, ama_fild01 200,291; Kiyoshi 210,150, Renga 200,140, Ayame 215,140 in Amatsu | 40 Crimson Fields Soldiers and the **Shade of Yami**; Yami reveals himself. Three trials: **General Mibu** (ice_dun02 150,155), **Fallen Monk Genkai** (prt_monk 225,140), **Kage** (ama_dun02 40,50; then 5 Holy Water). Each companion gives a relic. |
| V The Shrine of Seals | 51-60 | Sealed Gate, ama_dun03 120,30; Chiyo, 110,30 | The **Guardian of the Seal** (Muramasa in hand); curse and Sarugami blood free **Kusanagi**. Chiyo's master, **High Priestess Sayo**. |
| VI Chains of Light | 60-71 | Tetsuya; Taro and Jiro, Amatsu 225/227,150; Lady Hanae, ama_in02 196,172 | Trust the goddess or Tetsuya. The **Glacial Yokai** (ice_dun03 149,45). Three Sealed Letters (from Shinobi and Miyabi Dolls), then **Daimyo Kurozane** (ama_in02 204,168). |
| VII Return of the Ashes | 71-81 | Altar of Ashes, thor_v02 90,199; Masaru, Prontera 161,179 | 30 Cultists of Ashes and the **Herald of Ashes** (Twin Flames: both blades dual wielded). Five ledger pages (from Kasa and Salamanders) for Masaru. |
| VIII The Fall of Yami | 81-90 | Kohaku, pay_fild08 40,80; Abyssal Gate, thor_v03 49,250 | The **Contract Binder** frees Kohaku the fox. **Kagutsuchi-no-Yami** falls (Twin Flames); the goddess's false blessing. |
| IX The Weaver Unmasked | 90-100 | Tetsuya | Bring all eight relics; Tetsuya adds the Sarugami Essence. |
| X The Mortal Flame | 100-120 | Masaru and Tetsuya at the First Forge, mag_dun02 49,40 / 53,44; the Weaver's Throne, valkyrie 48,64 | Forge **Tenseiga-no-Hayate** (Twin Flames, 9 relics, 10 Oridecon, 10 Burning Hearts) and learn **Mortal Flame**. In the Celestial Veil, the Weaver in three forms: Radiant, Eclipsed, then **Amaterasu-no-Mikazuki** (Tenseiga in hand). |

The forge keeps the lower refine of the two blades and refuses blades with cards in them.

## Bosses

Each boss is called by the quest's own player at an arena NPC, on that quest step and with
the blade it needs, and leaves after 15 minutes if it still stands (`TF_Arenas` in
`tf_common.txt`). Quest kill credit goes to the killer and to party members on the map. The
Weaver's forms follow one another as each falls.

| Id | Monster | Lv | HP | Notes |
| --- | --- | --- | --- | --- |
| 31900 | Ashigaru Raider | 110 | 45k | Amatsu fields (25) |
| 31901 | Crimson Fields Soldier | 125 | 90k | Amatsu fields, north (30) |
| 31902 | Cultist of Ashes | 140 | 160k | Thor's volcano, first level (20) |
| 31903 | Warlord Kurogane | 145 | 3M | |
| 31904 | Shade of Yami | 150 | 4M | |
| 31905 | Usurper General Mibu | 150 | 5M | |
| 31906 | Fallen Monk Genkai | 150 | 5M | |
| 31907 | Kage, Assassin of Ashes | 155 | 5.5M | |
| 31908 | Guardian of the Seal | 160 | 9M | |
| 31909 | High Priestess Sayo | 160 | 9M | |
| 31910 | Glacial Yokai | 165 | 12M | |
| 31911 | Daimyo Kurozane | 165 | 12M | |
| 31912 | Herald of Ashes | 175 | 20M | |
| 31913 | Contract Binder | 170 | 15M | |
| 31914 | Kagutsuchi-no-Yami | 185 | 50M | MVP |
| 31915 | Radiant Amaterasu | 195 | 35M | Holy |
| 31916 | Eclipsed Amaterasu | 195 | 35M | Dark |
| 31917 | Amaterasu-no-Mikazuki | 200 | 60M | MVP, Neutral |

They are tuned against the Samurai's 4th-job-strength skills. The ids are this server's own,
so the official client has no sprite for them; roclient draws each from a stock monster
sprite, recoloured, resized and tinted, with code-drawn auras for Yami (embers over a black
pool) and the Weaver (sun gold and moon silver).

## Testing

`@set TF_STEP <n>` with `@setquest` / `@completequest` jumps to a chapter; `@item 900010`..`900018`
gives the relics. Chapter I, the First Forge and the Celestial Veil were played through in
roclient on 2026-10-30, including the Weaver's three forms and quest credit for the last.
