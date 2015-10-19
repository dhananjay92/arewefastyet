<?php
// Add entries for Servo in the awfy_vendor and awfy_mode.
function migrate() {
    // INSERT an entry into awfy_vendor
    mysql_query("INSERT INTO `awfy_vendor` (`id`, `name`, `vendor`, `csetURL`, `browser`, `rangeURL`) VALUES (15, 'SpiderMonkey', 'Mozilla', 'https://github.com/servo/servo/commits', 'Servo', 'https://github.com/servo/servo/compare/{from}...{to}');") or die(mysql_error());

    // Get last inserted id
    $vendor_id = mysql_insert_id();

    // INSERT into awfy_mode with inserted vendor id
    mysql_query("INSERT INTO `awfy_mode` (`id`, `vendor_id`, `mode`, `name`, `color`, `level`) VALUES (46, {$vendor_id}, 'servo', 'Servo', '#FF0000', 1);") or die(mysql_error());
}

function rollback() {
    // Delete mode first
    mysql_query("DELETE FROM `awfy_mode` WHERE `awfy_mode`.`id` = 46") or die(mysql_error());

    // Delete vendor now
    mysql_query("DELETE FROM `awfy_vendor` WHERE `awfy_vendor`.`id` = 15") or die(mysql_error());
}