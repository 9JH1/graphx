//landing page 
const landing_imageBackground = document.getElementById("landing-background-image");

function landingPageImageAnimation() {
    fetch("../img/index.json")
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            var count = (Object.keys(data).length)-1;
            // data and length ( count ) 
            // ;
            // background-image: url(/img/banners/banner.png);
            landing_imageBackground.style.backgroundImage
            setInterval(()=>{
                landing_imageBackground.style.backgroundImage = `url(${data[Math.floor(Math.random()*count)]["img_local"]})`
            },12000)
        })
}

landingPageImageAnimation()