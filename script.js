const cryptoContainer = document.getElementById("crypto-container");
const loader = document.getElementById("loader");

async function fetchData() {
  loader.style.display = "block";
  cryptoContainer.innerHTML = "";

  try {
    const response = await fetch(
      "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=200&page=1&sparkline=false"
    );
    const data = await response.json();

    loader.style.display = "none";

    data.forEach((coin) => {
      const card = document.createElement("div");
      card.classList.add("coin-card");

      card.innerHTML = `
        <img src="${coin.image}" alt="${coin.name}">
        <h2>${coin.name}</h2>
        <p>$${coin.current_price.toLocaleString()}</p>
        <span class="${coin.price_change_percentage_24h >= 0 ? "positive" : "negative"}">
          ${coin.price_change_percentage_24h.toFixed(2)}%
        </span>
      `;
      cryptoContainer.appendChild(card);
    });
  } catch (error) {
    console.error("Error fetching data:", error);
    loader.innerText = "Failed to load data!";
  }
}

fetchData();
setInterval(fetchData, 60000); // auto-refresh every 60s