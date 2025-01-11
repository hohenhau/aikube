-- Create the items table
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,                        -- Auto-incrementing primary key
    text TEXT NOT NULL,                           -- Text for sentiment analysis
    sentiment FLOAT CHECK (sentiment >= -1 AND sentiment <= 1),  -- Sentiment score (-1 to 1)
    processed BOOLEAN DEFAULT FALSE,              -- Whether the text has been processed
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the row is added
    CONSTRAINT check_sentiment_range CHECK (sentiment >= -1 AND sentiment <= 1)  -- Validation constraint
);

-- Add a sample entry for testing
INSERT INTO items (text, sentiment, processed)
VALUES ('This is a sample text.', NULL, FALSE);
