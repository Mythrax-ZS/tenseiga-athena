// Copyright (c) rAthena Dev Teams - Licensed under GNU GPL
// For more information, see LICENCE in the main folder

#include "skill_factory_custom.hpp"

#include "../skill_impl.hpp"
#include "common/utils.hpp"
#include "map/clif.hpp"
#include "map/mob.hpp"
#include "map/party.hpp"
#include "map/pc.hpp"
#include "map/status.hpp"

namespace {
class SamuraiStrike final : public WeaponSkillImpl {
public:
    explicit SamuraiStrike(e_skill id) : WeaponSkillImpl(id) {}
    void calculateSkillRatio(const Damage*, const block_list*, const block_list*, uint16 lv, int32& ratio, int32) const override {
        // Severance: 400-800%; Wrath: 800-1600% of weapon damage.
        ratio += getSkillId() == SAM_WRATH_UNBOUND ? 500 + 200 * lv : 200 + 100 * lv;
    }
};

class SamuraiAshenWind final : public SkillImplRecursiveDamageSplash {
public:
    SamuraiAshenWind() : SkillImplRecursiveDamageSplash(SAM_ASHEN_WIND_SLASH) {}
    void castendNoDamageId(block_list* src, block_list* target, uint16 lv, t_tick tick, int32& flag) const override {
        clif_skill_nodamage(src, *target, getSkillId(), lv);
        skill_castend_damage_id(src, target, getSkillId(), lv, tick, flag);
    }
    void calculateSkillRatio(const Damage*, const block_list*, const block_list*, uint16 lv, int32& ratio, int32) const override {
        ratio += 100 + 100 * lv; // 300-700%.
    }
    void applyAdditionalEffects(block_list* src, block_list* target, uint16 lv, t_tick, int32, damage_lv) const override {
        sc_start2(src, target, SC_BLEEDING, 10 + 5 * lv, lv, src->id, skill_get_time2(getSkillId(), lv));
    }
};

// The Mortal Flame line (Tenseiga's techniques; skill.cpp checks that Tenseiga is wielded).

// Severing Heaven's Lies: "its edge cut through illusions and divine lies".
class SamuraiSeverLies final : public WeaponSkillImpl {
public:
    SamuraiSeverLies() : WeaponSkillImpl(SAM_SEVER_HEAVENS_LIES) {}
    void calculateSkillRatio(const Damage*, const block_list*, const block_list*, uint16 lv, int32& ratio, int32) const override {
        ratio += 400 + 100 * lv; // 500-900%.
    }
    void applyAdditionalEffects(block_list*, block_list* target, uint16 lv, t_tick, int32, damage_lv) const override {
        if (rnd() % 100 < 20 + 10 * lv) // 30-70%: strip the target's buffs.
            status_change_clear_buffs(target, SCCB_BUFFS);
    }
};

// Light and Shadow: two cuts as Holy or Shadow, whichever the target takes more from.
class SamuraiLightAndShadow final : public WeaponSkillImpl {
public:
    SamuraiLightAndShadow() : WeaponSkillImpl(SAM_LIGHT_AND_SHADOW) {}
    void calculateSkillRatio(const Damage*, const block_list*, const block_list*, uint16 lv, int32& ratio, int32) const override {
        ratio += 150 + 50 * lv; // 300-500% per hit, two hits.
    }
    void modifyElement(const Damage&, const block_list&, const block_list& target, uint16, int32& element, int32) const override {
        const status_data* tstatus = status_get_status_data(target);
        int16 holy = elemental_attribute_db.getAttribute(tstatus->ele_lv, ELE_HOLY, tstatus->def_ele);
        int16 shadow = elemental_attribute_db.getAttribute(tstatus->ele_lv, ELE_DARK, tstatus->def_ele);
        element = shadow > holy ? ELE_DARK : ELE_HOLY;
    }
};

// Unchained Will: "balance is not obedience, balance is freedom". Cures the statuses it
// then wards off (status.cpp, status_get_sc_def).
class SamuraiUnchainedWill final : public SkillImpl {
public:
    SamuraiUnchainedWill() : SkillImpl(SAM_UNCHAINED_WILL) {}
    void castendNoDamageId(block_list* src, block_list* target, uint16 lv, t_tick, int32&) const override {
        for (sc_type sc : { SC_STUN, SC_FREEZE, SC_STONE, SC_STONEWAIT, SC_SLEEP, SC_SILENCE, SC_CURSE, SC_BLIND, SC_CONFUSION })
            status_change_end(target, sc);
        clif_skill_nodamage(src, *target, getSkillId(), lv, sc_start(src, target, SC_SAM_UNCHAINED_WILL, 100, lv, skill_get_time(getSkillId(), lv)));
    }
};

// Forge of Ten Souls: the companions' will that lit the First Forge. Every party member in
// range gains ATK and MATK for each of them there (counting at most ten).
class SamuraiForgeOfTenSouls final : public SkillImpl {
    // Souls counted when the caster casts, for the members it then reaches.
    inline static int32 souls = 1;
public:
    SamuraiForgeOfTenSouls() : SkillImpl(SAM_FORGE_OF_TEN_SOULS) {}
    void castendNoDamageId(block_list* src, block_list* target, uint16 lv, t_tick tick, int32& flag) const override {
        map_session_data* sd = BL_CAST(BL_PC, src);

        if (sd == nullptr || sd->status.party_id == 0 || (flag & 1)) {
            if (!(flag & 1))
                souls = 1; // Alone: only the caster's own.
            if (check_distance_bl(src, target, AREA_SIZE))
                clif_skill_nodamage(target, *target, getSkillId(), lv);
            sc_start2(src, target, SC_SAM_FORGE_OF_TEN_SOULS, 100, lv, lv * souls, skill_get_time(getSkillId(), lv));
            return;
        }
        int32 range = skill_get_splash(getSkillId(), lv);
        souls = cap_value(party_foreachsamemap(party_sub_count, sd, range), 1, 10);
        party_foreachsamemap(skill_area_sub, sd, range, src, getSkillId(), lv, tick, flag | BCT_PARTY | 1, skill_castend_nodamage_id);
    }
};

// Destiny's Severance: the strike that "severed the bond between divinity and mortal
// destiny". Ignores DEF (skill_db); half again against bosses.
class SamuraiDestinysSeverance final : public WeaponSkillImpl {
public:
    SamuraiDestinysSeverance() : WeaponSkillImpl(SAM_DESTINYS_SEVERANCE) {}
    void calculateSkillRatio(const Damage*, const block_list*, const block_list* target, uint16 lv, int32& ratio, int32) const override {
        ratio += 650 + 250 * lv; // 1000-2000%.
        if (target != nullptr && status_get_class_(target) == CLASS_BOSS)
            ratio = ratio * 3 / 2;
    }
};
} // namespace

