-- Add job dependencies table to support workflow-style job orchestration
-- where jobs can depend on the successful completion of other jobs

CREATE TABLE procrastinate_job_dependencies (
    job_id bigint NOT NULL REFERENCES procrastinate_jobs(id) ON DELETE CASCADE,
    depends_on_job_id bigint NOT NULL REFERENCES procrastinate_jobs(id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, depends_on_job_id),
    -- Prevent circular dependencies
    CONSTRAINT no_self_dependency CHECK (job_id != depends_on_job_id)
);

-- Index to efficiently find which jobs depend on a given job (useful for cleanup)
CREATE INDEX procrastinate_job_dependencies_depends_on_idx
    ON procrastinate_job_dependencies(depends_on_job_id);

-- Index to efficiently check if a job has unmet dependencies
CREATE INDEX procrastinate_job_dependencies_job_id_idx
    ON procrastinate_job_dependencies(job_id);

-- Update procrastinate_fetch_job_v2 to respect job dependencies
CREATE OR REPLACE FUNCTION procrastinate_fetch_job_v3(
    target_queue_names character varying[],
    p_worker_id bigint
)
    RETURNS procrastinate_jobs
    LANGUAGE plpgsql
AS $$
DECLARE
    found_jobs procrastinate_jobs;
BEGIN
    WITH candidate AS (
        SELECT jobs.*
            FROM procrastinate_jobs AS jobs
            WHERE
                -- reject the job if its lock has earlier or higher priority jobs
                NOT EXISTS (
                    SELECT 1
                        FROM procrastinate_jobs AS other_jobs
                        WHERE
                            jobs.lock IS NOT NULL
                            AND other_jobs.lock = jobs.lock
                            AND (
                                -- job with same lock is already running
                                other_jobs.status = 'doing'
                                OR
                                -- job with same lock is waiting and has higher priority (or same priority but was queued first)
                                (
                                    other_jobs.status = 'todo'
                                    AND (
                                        other_jobs.priority > jobs.priority
                                        OR (
                                        other_jobs.priority = jobs.priority
                                        AND other_jobs.id < jobs.id
                                        )
                                    )
                                )
                            )
                )
                -- reject the job if it has dependencies that haven't finished
                -- (finished means any terminal status: succeeded, failed, cancelled, aborted)
                AND NOT EXISTS (
                    SELECT 1
                        FROM procrastinate_job_dependencies AS deps
                        INNER JOIN procrastinate_jobs AS parent_jobs
                            ON deps.depends_on_job_id = parent_jobs.id
                        WHERE
                            deps.job_id = jobs.id
                            AND parent_jobs.status NOT IN ('succeeded', 'failed', 'cancelled', 'aborted')
                )
                AND jobs.status = 'todo'
                AND (target_queue_names IS NULL OR jobs.queue_name = ANY( target_queue_names ))
                AND (jobs.scheduled_at IS NULL OR jobs.scheduled_at <= now())
            ORDER BY jobs.priority DESC, jobs.id ASC LIMIT 1
            FOR UPDATE OF jobs SKIP LOCKED
    )
    UPDATE procrastinate_jobs
        SET status = 'doing', worker_id = p_worker_id
        FROM candidate
        WHERE procrastinate_jobs.id = candidate.id
        RETURNING procrastinate_jobs.* INTO found_jobs;

 RETURN found_jobs;
END;
$$;
