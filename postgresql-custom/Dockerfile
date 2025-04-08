# Use the official PostgreSQL 15 image as the base
FROM pgvector/pgvector:pg16

COPY schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
