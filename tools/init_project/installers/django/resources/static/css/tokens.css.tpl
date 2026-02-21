:root {
    /* Colors */
    --color-primary: #3b82f6;
    --color-bg: #ffffff;
    --color-text: #1f2937;
    --color-surface: #f3f4f6;

    /* Spacing */
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 2rem;

    /* Typography */
    --font-main: 'Inter', system-ui, sans-serif;
}

@media (prefers-color-scheme: dark) {
    :root {
        --color-bg: #111827;
        --color-text: #f9fafb;
        --color-surface: #1f2937;
    }
}
