<?php
/**
 * Plugin Name: Satira Srbija
 * Plugin URI:  https://github.com/ArhitektaHaosa/satira-srbija
 * Description: Forces SATIRA / PARODIJA labeling, satire schema, and draft-only AI meta on a WordPress humor site.
 * Version:     0.1.0
 * Author:      Satira Srbija
 * License:     GPL-2.0-or-later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: satira-srbija
 * Requires at least: 6.4
 * Requires PHP: 8.1
 */

if (!defined('ABSPATH')) {
    exit;
}

define('SATIRA_SRBIJA_VERSION', '0.1.0');
define('SATIRA_SRBIJA_FILE', __FILE__);
define('SATIRA_SRBIJA_DIR', plugin_dir_path(__FILE__));
define('SATIRA_SRBIJA_URL', plugin_dir_url(__FILE__));

require_once SATIRA_SRBIJA_DIR . 'includes/class-setup.php';
require_once SATIRA_SRBIJA_DIR . 'includes/class-meta.php';
require_once SATIRA_SRBIJA_DIR . 'includes/class-labels.php';
require_once SATIRA_SRBIJA_DIR . 'includes/class-schema.php';
require_once SATIRA_SRBIJA_DIR . 'includes/class-rest.php';
require_once SATIRA_SRBIJA_DIR . 'admin/class-admin.php';

register_activation_hook(__FILE__, ['Satira_Srbija_Setup', 'activate']);

add_action('plugins_loaded', static function (): void {
    Satira_Srbija_Meta::init();
    Satira_Srbija_Labels::init();
    Satira_Srbija_Schema::init();
    Satira_Srbija_Rest::init();
    if (is_admin()) {
        Satira_Srbija_Admin::init();
    }
});
