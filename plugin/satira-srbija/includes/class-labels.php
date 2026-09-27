<?php

if (!defined('ABSPATH')) {
    exit;
}

class Satira_Srbija_Labels
{
    public static function init(): void
    {
        add_action('wp_enqueue_scripts', [self::class, 'assets']);
        add_filter('the_content', [self::class, 'prepend'], 8);
        add_filter('the_title', [self::class, 'feed_title'], 10, 2);
        add_filter('get_the_excerpt', [self::class, 'excerpt_prefix']);
        add_filter('wp_kses_allowed_html', [self::class, 'kses'], 10, 2);
    }

    public static function assets(): void
    {
        wp_enqueue_style(
            'satira-srbija',
            SATIRA_SRBIJA_URL . 'assets/front.css',
            [],
            SATIRA_SRBIJA_VERSION
        );
    }

    public static function badge_html(): string
    {
        $url = home_url('/satira-parodija/');
        return '<p class="satira-badge"><a href="' . esc_url($url) . '">SATIRA / PARODIJA</a></p>';
    }

    public static function prepend(string $content): string
    {
        if (is_admin() || !is_singular('post') || !in_the_loop() || !is_main_query()) {
            return $content;
        }
        $prefix = self::badge_html();
        $note = Satira_Srbija_Meta::get(get_the_ID(), 'satira_inspiration_note');
        $url = Satira_Srbija_Meta::get(get_the_ID(), 'satira_inspiration_url');
        $suffix = '';
        if ($url || $note) {
            $suffix .= '<p class="satira-inspiration"><strong>Inspiracija / kontekst:</strong> ';
            $suffix .= $note ? esc_html($note) . ' ' : '';
            if ($url) {
                $suffix .= '<a href="' . esc_url($url) . '" rel="nofollow noopener">izvor</a>';
            }
            $suffix .= '</p>';
        }
        $allowed = [
            'p' => ['class' => true],
            'a' => ['href' => true, 'rel' => true],
            'strong' => [],
            'em' => [],
            'h2' => [],
            'h3' => [],
            'blockquote' => [],
            'footer' => [],
            'ul' => [],
            'ol' => [],
            'li' => [],
            'figure' => [],
            'figcaption' => [],
        ];
        return $prefix . wp_kses($content, $allowed) . $suffix;
    }

    public static function feed_title($title, $post_id = 0)
    {
        if (!is_feed() || get_post_type($post_id) !== 'post') {
            return $title;
        }
        if (stripos((string) $title, 'SATIRA') !== false) {
            return $title;
        }
        return 'SATIRA / PARODIJA — ' . $title;
    }

    public static function excerpt_prefix($excerpt)
    {
        if (!is_string($excerpt) || $excerpt === '') {
            return $excerpt;
        }
        if (stripos($excerpt, 'satir') !== false || stripos($excerpt, 'parod') !== false) {
            return $excerpt;
        }
        return 'Satira / parodija. ' . $excerpt;
    }

    public static function kses(array $tags, $context): array
    {
        if ($context !== 'post') {
            return $tags;
        }
        $tags['footer'] = [];
        $tags['figure'] = [];
        $tags['figcaption'] = [];
        return $tags;
    }
}
