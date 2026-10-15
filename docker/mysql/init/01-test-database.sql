-- Database for the backend test suite (pytest drops and recreates it on every run).
CREATE DATABASE IF NOT EXISTS shop_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON shop_test.* TO 'shop'@'%';
