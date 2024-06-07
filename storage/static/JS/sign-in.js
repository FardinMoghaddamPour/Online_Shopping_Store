document.addEventListener('DOMContentLoaded', function () {
    // noinspection JSUnusedLocalSymbols
    document.getElementById('login-form').addEventListener('submit', function (event) {
        // noinspection UnnecessaryLocalVariableJS
        const localCart = localStorage.getItem('cart') || '{}';
        document.getElementById('local-cart').value = localCart;
    });

    window.addEventListener('load', function () {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('success_message')) {
            localStorage.removeItem('cart');
        }
    });
});
