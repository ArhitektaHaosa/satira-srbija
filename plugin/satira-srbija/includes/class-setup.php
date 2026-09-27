<?php

if (!defined('ABSPATH')) {
    exit;
}

class Satira_Srbija_Setup
{
    public const CATEGORIES = [
        'politika' => 'Politika',
        'tehnologija' => 'Tehnologija',
        'ai' => 'AI',
        'internet' => 'Internet',
        'drustvo' => 'Društvo',
        'biznis' => 'Biznis',
        'kultura' => 'Kultura',
        'sport' => 'Sport',
        'svet' => 'Svet',
        'srbija' => 'Srbija',
        'apsurd-dana' => 'Apsurd dana',
    ];

    public static function activate(): void
    {
        foreach (self::CATEGORIES as $slug => $name) {
            if (!term_exists($slug, 'category')) {
                wp_insert_term($name, 'category', ['slug' => $slug]);
            }
        }

        self::ensure_page(
            'o-sajtu',
            'O sajtu / Disclaimer',
            self::disclaimer_html()
        );
        self::ensure_page(
            'satira-parodija',
            'SATIRA / PARODIJA',
            self::label_html()
        );

        if (!get_option('permalink_structure')) {
            update_option('permalink_structure', '/%category%/%postname%/');
            flush_rewrite_rules();
        }

        update_option('satira_srbija_seeded', time());
    }

    private static function ensure_page(string $slug, string $title, string $content): void
    {
        $found = get_page_by_path($slug);
        if ($found instanceof WP_Post) {
            return;
        }
        wp_insert_post([
            'post_type' => 'page',
            'post_status' => 'publish',
            'post_name' => $slug,
            'post_title' => $title,
            'post_content' => $content,
            'post_author' => get_current_user_id() ?: 1,
        ]);
    }

    private static function disclaimer_html(): string
    {
        return <<<HTML
<p><strong>Ovaj sajt objavljuje satiru i parodiju.</strong> Tekstovi su humoristički, izmišljeni ili satirično obrađeni. Nisu novinske vesti.</p>
<p>Vidljiva oznaka na člancima glasi <strong>SATIRA / PARODIJA</strong>. Ako je ne vidite, ne čitajte tekst kao izveštaj.</p>
<p>Pojedine reference na stvarne osobe, firme ili događaje postoje samo kao materijal za parodiju. Izmišljeni citati nisu izjave tih osoba.</p>
<p>Sajt ne daje pravne, medicinske ni finansijske savete. Tumačenje je na čitaocu.</p>
<p>Ako smatrate da neki tekst prelazi granicu parodije, pišite uredništvu preko kontakt forme sajta.</p>
HTML;
    }

    private static function label_html(): string
    {
        return <<<HTML
<p><strong>SATIRA / PARODIJA</strong> znači da je tekst namerno izmišljen ili preuveličan radi humora i društvene kritike.</p>
<p>Naslov može da zvuči kao vest. Telo teksta ne sme da se čita kao vest. Ako neko prenese članak bez oznake, prenela je lažnu vest — ne satiru.</p>
HTML;
    }
}
