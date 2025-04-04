
// for dynamically loading subpage html
document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".navigator a");
    const content = document.getElementById("dynamic-content");

    links.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            let page = this.getAttribute("data-page");
            let root = window.location.pathname.startsWith("/about") ? "/about" : "/home";

            if (!page || page === "null") {
                window.location.href = root;
                return;
            }

            fetch(`${root}/${page}`, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.text())
                .then(html => {
                    content.innerHTML = html;
                    history.pushState({ page }, "", `${root}/${page}`);
                })
                .catch(error => console.error("Error loading page:", error));
        });
    });

    window.addEventListener("popstate", function (event) {
        if (event.state && event.state.page) {
            fetch(`/home/${event.state.page}`, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.text())
                .then(html => {
                    content.innerHTML = html;
                });
        }
    });
});
