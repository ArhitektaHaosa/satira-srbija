<?php

if (!defined('ABSPATH')) {
    exit;
}

class Satira_Srbija_Admin
{
    public static function init(): void
    {
        add_action('admin_menu', [self::class, 'menu']);
        add_action('admin_init', [self::class, 'register_settings']);
        add_action('admin_post_satira_srbija_generate', [self::class, 'generate']);
        add_action('admin_enqueue_scripts', [self::class, 'assets']);
    }

    public static function menu(): void
    {
        add_menu_page(
            'Satira',
            'Satira',
            'edit_posts',
            'satira-srbija',
            [self::class, 'render'],
            'dashicons-format-aside',
            26
        );
    }

    public static function register_settings(): void
    {
        register_setting('satira_srbija', 'satira_srbija_middleware_url', [
            'type' => 'string',
            'sanitize_callback' => 'esc_url_raw',
        ]);
        register_setting('satira_srbija', 'satira_srbija_middleware_token', [
            'type' => 'string',
            'sanitize_callback' => 'sanitize_text_field',
        ]);
    }

    public static function assets(string $hook): void
    {
        if ($hook !== 'toplevel_page_satira-srbija') {
            return;
        }
        wp_enqueue_style('satira-srbija-admin', SATIRA_SRBIJA_URL . 'assets/admin.css', [], SATIRA_SRBIJA_VERSION);
    }

    public static function render(): void
    {
        if (!current_user_can('edit_posts')) {
            wp_die(esc_html__('No permission.', 'satira-srbija'));
        }
        $notice = isset($_GET['satira_notice']) ? sanitize_text_field(wp_unslash($_GET['satira_notice'])) : '';
        include SATIRA_SRBIJA_DIR . 'admin/views/dashboard.php';
    }

    public static function generate(): void
    {
        if (!current_user_can('edit_posts')) {
            wp_die(esc_html__('No permission.', 'satira-srbija'));
        }
        check_admin_referer('satira_srbija_generate');
        $idea = isset($_POST['idea']) ? sanitize_textarea_field(wp_unslash($_POST['idea'])) : '';
        $url = rtrim((string) get_option('satira_srbija_middleware_url'), '/');
        $token = (string) get_option('satira_srbija_middleware_token');
        if ($idea === '' || $url === '' || $token === '') {
            wp_safe_redirect(add_query_arg('satira_notice', 'missing', admin_url('admin.php?page=satira-srbija')));
            exit;
        }
        $response = wp_remote_post($url . '/v1/draft', [
            'timeout' => 180,
            'headers' => [
                'Authorization' => 'Bearer ' . $token,
                'Content-Type' => 'application/json',
            ],
            'body' => wp_json_encode(['idea' => $idea, 'push' => true]),
        ]);
        if (is_wp_error($response)) {
            wp_safe_redirect(add_query_arg('satira_notice', 'http', admin_url('admin.php?page=satira-srbija')));
            exit;
        }
        $code = wp_remote_retrieve_response_code($response);
        $body = json_decode(wp_remote_retrieve_body($response), true);
        if ($code >= 400 || empty($body['ok'])) {
            wp_safe_redirect(add_query_arg('satira_notice', 'fail', admin_url('admin.php?page=satira-srbija')));
            exit;
        }
        $edit = $body['wordpress']['edit'] ?? admin_url('edit.php');
        wp_safe_redirect($edit);
        exit;
    }
}
