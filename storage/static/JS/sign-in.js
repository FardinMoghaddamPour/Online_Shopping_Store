document.addEventListener('DOMContentLoaded', function () {
    // noinspection JSUnusedLocalSymbols
    document.getElementById('login-form').addEventListener('submit', function (event) {
        // noinspection UnnecessaryLocalVariableJS
        const localCart = localStorage.getItem('cart') || '{}';
        document.getElementById('local-cart').value = localCart;
    });
});
