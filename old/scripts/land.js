const landing_imageBackground = document.getElementById(
  "landing-background-image"
);
const landing_imageBackgroundBackground = document.getElementById(
  "landing-background-image-background"
);
fetch("img/index.json")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    var count = Object.keys(data).length - 1;
    var timing = 30000 + 10; //ms
    // data and length ( count )
    let image = "";
    getNewImage();
    function getNewImage() {
      let imageTmp = `url(${
        data[Math.floor(Math.random() * count)]["img_local"]
      })`;
      console.log("------");
      console.log(imageTmp);
      if (imageTmp == image) {
        getNewImage();
      } else {
        image = imageTmp;
      }
    }
    function setBackground() {
      landing_imageBackground.style.backgroundImage = image;
      landing_imageBackground.classList.remove("image-animation-call");
      void landing_imageBackground.offsetWidth;
      landing_imageBackground.classList.add("image-animation-call");
      getNewImage();
      landing_imageBackgroundBackground.style.backgroundImage = image;
    }

    setBackground();
    setInterval(() => {
      setBackground();
    }, timing);
  });
