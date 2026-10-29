// Copyright (c) rAthena Dev Teams - Licensed under GNU GPL
// For more information, see LICENCE in the main folder

#include "skill_factory_custom.hpp"

#include "../skill_impl.hpp"
#include "map/clif.hpp"
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
        default:
            return nullptr;
    }
}
