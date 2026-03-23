ALTER TABLE items ADD COLUMN status TEXT NOT NULL DEFAULT 'discovered';
ALTER TABLE items ADD COLUMN published_at TEXT;
