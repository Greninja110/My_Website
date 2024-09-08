function dropdownmenu() {
    const dropdowns = document.querySelectorAll("#gate_drop_down");

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener("click", event => {
            // event.target.classList.remove("dropdownmenu");
            // event.target.classList.add("dropdown");
            event.target.classList.replace("dropdown" ,"dropdownmenu");
        });
    });
    
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener("mouseout", event => {
            event.target.classList.replace("dropdownmenu","dropdown");
            // event.target.classList.remove("dropdown");
            // event.target.classList.add("dropdownmenu");
        });
    });
}
