const fs = require('fs');
const jsonObject = JSON.parse(fs.readFileSync('./search_ingredients/search_ingredients.json', 'utf8'));


// search from text box
const allIngredientsList = jsonObject.map((item, index) => {
  return item["ingredients"];
});
const reducer = (pre, current) => {
  pre.push(...current);
  return pre;
};
const reduceIngredientsList = allIngredientsList.reduce(reducer, []);
const duplicateCheckFilter = reduceIngredientsList.filter((x, i, self) => self.indexOf(x) === i);
console.log(duplicateCheckFilter);

const output = fs.writeFileSync('search_ingredients.json', JSON.stringify(duplicateCheckFilter, null, '    '));


