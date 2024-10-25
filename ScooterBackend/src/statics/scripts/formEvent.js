function onClickFormUpdate() {
  let form_data = document.getElementById("form_file");
  form_data.action += "/update";
  form_data.submit();
}