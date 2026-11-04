// Mobile Navigation
const menuButton = document.getElementById("menu-button");
const mobileMenu = document.getElementById("mobile-menu");

if (menuButton && mobileMenu) {
    menuButton.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
    });
}


// Dark Mode Toggle
const themeButtons = document.querySelectorAll("[data-theme-toggle]");
const root = document.documentElement;
const THEME_STORAGE_KEY = "theme";

function updateThemeButtons() {
    const isDark = root.classList.contains("dark");

    themeButtons.forEach((button) => {
        button.setAttribute("aria-pressed", String(isDark));
    });
}

themeButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const isDark = root.classList.toggle("dark");

        localStorage.setItem(
            THEME_STORAGE_KEY,
            isDark ? "dark" : "light"
        );

        updateThemeButtons();
    });
});

updateThemeButtons();