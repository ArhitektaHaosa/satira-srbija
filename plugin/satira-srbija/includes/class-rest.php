<?php

if (!defined('ABSPATH')) {
    exit;
}

class Satira_Srbija_Rest
{
    public static function init(): void
    {
        add_filter('content_save_pre', [self::class, 'sanitize_incoming']);
    }

    public static function sanitize_incoming($content)
    {
        if (!is_string($content)) {
            return $content;
        }
        $post_type = isset($_POST['post_type']) ? sanitize_key(wp_unslash($_POST['post_type'])) : 'post';
        if ($post_type !== 'post') {
            return $content;
        }
        $allowed = [
            'h2' => [],
            'h3' => [],
            'p' => [],
            'blockquote' => [],
            'strong' => [],
            'em' => [],
            'ul' => [],
            'ol' => [],
            'li' => [],
            'figure' => [],
            'figcaption' => [],
            'footer' => [],
        ];
        return wp_kses($content, $allowed);
    }
}
