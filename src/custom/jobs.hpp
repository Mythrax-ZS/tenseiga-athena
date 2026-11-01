// Copyright (c) rAthena Dev Teams - Licensed under GNU GPL
// For more information, see LICENCE in the main folder

#ifndef CONFIG_CUSTOM_JOBS_HPP
#define CONFIG_CUSTOM_JOBS_HPP

#include <iterator>

#include <common/mmo.hpp>

/// A custom job: its id (JOB_CUSTOM_START..JOB_CUSTOM_END), the name scripts and the db files
/// use (JOB_<constant>, EAJ_<constant>), its display name, and the job it descends from: it
/// inherits that job's skills checks and equipment (map.hpp, JOBL_CUSTOM).
struct s_custom_job {
	e_job id;
	const char* constant;
	const char* name;
	e_job ancestor;
};

/// The custom jobs. A new one is a row here, then its db files like any job (job_stats,
/// skill_tree...; doc/custom_jobs/adding_a_job.md). Rows keep their place: a row's position is
/// part of its job's map id and item bit.
static constexpr s_custom_job custom_jobs[] = {
	{ JOB_SAMURAI, "SAMURAI", "Samurai", JOB_ASSASSIN_CROSS },
};

static constexpr bool custom_jobs_in_range(){
	for( const s_custom_job& job : custom_jobs ){
		if( job.id < JOB_CUSTOM_START || job.id > JOB_CUSTOM_END ){
			return false;
		}
	}
	return true;
}

static_assert( custom_jobs_in_range(), "custom job ids are JOB_CUSTOM_START..JOB_CUSTOM_END" );
// One item bit each, in the top half of class_base (map.hpp, ITEMJOB_CUSTOM).
static_assert( std::size( custom_jobs ) <= 32, "at most 32 custom jobs" );

/// The custom job with this id, if any.
static inline const s_custom_job* custom_job( int32 id ){
	for( const s_custom_job& job : custom_jobs ){
		if( job.id == id ){
			return &job;
		}
	}
	return nullptr;
}

#endif /* CONFIG_CUSTOM_JOBS_HPP */
