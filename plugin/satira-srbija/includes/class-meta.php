<?php

if (!defined('ABSPATH')) {
    exit;
}

class Satira_Srbija_Meta
{
    public const KEYS = [
        'satira_label' => 'Satira / Parodija',
        'satira_seo_title' => '',
        'satira_meta_description' => '',
        'satira_social_title' => '',
        'satira_social_description' => '',
        'satira_image_prompt' => '',
        'satira_alt_text' => '',
        'satira_inspiration_url' => '',
        'satira_inspiration_note' => '',
    ];

    public static function init(): void
    {
        add_action('init', [self::class, 'register']);
        add_action('save_post_post', [self::class, 'save_metabox'], 10, 2);
        add_action('add_meta_boxes', [self::class, 'metabox']);
        add_filter('pre_get_document_title', [self::class, 'document_title'], 20);
        add_action('wp_head', [self::class, 'meta_tags'], 5);
    }

    public static function register(): void
    {
        foreach (array_keys(self::KEYS) as $key) {
            register_post_meta('post', $key, [
                'type' => 'string',
                'single' => true,
                'show_in_rest' => true,
                'auth_callback' => static function (): bool {
                    return current_user_can('edit_posts');
                },
                'sanitize_callback' => 'sanitize_text_field',
            ]);
        }
    }

    public static function metabox(): void
    {
        add_meta_box(
            'satira-srbija-meta',
            'Satira polja',
            [self::class, 'render_metabox'],
            'post',
            'normal',
            'high'
        );
    }

    public static function render_metabox(WP_Post $post): void
    {
        wp_nonce_field('satira_srbija_meta', 'satira_srbija_meta_nonce');
        echo '<p><label>Oznaka<br><input type="text" class="widefat" name="satira_label" value="' . esc_attr(self::get($post->ID, 'satira_label') ?: 'Satira / Parodija') . '"></label></p>';
        echo '<p><label>SEO title<br><input type="text" class="widefat" name="satira_seo_title" value="' . esc_attr(self::get($post->ID, 'satira_seo_title')) . '"></label></p>';
        echo '<p><label>Meta description<br><textarea class="widefat" rows="3" name="satira_meta_description">' . esc_textarea(self::get($post->ID, 'satira_meta_description')) . '</textarea></label></p>';
        echo '<p><label>Social title<br><input type="text" class="widefat" name="satira_social_title" value="' . esc_attr(self::get($post->ID, 'satira_social_title')) . '"></label></p>';
        echo '<p><label>Social description<br><textarea class="widefat" rows="3" name="satira_social_description">' . esc_textarea(self::get($post->ID, 'satira_social_description')) . '</textarea></label></p>';
        echo '<p><label>Image prompt<br><textarea class="widefat" rows="3" name="satira_image_prompt">' . esc_textarea(self::get($post->ID, 'satira_image_prompt')) . '</textarea></label></p>';
        echo '<p><label>ALT<br><input type="text" class="widefat" name="satira_alt_text" value="' . esc_attr(self::get($post->ID, 'satira_alt_text')) . '"></label></p>';
        echo '<p><label>Inspiration URL<br><input type="url" class="widefat" name="satira_inspiration_url" value="' . esc_attr(self::get($post->ID, 'satira_inspiration_url')) . '"></label></p>';
        echo '<p><label>Inspiration note<br><input type="text" class="widefat" name="satira_inspiration_note" value="' . esc_attr(self::get($post->ID, 'satira_inspiration_note')) . '"></label></p>';
    }

    public static function save_metabox(int $post_id, WP_Post $post): void
    {
        if (!isset($_POST['satira_srbija_meta_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['satira_srbija_meta_nonce'])), 'satira_srbija_meta')) {
            return;
        }
        if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
            return;
        }
        if (!current_user_can('edit_post', $post_id)) {
            return;
        }
        foreach (array_keys(self::KEYS) as $key) {
            if (!isset($_POST[$key])) {
                continue;
            }
            $value = sanitize_text_field(wp_unslash($_POST[$key]));
            if ($key === 'satira_label' && $value === '') {
                $value = 'Satira / Parodija';
            }
            update_post_meta($post_id, $key, $value);
        }
    }

    public static function get(int $post_id, string $key): string
    {
        $value = get_post_meta($post_id, $key, true);
        if ($key === 'satira_label' && !$value) {
            return 'Satira / Parodija';
        }
        return is_string($value) ? $value : '';
    }

    public static function document_title($title)
    {
        if (!is_singular('post')) {
            return $title;
        }
        $custom = self::get(get_the_ID(), 'satira_seo_title');
        return $custom !== '' ? $custom : $title;
    }

    public static function meta_tags(): void
    {
        if (!is_singular('post')) {
            return;
        }
        $id = get_the_ID();
        $desc = self::get($id, 'satira_meta_description');
        if ($desc) {
            echo '<meta name="description" content="' . esc_attr($desc) . '">' . "\n";
        }
        $og_title = self::get($id, 'satira_social_title') ?: get_the_title();
        $og_desc = self::get($id, 'satira_social_description') ?: $desc;
        echo '<meta property="og:type" content="article">' . "\n";
        echo '<meta property="og:title" content="' . esc_attr('SATIRA / PARODIJA — ' . $og_title) . '">' . "\n";
        if ($og_desc) {
            echo '<meta property="og:description" content="' . esc_attr($og_desc) . '">' . "\n";
        }
        echo '<meta property="og:url" content="' . esc_url(get_permalink()) . '">' . "\n";
        if (has_post_thumbnail($id)) {
            $src = wp_get_attachment_image_url(get_post_thumbnail_id($id), 'large');
            if ($src) {
                echo '<meta property="og:image" content="' . esc_url($src) . '">' . "\n";
            }
        }
        echo '<link rel="canonical" href="' . esc_url(get_permalink()) . '">' . "\n";
    }
}
