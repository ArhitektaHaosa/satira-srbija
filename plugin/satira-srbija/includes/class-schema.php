<?php

if (!defined('ABSPATH')) {
    exit;
}

class Satira_Srbija_Schema
{
    public static function init(): void
    {
        add_action('wp_head', [self::class, 'print_jsonld'], 30);
    }

    public static function print_jsonld(): void
    {
        if (!is_singular('post')) {
            return;
        }
        $id = get_the_ID();
        $data = [
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => wp_strip_all_tags(get_the_title()),
            'genre' => 'Satire',
            'description' => Satira_Srbija_Meta::get($id, 'satira_meta_description') ?: wp_strip_all_tags(get_the_excerpt()),
            'datePublished' => get_the_date('c'),
            'dateModified' => get_the_modified_date('c'),
            'inLanguage' => get_bloginfo('language'),
            'mainEntityOfPage' => get_permalink(),
            'author' => [
                '@type' => 'Organization',
                'name' => get_bloginfo('name'),
            ],
            'publisher' => [
                '@type' => 'Organization',
                'name' => get_bloginfo('name'),
            ],
            'isAccessibleForFree' => true,
            'creativeWorkStatus' => get_post_status($id) === 'publish' ? 'Published' : 'Draft',
            'usageInfo' => home_url('/o-sajtu/'),
            'about' => [
                '@type' => 'Thing',
                'name' => 'Satira / Parodija',
            ],
        ];
        echo '<script type="application/ld+json">' . wp_json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . '</script>' . "\n";
    }
}
