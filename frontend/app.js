function search() {
    const query = document.getElementById("search-input").value.trim()
    if (!query) return
    window.location.href = `results.html?query=${encodeURIComponent(query)}`
}

document.getElementById("search-input").addEventListener("keydown", e => { 
    if (e.key === "Enter") search()
})