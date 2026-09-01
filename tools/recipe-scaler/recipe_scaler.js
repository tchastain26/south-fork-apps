function parseRecipe(recipeText) {
    const pattern = /(\d+)\s*([a-zA-Z]+)\s+(.*)/;
    const ingredients = [];
    
    recipeText.split('\n').forEach(line => {
        const match = line.match(pattern);
        if (match) {
            const [, quantity, unit, ingredient] = match;
            ingredients.push({ ingredient: ingredient.trim(), quantity: parseInt(quantity), unit: unit.trim() });
        }
    });
    
    return ingredients;
}

function scaleRecipe(ingredients, originalServings, newServings) {
    const scalingFactor = newServings / originalServings;
    return ingredients.map(({ ingredient, quantity, unit }) => ({
        ingredient,
        quantity: Math.round(quantity * scalingFactor),
        unit
    }));
}

function formatRecipe(scaledIngredients) {
    return scaledIngredients.map(({ ingredient, quantity, unit }) => `${quantity} ${unit} ${ingredient}`).join('\n');
}

function scaleRecipe() {
    const recipeText = document.getElementById('recipeInput').value;
    const originalServings = parseInt(document.getElementById('originalServings').value);
    const newServings = parseInt(document.getElementById('newServings').value);

    const ingredients = parseRecipe(recipeText);
    const scaledIngredients = scaleRecipe(ingredients, originalServings, newServings);
    const formattedRecipe = formatRecipe(scaledIngredients);

    document.getElementById('scaledRecipe').textContent = formattedRecipe;
}
