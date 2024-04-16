var loadFile = function (event) {
    var image = document.getElementById("img-profile");
    image.src = URL.createObjectURL(event.target.files[0]);
  };