const uploadForm = document.getElementById("uploadForm");
const csvFile = document.getElementById("csvFile");
const processButton = document.getElementById("processButton");
const status = document.getElementById("status");
const results = document.getElementById("results");

// Elementos del benchmark
const benchmarkButton = document.getElementById("benchmarkButton");
const benchmarkStatus = document.getElementById("benchmarkStatus");
const benchmarkResults = document.getElementById("benchmarkResults");
const benchmarkTable = document.getElementById("benchmarkTable");
const benchmarkChart = document.getElementById("benchmarkChart");
const benchmarkBestSpeedup = document.getElementById("benchmarkBestSpeedup");


// ============================================================
// PROCESAR ARCHIVO CSV
// ============================================================

uploadForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (!csvFile.files.length) {
        status.textContent = "Selecciona un archivo CSV.";
        return;
    }

    const file = csvFile.files[0];

    if (!file.name.toLowerCase().endsWith(".csv")) {
        status.textContent = "El archivo debe ser CSV.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    processButton.disabled = true;
    processButton.textContent = "Procesando...";
    status.textContent = "Calculando prioridades y ordenando envíos...";

    if (benchmarkResults) {
        benchmarkResults.classList.add("hidden");
    }

    if (benchmarkStatus) {
        benchmarkStatus.textContent = "";
    }

    try {
        const response = await fetch("/process", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Ocurrió un error al procesar el archivo."
            );
        }

        showResults(data);
        status.textContent = "Procesamiento completado correctamente.";
    } catch (error) {
        status.textContent = error.message;
    } finally {
        processButton.disabled = false;
        processButton.textContent = "Generar priorización";
    }
});


// ============================================================
// MOSTRAR RESULTADOS DEL PROCESAMIENTO
// ============================================================

function showResults(data) {
    results.classList.remove("hidden");

    document.getElementById("totalShipments").textContent =
        Number(data.total_shipments).toLocaleString("es-CO");

    document.getElementById("priorityTime").textContent =
        `${data.processing_time.priority_score} s`;

    document.getElementById("mergeTime").textContent =
        `${data.processing_time.merge_sort} s`;

    // Distribución de prioridades
    const distribution = document.getElementById("priorityDistribution");
    distribution.innerHTML = "";

    const priorities = ["Alta", "Media", "Baja"];

    priorities.forEach(function (priority) {
        const count = data.priority_distribution[priority] || 0;

        const item = document.createElement("div");
        item.className = "priority-item";

        const label = document.createElement("span");
        label.textContent = priority;

        const value = document.createElement("strong");
        value.textContent = Number(count).toLocaleString("es-CO");

        item.append(label, value);
        distribution.appendChild(item);
    });

    // Tabla Top 10
    const table = document.getElementById("shipmentsTable");
    table.innerHTML = "";

    data.top_shipments.forEach(function (shipment) {
        const row = document.createElement("tr");

        const values = [
            shipment.Order_ID,
            shipment.Priority_Score,
            shipment.Priority_Level,
            shipment.Traffic,
            shipment.Weather,
            shipment.Area,
            shipment.Order_Hour
        ];

        values.forEach(function (value) {
            const cell = document.createElement("td");
            cell.textContent = value ?? "-";
            row.appendChild(cell);
        });

        table.appendChild(row);
    });
}


// ============================================================
// COMPARACIÓN EXPERIMENTAL DE ALGORITMOS
// ============================================================

if (benchmarkButton) {
    benchmarkButton.addEventListener("click", runBenchmark);
}

async function runBenchmark() {
    benchmarkButton.disabled = true;
    benchmarkButton.textContent = "Comparando algoritmos...";
    benchmarkStatus.textContent = "Consultando resultados del benchmark...";

    try {
        const response = await fetch("/benchmark", {
            method: "GET",
            cache: "no-store"
        });

        // Leer primero el texto para poder diagnosticar respuestas no JSON.
        const responseText = await response.text();

        console.log("Benchmark HTTP:", response.status);
        console.log("Benchmark respuesta:", responseText);

        if (!response.ok) {
            throw new Error(
                `Error HTTP ${response.status}: ${responseText}`
            );
        }

        let data;

        try {
            data = JSON.parse(responseText);
        } catch {
            throw new Error("La respuesta de /benchmark no es JSON válido.");
        }

        console.log("Benchmark datos recibidos:", data);
        console.log("Claves de la respuesta:", Object.keys(data));

        renderBenchmark(data);

        // Mostrar explícitamente el contenedor de resultados.
        benchmarkResults.classList.remove("hidden");
        benchmarkResults.style.display = "block";

        benchmarkStatus.textContent =
            "Comparación completada correctamente.";
    } catch (error) {
        console.error("Error mostrando el benchmark:", error);

        benchmarkStatus.textContent =
            `No se pudo mostrar la gráfica: ${error.message}`;
    } finally {
        benchmarkButton.disabled = false;
        benchmarkButton.textContent = "Volver a comparar";
    }
}


// ============================================================
// FORMATEAR TIEMPOS
// ============================================================

function formatSeconds(value) {
    const seconds = Number(value);

    if (!Number.isFinite(seconds)) {
        return "-";
    }

    if (seconds < 0.001) {
        return `${(seconds * 1000000).toFixed(2)} µs`;
    }

    if (seconds < 1) {
        return `${(seconds * 1000).toFixed(3)} ms`;
    }

    return `${seconds.toFixed(4)} s`;
}


// ============================================================
// MOSTRAR TABLA Y GRÁFICA DEL BENCHMARK
// ============================================================

