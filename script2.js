const tableSelect = document.getElementById("tableSelect");
const tableContainer = document.getElementById("tableContainer");

tableSelect.addEventListener("change", () => {
    const selectedTable = tableSelect.value;

    fetch(`/api/${selectedTable}`)
        .then(response => response.json())
        .then(data => {
            const tableHtml = generateTableHtml(data);
            tableContainer.innerHTML = tableHtml;
        })
        .catch(error => console.error("Error fetching data:", error));
});

function generateTableHtml(data) {
    if (data && data.length > 0) {
        const columns = Object.keys(data[0]);

        const tableHeader = `<thead><tr>${columns.map(column => `<th>${column}</th>`).join("")}</tr></thead>`;

        const tableRows = data.map(row => `<tr>${columns.map(column => `<td>${row[column]}</td>`).join("")}</tr>`).join("");

        const tableHtml = `<table class="table table-striped table-bordered">${tableHeader}<tbody>${tableRows}</tbody></table>`;
        return tableHtml;
    } else {
        // If data is empty, display a message
        return "<p>No data available for the selected table.</p>";
    }
}
