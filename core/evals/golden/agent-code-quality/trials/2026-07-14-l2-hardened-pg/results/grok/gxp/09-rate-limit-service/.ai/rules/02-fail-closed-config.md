# Rule: fail closed on bad config

If a config path is provided but the file is missing or invalid, the limiter
must **deny** traffic (`max_requests=0`), not open the floodgates.
