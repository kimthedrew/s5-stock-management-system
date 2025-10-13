-- Fix password column length in PostgreSQL
-- This script expands the password column from 120 to 255 characters

ALTER TABLE "user" ALTER COLUMN password TYPE VARCHAR(255);
