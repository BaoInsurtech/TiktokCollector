CREATE TABLE TiktokShopTokens (
    customer_id VARCHAR(100) PRIMARY KEY,
    access_token TEXT NOT NULL,
    access_token_expire_in BIGINT NOT NULL,
    refresh_token TEXT NOT NULL,
    refresh_token_expire_in BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);