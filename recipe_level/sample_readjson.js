const fs = require('fs');
const jsonObject = JSON.parse(fs.readFileSync('./search_ingredients/dbdata_ingredients.json', 'utf8'));


// search from text box **********
const allIngredientsList = jsonObject.map((item, index) => {
  return item["ingredients"];
});
const reducer = (pre, current) => {
  pre.push(...current);
  return pre;
};
const reduceIngredientsList = allIngredientsList.reduce(reducer, []);
const duplicateCheckFilter = reduceIngredientsList.filter((x, i, self) => self.indexOf(x) === i);
// console.log(duplicateCheckFilter);


// serch by value *****************
const searchByValue = (data, query) => {
  let condition;
  let targetList = data.filter(function(item, index) {
    condition = item['ingredients'].indexOf(query);
    // console.log(condition);
    // console.log(condition != -1);
    if (condition != -1) {
      return true;
    } else {
      return false;
    }
  });
  return targetList;
};
// console.log(searchByValue(jsonObject, 'だし'));
let searchResult = searchByValue(jsonObject, 'だし');
// ********************************

// level filter *******************
const LOWER_THRESHOLD = 4;
const UPPER_THRESHOLD = 14;
const levelFilter = (data, condition) => {
  let numofdata;
  let filterData = data.filter((item, index) => {
    numofdata = item['numof'];
    switch(condition) {
    case 'easy':
      if (numofdata <= LOWER_THRESHOLD) {
        return true;
      } else {
        return false;
      }
      break;
    case 'standard':
      if (LOWER_THRESHOLD < numofdata && numofdata < UPPER_THRESHOLD) {
        return true;
      } else {
        return false;
      }
      break;
    case 'authentic':
      // console.log(UPPER_THRESHOLD <= numofdata);
      if (UPPER_THRESHOLD < numofdata) {
        return true;
      } else {
        return false;
      }
      break;
    default:
      break;
    }
  });
  return filterData;
};
let filterResult = levelFilter(searchResult, 'standard');
// console.log(filterResult);
// console.log(filterResult.length);
// ********************************

// console.log('**************** sorted before ****************');
// console.log('**************** sorted after  ****************');

// sort by main or side************
const recipeSort = (recipelist) => {
  recipelist.sort((a, b) => {
    if (b.main_or_side === '主菜・主食') {
      return 1;
    } else {
      return -1;
    }
  });
  return recipelist;
};

let sortedList = recipeSort(filterResult);
console.log(sortedList);
// ********************************

// display for each 3 recipes *****
const layoutElemens = (arr, size) => {
  return arr.reduce(
    (newarr, _, i) => (i % size ? newarr : [...newarr, arr.slice(i, i + size)]),
    []
  );
};
console.log(layoutElemens(sortedList, 3));
// ********************************
