window.addEventListener("load", function() {
    const loaderContainer = document.getElementById("laoderContainer");

    setTimeout(() => {
        loaderContainer.classList.add("fade-out");
        
        setTimeout(() => {
            loaderContainer.style.display = "none"; // Oculta el loader
            document.getElementById("content").style.display = "block"; 
        }, 1000); 
    }, 1000); 
});