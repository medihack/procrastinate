-- Add canvas coordination table for chords

CREATE TABLE procrastinate_canvas_chords (
    chord_id character varying(128) PRIMARY KEY,
    header_size integer NOT NULL,
    completed_count integer DEFAULT 0 NOT NULL,
    results jsonb DEFAULT '[]' NOT NULL,
    callback_task_name character varying(128) NOT NULL,
    callback_kwargs jsonb DEFAULT '{}' NOT NULL,
    callback_options jsonb DEFAULT '{}' NOT NULL,
    created_at timestamp with time zone DEFAULT NOW() NOT NULL,
    CONSTRAINT check_completed_lte_size CHECK (completed_count <= header_size)
);

-- Index for efficient lookups
CREATE INDEX procrastinate_canvas_chords_created_at_idx ON procrastinate_canvas_chords(created_at);
