const cryptoContainer = document.getElementById('crypto-container');
const loader = document.getElementById('loader');

const coins = [
  {id:'bitcoin', name:'Bitcoin', logo:'https://assets.coingecko.com/coins/images/1/large/bitcoin.png'},
  {id:'ethereum', name:'Ethereum', logo:'https://assets.coingecko.com/coins/images/279/large/ethereum.png'},
  {id:'dogecoin', name:'Dogecoin', logo:'https://assets.coingecko.com/coins/images/5/large/dogecoin.png'}
];
const apiUrl = `https://api.coingecko.com/api/v3/simple/price?ids=${coins.map(c=>c.id).join(',')}&vs_currencies=usd`;

let isFetching = false;

async function fetchCryptoPrices() {
    if(isFetching) return;
    isFetching = true;

    loader.classList.remove('hidden');
    cryptoContainer.classList.add('hidden');

    try {
        const response = await fetch(apiUrl);

        if(!response.ok) throw new Error(`Network response not ok: ${response.status}`);

        // Parse JSON safely
        let data;
        try {
            data = await response.json();
        } catch(parseError) {
            throw new Error("Failed to parse JSON: " + parseError.message);
        }

        console.log("Fetched data:", data);
        displayPrices(data);

    } catch(error) {
        console.error("Fetch error:", error);
        cryptoContainer.innerHTML = `<p style="color:red;">Could not fetch data. Please try again later.<br>${error.message}</p>`;
        loader.classList.add('hidden');
        cryptoContainer.classList.remove('hidden');
        isFetching = false;
    }
}

function displayPrices(data){
    cryptoContainer.innerHTML = '';

    coins.forEach(coin=>{
        const price = data[coin.id]?.usd ?? 'N/A';

        const card = document.createElement('div');
        card.className = 'crypto-card';
        card.innerHTML = `
            <img src="${coin.logo}" class="crypto-logo" alt="${coin.name} logo">
            <span class="crypto-name">${coin.name}</span>
            <span class="crypto-price">$${typeof price === 'number' ? price.toLocaleString() : price}</span>
        `;
        cryptoContainer.appendChild(card);
    });

    const timestamp = new Date().toLocaleTimeString();
    const timeEl = document.createElement('div');
    timeEl.className = 'update-time';
    timeEl.textContent = `Last updated: ${timestamp}`;
    cryptoContainer.appendChild(timeEl);
}
// Initial fetch and auto-refresh every 10 seconds
fetchCryptoPrices();
setInterval(fetchCryptoPrices, 10000);