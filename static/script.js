document
    .getElementById("quote-btn")
    .addEventListener("click", getQuote);

async function getQuote() {

    const response = await fetch("/quote");
    const data = await response.json();

    document.getElementById("quote-box").innerHTML =
        `"${data.quote}" <br><br> - ${data.author}`;

    loadHistory();
}

async function loadHistory() {

    const response = await fetch("/history");

    const history = await response.json();

    let html = "";

    history.forEach(item => {
        html += `<li>"${item[0]}" - ${item[1]}</li>`;
    });

    document.getElementById("history-list").innerHTML = html;
}

loadHistory();