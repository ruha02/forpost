copy dump.sql apps\pgsql\data\dump.sql
docker exec -it forpost_pgsql bash -c "psql -U admin -d database -f /data/dump.sql"