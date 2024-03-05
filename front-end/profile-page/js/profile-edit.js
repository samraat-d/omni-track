var loadFile = function (event) {
    var image = document.getElementById("output_img");
    image.src = URL.createObjectURL(event.target.files[0]);
  };