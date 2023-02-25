let login = document.getElementById("login");
let password = document.getElementById("password");
let submit = document.getElementById("submit");
let upload = document.getElementById("btn-upload");
let inputSection = document.getElementById("input-section");

const hello = document.getElementById("hello");

upload.addEventListener("click", () => {
  inputSection.innerHTML = ` 
  <form action=""
  method="post"
  enctype="multipart/form-data">

<input type="file"
     name="my_video"
  class='button'>

<input type="submit"
     name="submit" 
     value="Upload"
  class="button">
</form>`;

  
});


