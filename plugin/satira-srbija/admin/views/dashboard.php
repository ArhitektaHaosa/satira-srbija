<?php
if (!defined('ABSPATH')) {
    exit;
}
?>
<div class="wrap satira-desk">
    <h1>Satira desk</h1>
    <p>AI pravi <strong>draft</strong>. Publish ostaje tvoje dugme.</p>
    <?php if ($notice === 'missing') : ?>
        <div class="notice notice-error"><p>Idea, middleware URL i token su obavezni.</p></div>
    <?php elseif ($notice === 'http' || $notice === 'fail') : ?>
        <div class="notice notice-error"><p>Generisanje nije uspelo. Pogledaj log middleware-a. Ništa nije objavljeno.</p></div>
    <?php endif; ?>

    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
        <?php wp_nonce_field('satira_srbija_generate'); ?>
        <input type="hidden" name="action" value="satira_srbija_generate">
        <p>
            <label for="satira-idea">Nova ideja</label><br>
            <textarea id="satira-idea" name="idea" rows="6" class="large-text" required placeholder="Windows Update zatražio godišnji odmor."></textarea>
        </p>
        <?php submit_button('Generate article (draft)'); ?>
    </form>

    <hr>
    <form method="post" action="options.php">
        <?php settings_fields('satira_srbija'); ?>
        <h2>Middleware</h2>
        <p>Samo localhost ili privatni reverse proxy. Nema javnog endpointa.</p>
        <p>
            <label>URL<br>
                <input type="url" class="regular-text" name="satira_srbija_middleware_url" value="<?php echo esc_attr((string) get_option('satira_srbija_middleware_url')); ?>" placeholder="http://127.0.0.1:8787">
            </label>
        </p>
        <p>
            <label>Token<br>
                <input type="password" class="regular-text" name="satira_srbija_middleware_token" value="<?php echo esc_attr((string) get_option('satira_srbija_middleware_token')); ?>">
            </label>
        </p>
        <?php submit_button('Save connection'); ?>
    </form>
</div>