std::unique_ptr<const SkillImpl> SkillFactoryCustom::create(const e_skill skill_id) const {
    switch (skill_id) {
        case SAM_HEAVENS_SEVERANCE:
        case SAM_WRATH_UNBOUND:
            return std::make_unique<SamuraiStrike>(skill_id);
        case SAM_ASHEN_WIND_SLASH:
            return std::make_unique<SamuraiAshenWind>();
        case SAM_KUSANAGI_GUARD:
        case SAM_MOONLIT_REFLECTION:
        case SAM_BLADE_HARMONY:
        case SAM_BLOOD_COVENANT:
        case SAM_MURAMASAS_CURSE:
            return std::make_unique<StatusSkillImpl>(skill_id);
        case SAM_SEVER_HEAVENS_LIES:
            return std::make_unique<SamuraiSeverLies>();
        case SAM_LIGHT_AND_SHADOW:
            return std::make_unique<SamuraiLightAndShadow>();
        case SAM_UNCHAINED_WILL:
            return std::make_unique<SamuraiUnchainedWill>();
        case SAM_FORGE_OF_TEN_SOULS:
            return std::make_unique<SamuraiForgeOfTenSouls>();
        case SAM_DESTINYS_SEVERANCE:
            return std::make_unique<SamuraiDestinysSeverance>();
        default:
            return nullptr;
    }
}
