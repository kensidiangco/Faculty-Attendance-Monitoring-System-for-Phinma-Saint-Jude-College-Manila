/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
       // Templates within theme app (e.g. base.html)
       '../templates/**/*.html',
       // Templates in other apps
       '../../templates/**/*.html',
       // Ignore files in node_modules
       '!../../**/node_modules',
       // Include JavaScript files that might contain Tailwind CSS classes
       '../../**/*.js',
       // Include Python files that might contain Tailwind CSS classes
       '../../**/*.py'
    ],
    theme: {
        colors: {
            'bg-sjc-green': '#52735D',
            'bg-sjc-item-green': '#355C41',
            'bg-sjc-th-green': '#52735D',
        },

        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
