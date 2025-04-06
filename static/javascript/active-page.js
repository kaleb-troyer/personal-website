
function updateActiveLinks() {
    const links = document.querySelectorAll(".navigator a, header a");
    const currentPath = window.location.pathname;

    links.forEach(link => {
        link.classList.remove("active"); 
        const href = link.getAttribute("href");

        if (currentPath === "/home" && href.includes("/home/skills")) {
            link.classList.add("active");
        } 

        else if (currentPath === "/" && href.includes("/home/skills")) {
            link.classList.add("active");
        } 

        else if (currentPath === "/" && href === "/home") {
            link.classList.add("active");
        } 

        else if (currentPath === "/about" && href.includes("/about/interests")) {
            link.classList.add("active");
        }

        else if (href && currentPath.includes(href)) {
            link.classList.add("active");
        }
    });
}

