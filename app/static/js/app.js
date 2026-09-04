const uploadForm =
    document.getElementById("uploadForm");


const csvFile =
    document.getElementById("csvFile");


const processButton =
    document.getElementById("processButton");


const status =
    document.getElementById("status");


const results =
    document.getElementById("results");


uploadForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // ====================================================
        // VALIDAR ARCHIVO
        // ====================================================

        if (!csvFile.files.length) {

            status.textContent =
                "Selecciona un archivo CSV.";

            return;
        }


        const file =
            csvFile.files[0];


        if (
            !file.name
                .toLowerCase()
                .endsWith(".csv")
        ) {

            status.textContent =
                "El archivo debe ser CSV.";

            return;
        }


        // ====================================================
        // PREPARAR PETICIÓN
        // ====================================================

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );


        processButton.disabled =
            true;

        processButton.textContent =
            "Procesando...";


        status.textContent =
            "Calculando prioridades y ordenando envíos...";


        try {

            const response =
                await fetch(
                    "/process",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Ocurrió un error."
                );
            }


            // =================================================
            // MOSTRAR RESULTADOS
            // =================================================

            showResults(data);


            status.textContent =
                "Procesamiento completado correctamente.";

        }


        catch (error) {

            status.textContent =
                error.message;

        }


        finally {

            processButton.disabled =
                false;

            processButton.textContent =
                "Generar priorización";
        }

    }
);


// ============================================================
// MOSTRAR RESULTADOS
// ============================================================

function showResults(data) {

    results.classList.remove(
        "hidden"
    );


    // ========================================================
    // MÉTRICAS
    // ========================================================

    document.getElementById(
        "totalShipments"
    ).textContent =
        data.total_shipments;


    document.getElementById(
        "priorityTime"
    ).textContent =
        `${data.processing_time.priority_score} s`;


    document.getElementById(
        "mergeTime"
    ).textContent =
        `${data.processing_time.merge_sort} s`;


    // ========================================================
    // DISTRIBUCIÓN
    // ========================================================

    const distribution =
        document.getElementById(
            "priorityDistribution"
        );


    distribution.innerHTML = "";


    const priorities = [
        "Alta",
        "Media",
        "Baja"
    ];


    priorities.forEach(
        function (priority) {

            const count =
                data.priority_distribution[
                    priority
                ] || 0;


            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "priority-item";


            item.innerHTML = `
                <span>${priority}</span>
                <strong>${count}</strong>
            `;


            distribution.appendChild(
                item
            );

        }
    );


    // ========================================================
    // TOP 10
    // ========================================================

    const table =
        document.getElementById(
            "shipmentsTable"
        );


    table.innerHTML = "";


    data.top_shipments.forEach(
        function (shipment) {

            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `
                <td>${shipment.Order_ID}</td>
                <td>${shipment.Priority_Score}</td>
                <td>${shipment.Priority_Level}</td>
                <td>${shipment.Traffic ?? "-"}</td>
                <td>${shipment.Weather ?? "-"}</td>
                <td>${shipment.Area ?? "-"}</td>
                <td>${shipment.Order_Hour ?? "-"}</td>
            `;


            table.appendChild(
                row
            );

        }
    );

}