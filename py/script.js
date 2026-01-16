document.addEventListener("DOMContentLoaded", () => {
    const filterSelect = document.getElementById("filterSelect");
    const categoryList = document.getElementById("categoryList");
    const codeBlock = document.getElementById("codeBlock");
    const operationsHeader = document.getElementById("operationsHeader");

    const data = {
        problems: {
            name: "Problems API",
            operations: [
                {
                    method: "GETALL",
                    title: "Listar todos os problemas",
                    endpoint: "/problems",
                    python: `import requests

token = "dt0c01.YOUR_TOKEN"
headers = {"Authorization": f"Api-Token {token}"}

response = requests.get(
    "https://{ENV_ID}.live.dynatrace.com/api/v2/problems",
    headers=headers
)

print(response.json())`
                }
            ]
        }
    };

    function renderCategories() {
        categoryList.innerHTML = "";

        if (!filterSelect.value) {
            categoryList.innerHTML =
                '<li class="placeholder">Escolha uma categoria</li>';
            return;
        }

        data[filterSelect.value].operations.forEach(op => {
            const li = document.createElement("li");
            li.className = "category-item";
            li.textContent = op.title;

            li.onclick = () => showOperation(op);
            categoryList.appendChild(li);
        });
    }

    function showOperation(op) {
        operationsHeader.textContent = `${op.title} (${op.endpoint})`;
        codeBlock.innerHTML = `<pre>${op.python}</pre>`;
    }

    filterSelect.addEventListener("change", renderCategories);
});
