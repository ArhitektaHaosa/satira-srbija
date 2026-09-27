from satira.validator import validate_article

VALID = {
    "title": "Windows Update zatražio godišnji odmor",
    "slug": "windows-update-trazio-godisnji-odmor",
    "excerpt": "Satira: sistemske zakrpe traže kolektivni ugovor i dve nedelje na Tari.",
    "content_html": """
<p>U redakciji ove parodije, zakrpe su stavile slušalice i rekle da će se vratiti u januaru.</p>
<h2>Sindikat drajvera</h2>
<p>Prema ovoj satiri, noćni restart nije nestao. Samo je dobio formular.</p>
<blockquote><p>Ne dirajte ništa do ponedeljka.</p><footer>Iz satiričnog članka, nije izjava stvarne osobe.</footer></blockquote>
<h2>Kraj smene</h2>
<p>Računar je ostao da čeka. To je poenta.</p>
<p><em>Ovaj tekst je satira/parodija.</em></p>
""",
    "category": "Tehnologija",
    "tags": ["windows", "update", "sysadmin"],
    "featured_image_prompt": "Flat satirical illustration of a packing suitcase full of patches, no logos.",
    "alt_text": "Kofer pun zakrpa spreman za odmor",
    "seo_title": "Windows Update na odmoru — satira",
    "meta_description": "Parodija o zakrpama koje traže godišnji. Nije vest.",
    "social_title": "Zakrpe idu na Taru",
    "social_description": "Satirični tekst o Windows Update-u koji traži slobodne dane.",
    "satire_label": "Satira / Parodija",
    "layers": {
        "fact": "Windows Update exists and reboots machines.",
        "satire": "The updater demands annual leave.",
        "fictional_quote": "Ne dirajte ništa do ponedeljka.",
        "editorial_comment": "Maintenance windows already feel like labor law.",
    },
}


def test_valid_passes():
    assert validate_article(VALID) == []


def test_rejects_missing_label():
    bad = dict(VALID)
    bad["satire_label"] = "Vest"
    assert any("satire_label" in e for e in validate_article(bad))
