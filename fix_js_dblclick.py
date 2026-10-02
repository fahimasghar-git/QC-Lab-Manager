import re
path = '/Users/fahimasghar/Documents/QC-Lab-Manager/static_assets/js/custom_admin.js'
with open(path, 'r') as f:
    content = f.read()

dblclick_code = """
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
"""

# Insert before "let isResizing = false;"
content = content.replace('let isResizing = false;', dblclick_code + '\n    let isResizing = false;')

with open(path, 'w') as f:
    f.write(content)
