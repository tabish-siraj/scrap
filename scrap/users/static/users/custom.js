document.addEventListener('DOMContentLoaded', function () {
    // Get all quantity inputs and add an input event listener to each
    var quantityInputs = document.querySelectorAll('.quantity-input');

    quantityInputs.forEach(function (input) {
        input.addEventListener('input', function () {
            // Get the material name from the input ID
            var materialName = input.id.replace('_quantity', '');

            // Get the quantity, rate, and total elements
            var quantity = parseFloat(input.value) || 0;
            var rate = parseFloat(document.getElementById(materialName + '_rate').textContent) || 0;
            var totalElement = document.getElementById(materialName + '_total');

            // Calculate the total and update the total input
            var total = quantity * rate;
            totalElement.value = isNaN(total) ? '' : total.toFixed(2);
        });
    });
});
