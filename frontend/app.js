async function search() {
    const query = document.getElementById("search-input").value 
    const response = await fetch(`https://localhost:5000/api/search?query=${query}`)
    const data = await response.json()
    displayResults(data)
}

/*
function displayResults(restaurants) {
    const html = restaurants.map((r, index) => `
        <div class="card">
            <h2>#${index + 1} ${r.name}</h2>
            <p>${r.address}</p>
            <p>⭐ ${r.rating}</p>
            <h3>Category Scores</h3>
            <p>🍕 Food: ${r.scores.food}</p>
            <p>💁 Service: ${r.scores.service}</p>
            <p>✨ Ambiance: ${r.scores.ambiance}</p>
            <p>💰 Value: ${r.scores.value}</p>
            <p><strong>Total: ${r.scores.total}</strong></p>
        </div>
    `).join("")
    
    document.getElementById("results").innerHTML = html
}
*/