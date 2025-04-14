CREATE TABLE day (
    day BIGINT NOT NULL
);

CREATE TABLE clients (
    client_id UUID NOT NULL PRIMARY KEY UNIQUE,
    login VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    loc VARCHAR(511) NOT NULL,
    gender VARCHAR(6) NOT NULL
);

CREATE TABLE advertisers (
    advertiser_id UUID NOT NULL PRIMARY KEY UNIQUE,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE scores (
    client_id UUID NOT NULL,
    advertiser_id UUID NOT NULL,
    score INTEGER NOT NULL,
    CONSTRAINT score_unique UNIQUE (advertiser_id, client_id),
    CONSTRAINT fk_scores_client FOREIGN KEY (client_id) REFERENCES clients (client_id) ON DELETE CASCADE,
    CONSTRAINT fk_scores_advertiser FOREIGN KEY (advertiser_id) REFERENCES advertisers (advertiser_id) ON DELETE CASCADE
);

CREATE TABLE campaigns (
    campaign_id UUID NOT NULL PRIMARY KEY,
    advertiser_id UUID NOT NULL,
    ad_title VARCHAR(255) NOT NULL,
    ad_text TEXT NOT NULL,
    impressions_limit INTEGER NOT NULL,
    clicks_limit INTEGER NOT NULL,
    cost_per_impression FLOAT NOT NULL,
    cost_per_click FLOAT NOT NULL,
    start_date INTEGER NOT NULL,
    end_date INTEGER NOT NULL,
    age_from INTEGER,
    age_to INTEGER,
    gender VARCHAR(6),
    loc VARCHAR(511),
    image_url VARCHAR(255),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_campaigns_advertiser FOREIGN KEY (advertiser_id) REFERENCES advertisers (advertiser_id) ON DELETE CASCADE
);

CREATE TABLE impressions (
    serial_id SERIAL PRIMARY KEY,
    client_id UUID NOT NULL,
    campaign_id UUID NOT NULL,
    day BIGINT NOT NULL,
    price FLOAT NOT NULL,
    UNIQUE (client_id, campaign_id),
    CONSTRAINT fk_impressions_campaign FOREIGN KEY (campaign_id) REFERENCES campaigns (campaign_id) ON DELETE CASCADE,
    CONSTRAINT fk_impressions_client FOREIGN KEY (client_id) REFERENCES clients (client_id) ON DELETE CASCADE
);

CREATE TABLE clicks (
    serial_id SERIAL PRIMARY KEY,
    client_id UUID NOT NULL,
    campaign_id UUID NOT NULL,
    day BIGINT NOT NULL,
    price FLOAT NOT NULL,
    UNIQUE (client_id, campaign_id),
    CONSTRAINT fk_clicks_campaign FOREIGN KEY (campaign_id) REFERENCES campaigns (campaign_id) ON DELETE CASCADE,
    CONSTRAINT fk_clicks_client FOREIGN KEY (client_id) REFERENCES clients (client_id) ON DELETE CASCADE
);

CREATE VIEW active_campaigns AS
SELECT *
FROM campaigns
WHERE is_deleted = FALSE;