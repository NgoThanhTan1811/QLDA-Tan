-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 24, 2025 at 02:59 AM
-- Server version: 11.8.2-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;

--
-- Database: `fruit_manage`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user`
--

CREATE TABLE `accounts_user` (
    `id` bigint(20) NOT NULL,
    `password` varchar(128) NOT NULL,
    `is_superuser` tinyint(1) NOT NULL,
    `username` varchar(150) NOT NULL,
    `first_name` varchar(150) NOT NULL,
    `last_name` varchar(150) NOT NULL,
    `email` varchar(254) NOT NULL,
    `is_staff` tinyint(1) NOT NULL,
    `is_active` tinyint(1) NOT NULL,
    `date_joined` datetime(6) NOT NULL,
    `phone` varchar(15) DEFAULT NULL,
    `address` longtext DEFAULT NULL,
    `role` varchar(20) NOT NULL,
    `avatar` varchar(100) DEFAULT NULL,
    `is_active_employee` tinyint(1) NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_userprofile`
--

CREATE TABLE `accounts_userprofile` (
    `id` bigint(20) NOT NULL,
    `employee_id` varchar(10) NOT NULL,
    `department` varchar(100) NOT NULL,
    `position` varchar(100) NOT NULL,
    `hire_date` date DEFAULT NULL,
    `salary` decimal(12, 2) DEFAULT NULL,
    `user_id` bigint(20) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs_activitylog`
--

CREATE TABLE `activity_logs_activitylog` (
    `id` bigint(20) NOT NULL,
    `action` varchar(20) NOT NULL,
    `description` longtext NOT NULL,
    `severity` varchar(20) NOT NULL,
    `object_id` int(10) UNSIGNED DEFAULT NULL CHECK (`object_id` >= 0),
    `ip_address` char(39) NOT NULL,
    `user_agent` longtext NOT NULL,
    `session_key` varchar(40) NOT NULL,
    `old_values` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`old_values`)),
    `new_values` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`new_values`)),
    `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`extra_data`)),
    `timestamp` datetime(6) NOT NULL,
    `content_type_id` int(11) DEFAULT NULL,
    `user_id` bigint(20) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customers_customer`
--

CREATE TABLE `customers_customer` (
    `id` bigint(20) NOT NULL,
    `customer_code` varchar(20) NOT NULL,
    `full_name` varchar(200) NOT NULL,
    `phone` varchar(17) NOT NULL,
    `email` varchar(254) NOT NULL,
    `province` varchar(100) NOT NULL,
    `district` varchar(100) NOT NULL,
    `ward` varchar(100) NOT NULL,
    `address` longtext NOT NULL,
    `is_active` tinyint(1) NOT NULL,
    `is_verified` tinyint(1) NOT NULL,
    `date_of_birth` date DEFAULT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `user_id` bigint(20) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `farmers_farmer`
--

CREATE TABLE `farmers_farmer` (
    `id` bigint(20) NOT NULL,
    `farmer_code` varchar(20) NOT NULL,
    `name` varchar(200) NOT NULL,
    `farmer_type` varchar(20) NOT NULL,
    `phone` varchar(17) NOT NULL,
    `email` varchar(254) NOT NULL,
    `province` varchar(100) NOT NULL,
    `district` varchar(100) NOT NULL,
    `ward` varchar(100) NOT NULL,
    `address` longtext NOT NULL,
    `farming_region` varchar(200) NOT NULL,
    `total_farm_area` decimal(10, 2) NOT NULL,
    `active_farm_area` decimal(10, 2) NOT NULL,
    `farming_experience` int(11) NOT NULL,
    `main_crops` longtext NOT NULL,
    `certifications` varchar(20) NOT NULL,
    `certification_number` varchar(100) NOT NULL,
    `certification_expiry` date DEFAULT NULL,
    `bank_name` varchar(100) NOT NULL,
    `bank_account` varchar(50) NOT NULL,
    `account_holder` varchar(100) NOT NULL,
    `tax_code` varchar(20) DEFAULT NULL,
    `rating` decimal(3, 2) NOT NULL,
    `total_reviews` int(11) NOT NULL,
    `is_verified` tinyint(1) NOT NULL,
    `is_active` tinyint(1) NOT NULL,
    `is_featured` tinyint(1) NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `inventory_inventorystock`
--

CREATE TABLE `inventory_inventorystock` (
    `id` bigint(20) NOT NULL,
    `quantity` decimal(10, 2) NOT NULL,
    `reserved_quantity` decimal(10, 2) NOT NULL,
    `min_stock_level` decimal(10, 2) NOT NULL,
    `max_stock_level` decimal(10, 2) NOT NULL,
    `last_updated` datetime(6) NOT NULL,
    `product_id` bigint(20) NOT NULL,
    `warehouse_id` bigint(20) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `inventory_warehouse`
--

CREATE TABLE `inventory_warehouse` (
    `id` bigint(20) NOT NULL,
    `name` varchar(100) NOT NULL,
    `code` varchar(20) NOT NULL,
    `address` longtext NOT NULL,
    `capacity` decimal(10, 2) NOT NULL,
    `is_active` tinyint(1) NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `manager_id` bigint(20) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders_order`
