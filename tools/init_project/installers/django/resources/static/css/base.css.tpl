/* Main CSS Entry Point */

@import url('tokens.css');
@import url('layout.css');
@import url('components.css');

/* Global Reset & Base Styles */
*, *::before, *::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: var(--font-main, system-ui, sans-serif);
    background-color: var(--color-bg);
    color: var(--color-text);
    line-height: 1.5;
}