function renderBenchmark(data) {
    const rows = data.benchmark_results || [];

    if (!rows.length) {
        throw new Error("El benchmark no devolvió resultados.");
    }

    benchmarkTable.innerHTML = "";
    benchmarkChart.innerHTML = "";

    // Crear las filas de la tabla con los datos reales del backend
    rows.forEach(function (item) {
        const row = document.createElement("tr");

        const values = [
            Number(item.Registros).toLocaleString("es-CO"),
            formatSeconds(item.Merge_Sort),
            formatSeconds(item.Bubble_Sort),
            `${Number(item.Speedup).toFixed(2)}×`,
            item.Merge_Correcto ? "Sí" : "No",
            item.Bubble_Correcto ? "Sí" : "No"
        ];

        values.forEach(function (value) {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        benchmarkTable.appendChild(row);
    });

    // Mayor factor de aceleración observado
    const bestSpeedup = Math.max(
        ...rows.map(function (item) {
            return Number(item.Speedup) || 0;
        })
    );

    benchmarkBestSpeedup.textContent = `${bestSpeedup.toFixed(2)}×`;

    // Gráfica única: comparación visual usando tiempos reales de /benchmark
    rows.forEach(function (item) {
        const mergeTime = Math.max(0, Number(item.Merge_Sort) || 0);
        const bubbleTime = Math.max(0, Number(item.Bubble_Sort) || 0);

        // La barra más larga representa el mayor tiempo para este tamaño
        const maxTime = Math.max(
            mergeTime,
            bubbleTime,
            Number.EPSILON
        );

        const group = document.createElement("div");
        group.className = "benchmark-chart-row";

        const heading = document.createElement("div");
        heading.className = "benchmark-chart-heading";
        heading.textContent =
            `${Number(item.Registros).toLocaleString("es-CO")} registros`;

        const mergeBar = makeBenchmarkBar(
            "Merge Sort",
            mergeTime,
            maxTime,
            "merge"
        );

        const bubbleBar = makeBenchmarkBar(
            "Bubble Sort",
            bubbleTime,
            maxTime,
            "bubble"
        );

        group.append(heading, mergeBar, bubbleBar);
        benchmarkChart.appendChild(group);
    });

    benchmarkResults.classList.remove("hidden");
}


// ============================================================
// CREAR BARRA DE TIEMPO
// ============================================================

function makeBenchmarkBar(label, time, maxTime, algorithmClass) {
    const line = document.createElement("div");
    line.className = "benchmark-bar-line";

    const name = document.createElement("span");
    name.className = "benchmark-bar-label";
    name.textContent = label;

    const track = document.createElement("div");
    track.className = "benchmark-bar-track";

    const bar = document.createElement("div");
    bar.className = `benchmark-bar ${algorithmClass}`;

    const percentage = (time / maxTime) * 100;

    bar.style.width =
        `${Math.max(time > 0 ? 1 : 0, percentage)}%`;

    const value = document.createElement("span");
    value.className = "benchmark-bar-value";
    value.textContent = formatSeconds(time);

    track.appendChild(bar);
    line.append(name, track, value);

    return line;
}


// ============================================================
// ANÁLISIS TEÓRICO DE COMPLEJIDAD
// ============================================================

async function loadComplexityAnalysis() {
    const container = document.getElementById("complexity-content");

    if (!container) {
        return;
    }

    try {
        const response = await fetch("/complexity", {
            method: "GET",
            cache: "no-store"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "No fue posible cargar el análisis."
            );
        }

        const merge = data.merge_sort;
        const bubble = data.bubble_sort;

        container.innerHTML = `
            <div class="complexity-grid">

                <article class="complexity-card">
                    <h3>Merge Sort</h3>

                    <span class="complexity-badge efficient">
                        ${merge.time_complexity}
                    </span>

                    <h4>Aplicación del Teorema Maestro</h4>

                    <p class="recurrence">
                        ${merge.recurrence}
                    </p>

                    <ul class="complexity-parameters">
                        <li><strong>a:</strong> ${merge.a}</li>
                        <li><strong>b:</strong> ${merge.b}</li>
                        <li><strong>f(n):</strong> ${merge.f_n}</li>
                        <li>
                            <strong>Término crítico:</strong>
                            ${merge.critical_term}
                        </li>
                        <li>
                            <strong>Caso aplicado:</strong>
                            ${merge.master_theorem_case}
                        </li>
                    </ul>

                    <p>${merge.explanation}</p>

                    <p>
                        <strong>Conclusión:</strong>
                        ${merge.conclusion}
                    </p>

                    <p>
                        <strong>Complejidad espacial:</strong>
                        ${merge.space_complexity}
                    </p>
                </article>

                <article class="complexity-card">
                    <h3>Bubble Sort</h3>

                    <span class="complexity-badge quadratic">
                        ${bubble.average_time_complexity}
                    </span>

                    <h4>Análisis teórico</h4>

                    <p>${bubble.explanation}</p>

                    <p>
                        <strong>Complejidad temporal:</strong>
                        ${bubble.time_complexity}
                    </p>

                    <p>
                        <strong>Complejidad espacial:</strong>
                        ${bubble.space_complexity}
                    </p>

                    <p>
                        Bubble Sort no requiere aplicar directamente
                        el Teorema Maestro para analizar su comportamiento.
                        Su número de comparaciones crece cuadráticamente
                        en el caso promedio y en el peor caso.
                    </p>
                </article>

            </div>
        `;
    } catch (error) {
        container.innerHTML = `
            <p class="complexity-error">
                No fue posible cargar el análisis de complejidad.
                Verifica que la ruta /complexity esté disponible.
            </p>
        `;

        console.error(
            "Error cargando análisis de complejidad:",
            error
        );
    }
}

loadComplexityAnalysis();