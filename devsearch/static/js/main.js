let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");
//Ensure searchForm exits
if (searchForm) {
  for (let i = 0; pageLinks.length > i; i++) {
    pageLinks[i].addEventListener("click", function (e) {
      e.preventDefault();
      //console.log('btn click');
      //GET THE DATA ATTRIBUTE
      let page = this.dataset.page;

      //Add Hidden Search input to the form
      searchForm.innerHTML += `<input value = ${page} name="page" hidden/>`;

      //Submit Form
      searchForm.submit();
    });
  }


}

function close(){
  document.getElementById('close').style.display = 'hidden';
}