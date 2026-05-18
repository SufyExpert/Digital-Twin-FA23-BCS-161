FROM postgres:15-alpine

# Set default PostgreSQL environment variables
ENV POSTGRES_DB=digital_twin_db
ENV POSTGRES_USER=sufy_dev
ENV POSTGRES_PASSWORD=devops_pass

# Copy the seeded SQL file into the auto-init directory of PostgreSQL
COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
