/*const searchResults = String(window.location.search)
  .replace("?", "")
  .replaceAll("%20", " ");
*/

function levenshteinDistance(s1, s2) {
  // Create distance matrix
  const lenS1 = s1.length;
  const lenS2 = s2.length;
  const dp = Array.from({ length: lenS1 + 1 }, () => Array(lenS2 + 1));

  // Initialize base cases
  for (let i = 0; i <= lenS1; i++) {
    dp[i][0] = i;
  }
  for (let j = 0; j <= lenS2; j++) {
    dp[0][j] = j;
  }

  // Compute distances
  for (let i = 1; i <= lenS1; i++) {
    for (let j = 1; j <= lenS2; j++) {
      const cost = s1[i - 1] === s2[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1, // Deletion
        dp[i][j - 1] + 1, // Insertion
        dp[i - 1][j - 1] + cost // Substitution
      );
    }
  }

  return dp[lenS1][lenS2];
}

function sortBySimilarity(array, word) {
  return array.slice().sort((a, b) => {
    return levenshteinDistance(a, word) - levenshteinDistance(b, word);
  });
}

const searchbar = document.getElementById("search-bar-input");
const searchOptions = document.getElementById("search-options-input")
fetch("img/search.json")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    function runResults(){
      searchOptions.innerHTML = "";
      let inputArray = (((searchbar.value).trim()).split(" "));
      let inputText = inputArray[inputArray.length - 1]
      const newItems = sortBySimilarity(data["tags"], inputText);
      newItems.forEach((element, index) => {

        if (searchOptions.getElementsByClassName("entry").length < 5) {
            if (!inputArray.includes(element)) {
              const newSearchResult = document.createElement("div");
              newSearchResult.classList.add("entry")
              newSearchResult.innerHTML = element;
              newSearchResult.addEventListener("click",()=>{searchbar.value = searchbar.value +" " +  element;runResults()})
              searchOptions.append(newSearchResult);
            }
        }
      });
      if(searchbar.value == ""){
        searchOptions.innerHTML("");
      }
    }
    searchbar.addEventListener("keypress",runResults)
  })