const addProductBtn = document.querySelector('.product-add-to-cart-js')

addProductBtn.addEventListener('click', addProductClick)

function addProductClick() {
    console.log("Add product...");
    const sizeSelect = document.getElementById("size-select");
    const selectedOption = sizeSelect.selectedOptions[0];
    const prodData = selectedOption.getAttribute('data-product');
    localStorage.setItem("PRODUCT_VARIANT_ID", prodData);
    console.log(prodData.price);
}
