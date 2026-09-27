<?php

if (!defined('WP_UNINSTALL_PLUGIN')) {
    exit;
}

delete_option('satira_srbija_seeded');
delete_option('satira_srbija_middleware_url');
delete_option('satira_srbija_middleware_token');
