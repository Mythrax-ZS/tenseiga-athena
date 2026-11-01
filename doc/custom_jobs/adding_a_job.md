# Adding a custom job

Job ids **4500-4599** are reserved for custom jobs (`JOB_CUSTOM_START`..`JOB_CUSTOM_END`
in `src/common/mmo.hpp`). The Samurai is 4500. The Tenseiga client treats the whole range
as player jobs.

## Server

1. Add a row to `custom_jobs` in `src/custom/jobs.hpp`:

   ```cpp
   { static_cast<e_job>( 4501 ), "RONIN", "Ronin", JOB_SWORDMAN },
   ```

   The fields are the id, the constant name, the display name and the ancestor job.
   - **Constant name.** Scripts and db files get `JOB_RONIN` and `EAJ_RONIN` from it.
     Item, job and skill-tree entries use `Ronin` (case does not matter).
   - **Ancestor.** The new job passes that job's class checks and can wear its equipment.
   - **Rules.** Append rows; don't reorder them. A row's position is part of its job's map
     id and item bit. There can be at most 32 rows.
2. Rebuild the char and map servers together, since both read the table.
3. Add the db files, as for any job. `db/custom/samurai/` is a worked example. Import each
   file from the matching main db file.
   - `job_stats.yml`: levels, HP/SP, ASPD.
   - `skill_tree.yml`.
   - `item_db.yml`: an item with `Jobs: Ronin: true` can be worn only by that job.
4. Add a job-change NPC (see `npc/custom/samurai_jobchange.txt`).

Anything a job needs beyond this is code, as it was for the Samurai:
- weapon rules in `pc_job_can_use_item`;
- its own skills (`skill.hpp`, `skills/custom/skill_factory_custom.cpp`).

## Client (Tenseiga)

The client reads `System\customjobs.lua` from the game data or an overlay:

```lua
CustomJobs = {
	[4501] = { sprite = "ronin", name = "Ronin" },
}
```

The sprite name is used the same way the stock jobs use theirs:

| What | Path |
| --- | --- |
| Body | `data\sprite\인간족\몸통\{남,여}\ronin_{남,여}.spr/.act` |
| Weapons | `data\sprite\인간족\ronin\ronin_{남,여}{weapon}.spr/.act` |
| Body palettes | `data\palette\몸\ronin_{남,여}_{n}.pal` |

The Samurai is built into the client and is not listed there.

## Palettes

Clothes colour `n` loads `data\palette\몸\{job sprite}_{sex}_{n}.pal`, or
`data\palette\도람족\body\...` for Doram jobs.

- **Numbering.** Palettes are per job, as named, and any number works. A number a job
  has no file for shows the sprite's own colours.
- **Server limit.** The server caps the number at `max_cloth_color` in
  `conf/battle/client.conf` (now 7). Raise it in `conf/import/battle_conf.txt` to the highest
  palette a pack ships.
- **Stylist.** The stylist offers only the colours listed in `db/re/stylist.yml`. `@dye` and
  `setlook LOOK_CLOTHES_COLOR` reach any number up to the limit.
- **Indexed sprites only.** Palettes recolour palette-indexed sprites. A truecolor body
  can't be dyed, which includes the Samurai's current art.
