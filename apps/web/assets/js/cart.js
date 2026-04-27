cart = []
function addToCart(id, name, price) {
    item = { "id": Number(id), "name": name, "price": Number(price) }
    cart.push(item)
    localStorage.setItem("cart", JSON.stringify(cart))
    updateTotals()
}
function removeFromCart(id) {
    stored = localStorage.getItem('cart')
    if (!stored) {
        console.log("cart is empty")
        return
    }
    cart = JSON.parse(stored)
    const index = cart.findIndex(item => Number(item.id) === Number(id));
    if (index > -1) {
        cart.splice(index, 1);
        const element = document.querySelector(`[data-id="${id}"]`);
        if (element) element.remove();
        localStorage.setItem('cart', JSON.stringify(cart));
        updateTotals()
    }
}
function updateTotals() {
    const stored = localStorage.getItem('cart')
    const items = stored ? JSON.parse(stored) : []
    const total = items.reduce((sum, item) => sum + item.price, 0)
    document.querySelector('.total-items').textContent = items.length
    document.querySelector('.total-price').textContent = total.toFixed(2)
}
// Initialize totals on page load
function proceedToCheckout() {
    const stored = localStorage.getItem('cart')
    if (!stored) {
        alert('Cart is empty')
        return
    }
    const items = JSON.parse(stored)
    if (items.length === 0) {
        alert('Cart is empty')
        return
    }
    const total = items.reduce((sum, item) => sum + item.price, 0)
    const confirmMsg = `Checkout\n\nItems: ${items.length}\nTotal: $${total.toFixed(2)}\n\nProceed?`
    if (confirm(confirmMsg)) {
        localStorage.removeItem('cart')
        cart = []
        updateTotals()
        alert('Order placed! Thank you.')
    }
    items_list = document.getElementsByClassName("cart-items")[0];
    items_list.replaceChildren();
}