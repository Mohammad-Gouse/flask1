drop table if exists users;
-- Create table: users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by INTEGER NOT NULL DEFAULT 1,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_by INTEGER NOT NULL DEFAULT 1
);

drop table if exists rbac_roles;
-- Create table: rbac_roles
CREATE TABLE rbac_roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by INTEGER NOT NULL DEFAULT 1,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_by INTEGER NOT NULL DEFAULT 1
);


drop table if exists user_role_mapping;
-- Create table: user_role_mapping
CREATE TABLE user_role_mapping (
    user_role_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    role_id INTEGER NOT NULL REFERENCES rbac_roles (role_id),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by INTEGER NOT NULL DEFAULT 1,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_by INTEGER NOT NULL DEFAULT 1
);



-- Insert sample data into table: users
INSERT INTO users (username, password)
VALUES
    ('texple@texple.com', 'pbkdf2:sha256:260000$N71zQewqP9cTzpq4$70d1accaa6d8b32146ecdba973742dbeab92dffda40a4722c23e99890c3d71c0'),
    ('gouse', 'pbkdf2:sha256:600000$441hD7cpYt3ATw50$ba5e57c3908e03026a2b779eb6e12d9e2a63528aa0d4d88402052d4276c025f5'),
    ('zaid', 'pbkdf2:sha256:600000$hg38c1QEv4ukANZd$c08d09d3b0afed6f74ff8e6e9f1b22605130cdc8c503dd6f20eec01c7ee2803d');

-- Insert sample data into table: rbac_roles
INSERT INTO rbac_roles (role_name)
VALUES
    ('admin'),
    ('POA'),
    ('Nominee'),
    ('PMS');

-- Insert sample data into table: user_role_mapping
INSERT INTO user_role_mapping (user_id, role_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3);