--

CREATE TABLE `orders_order` (
    `id` bigint(20) NOT NULL,
    `order_number` varchar(50) NOT NULL,
    `order_type` varchar(20) NOT NULL,
    `status` varchar(20) NOT NULL,
    `payment_status` varchar(20) NOT NULL,
    `priority` varchar(10) NOT NULL,
    `order_date` datetime(6) NOT NULL,
    `delivery_date` date DEFAULT NULL,
    `expected_delivery` date DEFAULT NULL,
    `shipping_address` longtext NOT NULL,
    `shipping_contact` varchar(100) NOT NULL,
    `shipping_phone` varchar(15) NOT NULL,
    `subtotal` decimal(15, 2) NOT NULL,
    `tax_amount` decimal(15, 2) NOT NULL,
    `shipping_cost` decimal(15, 2) NOT NULL,
    `discount_amount` decimal(15, 2) NOT NULL,
    `total_amount` decimal(15, 2) NOT NULL,
    `tracking_number` varchar(100) NOT NULL,
    `estimated_weight` decimal(10, 2) NOT NULL,
    `actual_weight` decimal(10, 2) NOT NULL,
    `notes` longtext NOT NULL,
    `internal_notes` longtext NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `created_by_id` bigint(20) DEFAULT NULL,
    `customer_id` bigint(20) DEFAULT NULL,
    `farmer_id` bigint(20) DEFAULT NULL,
    `updated_by_id` bigint(20) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders_orderdetail`
--

CREATE TABLE `orders_orderdetail` (
    `id` bigint(20) NOT NULL,
    `quantity` decimal(10, 2) NOT NULL,
    `unit_price` decimal(12, 2) NOT NULL,
    `total_price` decimal(15, 2) NOT NULL,
    `tax_rate` decimal(5, 2) NOT NULL,
    `discount_rate` decimal(5, 2) NOT NULL,
    `notes` longtext NOT NULL,
    `order_id` bigint(20) NOT NULL,
    `product_id` bigint(20) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payments_payment`
--

CREATE TABLE `payments_payment` (
    `id` bigint(20) NOT NULL,
    `payment_code` varchar(50) NOT NULL,
    `payment_type` varchar(20) NOT NULL,
    `amount` decimal(15, 2) NOT NULL,
    `payment_method` varchar(20) NOT NULL,
    `status` varchar(20) NOT NULL,
    `payment_date` date NOT NULL,
    `due_date` date DEFAULT NULL,
    `bank_name` varchar(100) NOT NULL,
    `bank_account` varchar(50) NOT NULL,
    `transaction_reference` varchar(100) NOT NULL,
    `notes` longtext NOT NULL,
    `exchange_rate` decimal(10, 4) NOT NULL,
    `currency` varchar(3) NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `approved_by_id` bigint(20) DEFAULT NULL,
    `created_by_id` bigint(20) DEFAULT NULL,
    `customer_id` bigint(20) DEFAULT NULL,
    `farmer_id` bigint(20) DEFAULT NULL,
    `order_id` bigint(20) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products_category`
--

CREATE TABLE `products_category` (
    `id` bigint(20) NOT NULL,
    `name` varchar(100) NOT NULL,
    `description` longtext NOT NULL,
    `image` varchar(100) DEFAULT NULL,
    `is_active` tinyint(1) NOT NULL,
    `created_at` datetime(6) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products_product`
--

CREATE TABLE `products_product` (
    `id` bigint(20) NOT NULL,
    `code` varchar(20) NOT NULL,
    `name` varchar(200) NOT NULL,
    `description` longtext NOT NULL,
    `origin` varchar(20) NOT NULL,
    `origin_country` varchar(100) NOT NULL,
    `quality_grade` varchar(5) NOT NULL,
    `cost_price` decimal(12, 2) NOT NULL,
    `selling_price` decimal(12, 2) NOT NULL,
    `export_price` decimal(12, 2) DEFAULT NULL,
    `shelf_life_days` int(10) UNSIGNED NOT NULL CHECK (`shelf_life_days` >= 0),
    `storage_temperature_min` double DEFAULT NULL,
    `storage_temperature_max` double DEFAULT NULL,
    `humidity_requirement` varchar(50) NOT NULL,
    `hs_code` varchar(20) NOT NULL,
    `tax_rate` decimal(5, 2) NOT NULL,
    `image` varchar(100) DEFAULT NULL,
    `is_active` tinyint(1) NOT NULL,
    `created_at` datetime(6) NOT NULL,
    `updated_at` datetime(6) NOT NULL,
    `category_id` bigint(20) NOT NULL,
    `unit_id` bigint(20) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts_user`
--
ALTER TABLE `accounts_user`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `accounts_userprofile`
--
ALTER TABLE `accounts_userprofile`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `employee_id` (`employee_id`),
ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `activity_logs_activitylog`
--
ALTER TABLE `activity_logs_activitylog`
ADD PRIMARY KEY (`id`),
ADD KEY `activity_lo_user_id_8d9f3d_idx` (`user_id`, `timestamp`),
ADD KEY `activity_lo_action_e13a65_idx` (`action`, `timestamp`),
ADD KEY `activity_lo_content_50462e_idx` (
    `content_type_id`,
    `object_id`
),
ADD KEY `activity_lo_ip_addr_56ce69_idx` (`ip_address`, `timestamp`);

--
-- Indexes for table `customers_customer`
--
ALTER TABLE `customers_customer`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `customer_code` (`customer_code`),
ADD UNIQUE KEY `tax_code` (`tax_code`),
ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `farmers_farmer`
--
ALTER TABLE `farmers_farmer`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `farmer_code` (`farmer_code`),
ADD UNIQUE KEY `tax_code` (`tax_code`);

--
-- Indexes for table `inventory_inventorystock`
--
ALTER TABLE `inventory_inventorystock`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `inventory_inventorystock_warehouse_id_product_id_8a652488_uniq` (`warehouse_id`, `product_id`),
ADD KEY `inventory_inventorys_product_id_7a8f1319_fk_products_` (`product_id`);

--
-- Indexes for table `inventory_warehouse`
--
ALTER TABLE `inventory_warehouse`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `name` (`name`),
ADD UNIQUE KEY `code` (`code`),
ADD KEY `inventory_warehouse_manager_id_6def176a_fk_accounts_user_id` (`manager_id`);

--
-- Indexes for table `orders_order`
--
ALTER TABLE `orders_order`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `order_number` (`order_number`),
ADD KEY `orders_order_created_by_id_d5f5e69c_fk_accounts_user_id` (`created_by_id`),
ADD KEY `orders_order_customer_id_0b76f6a4_fk_customers_customer_id` (`customer_id`),
ADD KEY `orders_order_farmer_id_8e35246c_fk_farmers_farmer_id` (`farmer_id`),
ADD KEY `orders_order_updated_by_id_ebcc0e59_fk_accounts_user_id` (`updated_by_id`);

--
-- Indexes for table `orders_orderdetail`
--
ALTER TABLE `orders_orderdetail`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `orders_orderdetail_order_id_product_id_61c64608_uniq` (`order_id`, `product_id`),
ADD KEY `orders_orderdetail_product_id_3ecd225e_fk_products_product_id` (`product_id`);

--
-- Indexes for table `payments_payment`
--
ALTER TABLE `payments_payment`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `payment_code` (`payment_code`),
ADD KEY `payments_payment_approved_by_id_a70548a4_fk_accounts_user_id` (`approved_by_id`),
ADD KEY `payments_payment_created_by_id_28f0e284_fk_accounts_user_id` (`created_by_id`),
ADD KEY `payments_payment_customer_id_8b4d6141_fk_customers_customer_id` (`customer_id`),
ADD KEY `payments_payment_farmer_id_1042bf33_fk_farmers_farmer_id` (`farmer_id`),
ADD KEY `payments_payment_order_id_22c479b7_fk_orders_order_id` (`order_id`);

--
-- Indexes for table `products_category`
--
ALTER TABLE `products_category`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `products_product`
--
ALTER TABLE `products_product`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `code` (`code`),
ADD KEY `products_product_unit_id_07baa821_fk_products_unit_id` (`unit_id`),
ADD KEY `products_product_category_id_9b594869_fk_products_category_id` (`category_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts_user`
--
ALTER TABLE `accounts_user`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accounts_userprofile`
--
ALTER TABLE `accounts_userprofile`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `activity_logs_activitylog`
--
ALTER TABLE `activity_logs_activitylog`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customers_customer`
--
ALTER TABLE `customers_customer`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `farmers_farmer`
--
ALTER TABLE `farmers_farmer`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory_inventorystock`
--
ALTER TABLE `inventory_inventorystock`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory_warehouse`
--
ALTER TABLE `inventory_warehouse`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders_order`
--
ALTER TABLE `orders_order`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders_orderdetail`
--
ALTER TABLE `orders_orderdetail`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payments_payment`
--
ALTER TABLE `payments_payment`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products_category`
--
ALTER TABLE `products_category`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products_product`
--
ALTER TABLE `products_product`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_userprofile`
--
ALTER TABLE `accounts_userprofile`
ADD CONSTRAINT `accounts_userprofile_user_id_92240672_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `activity_logs_activitylog`
--
ALTER TABLE `activity_logs_activitylog`
ADD CONSTRAINT `activity_logs_activi_content_type_id_7f873f46_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
ADD CONSTRAINT `activity_logs_activitylog_user_id_9ba15f3d_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `customers_customer`
--
ALTER TABLE `customers_customer`
ADD CONSTRAINT `customers_customer_user_id_a9568d6c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `inventory_inventorystock`
--
ALTER TABLE `inventory_inventorystock`
ADD CONSTRAINT `inventory_inventorys_product_id_7a8f1319_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
ADD CONSTRAINT `inventory_inventorys_warehouse_id_15bb9cd7_fk_inventory` FOREIGN KEY (`warehouse_id`) REFERENCES `inventory_warehouse` (`id`);

--
-- Constraints for table `inventory_warehouse`
--
ALTER TABLE `inventory_warehouse`
ADD CONSTRAINT `inventory_warehouse_manager_id_6def176a_fk_accounts_user_id` FOREIGN KEY (`manager_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `orders_order`
--
ALTER TABLE `orders_order`
ADD CONSTRAINT `orders_order_created_by_id_d5f5e69c_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
ADD CONSTRAINT `orders_order_customer_id_0b76f6a4_fk_customers_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers_customer` (`id`),
ADD CONSTRAINT `orders_order_farmer_id_8e35246c_fk_farmers_farmer_id` FOREIGN KEY (`farmer_id`) REFERENCES `farmers_farmer` (`id`),
ADD CONSTRAINT `orders_order_updated_by_id_ebcc0e59_fk_accounts_user_id` FOREIGN KEY (`updated_by_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `orders_orderdetail`
--
ALTER TABLE `orders_orderdetail`
ADD CONSTRAINT `orders_orderdetail_order_id_8d02dd1f_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
ADD CONSTRAINT `orders_orderdetail_product_id_3ecd225e_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`);

--
-- Constraints for table `payments_payment`
--
ALTER TABLE `payments_payment`
ADD CONSTRAINT `payments_payment_approved_by_id_a70548a4_fk_accounts_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
ADD CONSTRAINT `payments_payment_created_by_id_28f0e284_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
ADD CONSTRAINT `payments_payment_customer_id_8b4d6141_fk_customers_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers_customer` (`id`),
ADD CONSTRAINT `payments_payment_farmer_id_1042bf33_fk_farmers_farmer_id` FOREIGN KEY (`farmer_id`) REFERENCES `farmers_farmer` (`id`),
ADD CONSTRAINT `payments_payment_order_id_22c479b7_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`);

--
-- Constraints for table `products_product`
--
ALTER TABLE `products_product`
ADD CONSTRAINT `products_product_category_id_9b594869_fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`),
ADD CONSTRAINT `products_product_unit_id_07baa821_fk_products_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `products_unit` (`id`);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;