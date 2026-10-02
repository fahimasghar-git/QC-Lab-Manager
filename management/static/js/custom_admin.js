document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("nav-sidebar");
    if (!sidebar) return;

    const wrapper = sidebar.closest('.w-\\[288px\\]');
    if (!wrapper) return;

    // Create a resize handle
    const resizer = document.createElement("div");
    resizer.style.width = "5px";
    resizer.style.cursor = "ew-resize";
    resizer.style.position = "absolute";
    resizer.style.top = "0";
    resizer.style.right = "0";
    resizer.style.bottom = "0";
    resizer.style.zIndex = "100";
    resizer.style.backgroundColor = "transparent";
    
    // Hover effect
    resizer.addEventListener('mouseenter', () => resizer.style.backgroundColor = "#3b82f6");
    resizer.addEventListener('mouseleave', () => resizer.style.backgroundColor = "transparent");

    sidebar.appendChild(resizer);
    

    let isResizing = false;

    resizer.addEventListener("mousedown", function(e) {
        isResizing = true;
        document.body.style.cursor = "ew-resize";
        // Prevent text selection during drag
        e.preventDefault();
    });

    document.addEventListener("mousemove", function(e) {
        if (!isResizing) return;
        
        // Calculate new width
        let newWidth = e.clientX;
        if (newWidth < 200) newWidth = 200;
        if (newWidth > window.innerWidth / 2) newWidth = window.innerWidth / 2;
        
        sidebar.style.width = newWidth + "px";
        wrapper.style.width = newWidth + "px";
    });

    document.addEventListener("mouseup", function() {
        if (isResizing) {
            isResizing = false;
            document.body.style.cursor = "default";
        }
    });
});
