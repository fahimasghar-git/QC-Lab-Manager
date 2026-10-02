document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("nav-sidebar");
    if (!sidebar) return;

    const wrapper = sidebar.closest('.w-\\[288px\\]');
    
    // Create a resize handle
    const resizer = document.createElement("div");
    resizer.style.setProperty("width", "6px", "important");
    resizer.style.setProperty("cursor", "ew-resize", "important");
    resizer.style.setProperty("position", "absolute", "important");
    resizer.style.setProperty("top", "0", "important");
    resizer.style.setProperty("right", "0", "important");
    resizer.style.setProperty("bottom", "0", "important");
    resizer.style.setProperty("z-index", "100", "important");
    resizer.style.setProperty("background-color", "transparent", "important");
    
    // Hover effect
    resizer.addEventListener('mouseenter', () => resizer.style.setProperty("background-color", "#3b82f6", "important"));
    resizer.addEventListener('mouseleave', () => resizer.style.setProperty("background-color", "transparent", "important"));

    sidebar.appendChild(resizer);

    
    // Double-click to snap back to default width
    resizer.addEventListener("dblclick", function(e) {
        const defaultWidth = "288px";
        
        // Add a smooth transition for the snap
        sidebar.style.setProperty("transition", "width 0.2s ease-out", "important");
        if (wrapper) wrapper.style.setProperty("transition", "width 0.2s ease-out", "important");
        
        sidebar.style.setProperty("width", defaultWidth, "important");
        if (wrapper) wrapper.style.setProperty("width", defaultWidth, "important");
        
        // Remove transition shortly after so regular dragging remains instantly responsive
        setTimeout(() => {
            sidebar.style.removeProperty("transition");
            if (wrapper) wrapper.style.removeProperty("transition");
        }, 200);
        
        e.preventDefault();
    });

    let isResizing = false;

    resizer.addEventListener("mousedown", function(e) {
        isResizing = true;
        document.body.style.setProperty("cursor", "ew-resize", "important");
        e.preventDefault();
    });

    document.addEventListener("mousemove", function(e) {
        if (!isResizing) return;
        
        // Calculate new width
        let newWidth = e.clientX;
        if (newWidth < 200) newWidth = 200;
        if (newWidth > window.innerWidth / 2) newWidth = window.innerWidth / 2;
        
        sidebar.style.setProperty("width", newWidth + "px", "important");
        if (wrapper) {
            wrapper.style.setProperty("width", newWidth + "px", "important");
        }
    });

    document.addEventListener("mouseup", function() {
        if (isResizing) {
            isResizing = false;
            document.body.style.setProperty("cursor", "default", "important");
        }
    });
});
