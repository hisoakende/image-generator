import config

SET_EVENT = f"""
    DECLARE $uuid AS STRING;
    DECLARE $name AS STRING;
    DECLARE $created_at AS STRING;

    $datetime_parse = DateTime::Parse("%Y-%m-%dT%H:%M:%SZ");

    INSERT INTO {config.YDB_EVENT_TABLE} (uuid, name, created_at) 
    VALUES ($uuid, $name, DateTime::MakeDatetime($datetime_parse($created_at)));
"""

SET_URL = f"""
    DECLARE $uuid AS STRING;
    DECLARE $url AS STRING;
    DECLARE $created_at AS STRING;
    
    $datetime_parse = DateTime::Parse("%Y-%m-%dT%H:%M:%SZ");
    
    INSERT INTO {config.YDB_URL_TABLE} (uuid, url, created_at) 
    VALUES ($uuid, $url, DateTime::MakeDatetime($datetime_parse($created_at)));
"""

GET_CURRENT_EVENT_UUID = f"""
    SELECT uuid, created_at
    FROM {config.YDB_EVENT_TABLE}
    ORDER BY created_at DESC 
    LIMIT 1
"""
