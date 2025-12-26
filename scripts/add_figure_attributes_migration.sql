-- Add new columns to mythological_figures table
-- Phase 2: Core attributes for rich figure data

ALTER TABLE mythological_figures 
ADD COLUMN IF NOT EXISTS role VARCHAR(200),
ADD COLUMN IF NOT EXISTS description TEXT,
ADD COLUMN IF NOT EXISTS symbols VARCHAR(500);

-- Add indexes for commonly queried fields
CREATE INDEX IF NOT EXISTS idx_figure_role ON mythological_figures(role);

-- Verify columns were added
SELECT column_name, data_type, character_maximum_length 
FROM information_schema.columns 
WHERE table_name = 'mythological_figures' 
AND column_name IN ('role', 'description', 'symbols');
