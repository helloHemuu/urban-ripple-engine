// Initialize map centered on Ujjain
const map = L.map('map').setView([23.1765, 75.7885], 14);

// Load OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Add marker for Ujjain
L.marker([23.1765, 75.7885])
    .addTo(map)
    .bindPopup("Ujjain, Madhya Pradesh");

// Backend API URL
const API_URL = "http://127.0.0.1:8000/road-impact";
let latestAnalysis = null;

// Button references
const analyzeBtn = document.getElementById("analyzeBtn");
const closuresInput = document.getElementById("closures");
const resultDiv = document.getElementById("result");

// Route layers
let originalRouteLayer = null;
let alternateRouteLayer = null;
let blockedRoadLayer = null;

// Button click event
analyzeBtn.addEventListener("click", async () => {

    const closures = parseInt(closuresInput.value);

    if (isNaN(closures) || closures < 1 || closures > 10) {
        resultDiv.innerHTML = "<p>Please enter a number between 1 and 10.</p>";
        return;
    }

    resultDiv.innerHTML = "<p>Analyzing road impact...</p>";

    try {

        const response = await fetch(`${API_URL}?closures=${closures}`);

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();
        latestAnalysis = data;

        const impact = (
            ((data.alternate_distance_m - data.original_distance_m) /
            data.original_distance_m) * 100
        );

        // Remove previous route layers
        if (originalRouteLayer) map.removeLayer(originalRouteLayer);
        if (alternateRouteLayer) map.removeLayer(alternateRouteLayer);
        if (blockedRoadLayer) map.removeLayer(blockedRoadLayer);

        // Original route - Blue
        originalRouteLayer = L.polyline(
            data.original_route_coordinates,
            {
                color: "blue",
                weight: 5,
                opacity: 0.7
            }
        ).addTo(map);

        // Alternate route - Green
        alternateRouteLayer = L.polyline(
            data.alternate_route_coordinates,
            {
                color: "green",
                weight: 6,
                opacity: 0.9
            }
        ).addTo(map);

        // Blocked roads - Red
        blockedRoadLayer = L.polyline(
            data.blocked_road_coordinates,
            {
                color: "red",
                weight: 8,
                opacity: 1
            }
        ).addTo(map);

        // Zoom to route
        map.fitBounds(alternateRouteLayer.getBounds(), {
            padding: [30, 30]
        });

        // Severity color
        let severityColor = "#22c55e";

        if (data.impact_severity === "Moderate") {
            severityColor = "#f59e0b";
        } else if (data.impact_severity === "High") {
            severityColor = "#f97316";
        } else if (data.impact_severity === "Severe") {
            severityColor = "#ef4444";
        }
        // Smart Route Recommendation

let recommendation = "";

if (!data.alternate_route_available) {
    recommendation = "No alternate route is available. Please check other road options.";
}
else if (impact < 5) {
    recommendation = "Low impact. The alternate route adds only a small travel distance.";
}
else if (impact < 15) {
    recommendation = "Moderate impact. Consider using the alternate route and allow extra travel time.";
}
else if (impact < 30) {
    recommendation = "High impact. Plan your journey carefully and consider other available roads.";
}
else {
    recommendation = "Severe impact. Significant route disruption detected. Consider delaying your journey if possible.";
}
        // Professional result dashboard
        resultDiv.innerHTML = `
            <h3>Road Impact Analysis</h3>

            <div class="metrics-grid">

                <div class="metric-card">
                    <span class="metric-label">Original Distance</span>
                    <h4>${data.original_distance_m} m</h4>
                </div>

                <div class="metric-card">
                    <span class="metric-label">Blocked Segments</span>
                    <h4>${data.blocked_segments}</h4>
                </div>

                <div class="metric-card">
                    <span class="metric-label">Alternate Distance</span>
                    <h4>${data.alternate_distance_m} m</h4>
                </div>

                <div class="metric-card">
                    <span class="metric-label">Extra Distance</span>
                    <h4>${data.extra_distance_m} m</h4>
                </div>

            </div>

            <div class="impact-box">
                <div>
                    <span class="metric-label">Route Impact</span>
                    <h2>${impact.toFixed(2)}%</h2>
                </div>

                <div class="severity-badge"
                     style="background:${severityColor}">
                    ${data.impact_severity}
                </div>
            </div>
<div class="impact-meter">

    <div class="impact-meter-header">
        <span>Additional Travel Impact</span>
        <strong>${impact.toFixed(2)}%</strong>
    </div>

    <div class="impact-track">
        <div class="impact-fill"
             style="width:${Math.min(Math.max(impact, 0), 100)}%; background:${severityColor};">
        </div>
    </div>

</div>
<div class="recommendation-box">
    <h3>🧠 Smart Route Recommendation</h3>
    <p>${recommendation}</p>
</div>
            <div class="route-legend">
            <button class="download-btn" onclick="downloadReport()">
    📄 Download Analysis Report
</button>
                <p><span class="legend-blue"></span> Original Route</p>
                <p><span class="legend-red"></span> Blocked Roads</p>
                <p><span class="legend-green"></span> Alternate Route</p>
            </div>
        `;

    } catch (error) {

        resultDiv.innerHTML = `
            <p style="color:#f87171;">
                Unable to connect to backend.
            </p>
            <p>Please ensure FastAPI is running.</p>
        `;

        console.error("Error:", error);
    }
});
// Generate Road Impact PDF Report
function downloadReport() {

    if (!latestAnalysis) {
        alert("Please analyze road impact first!");
        return;
    }

    const data = latestAnalysis;

    const impact = (
        ((data.alternate_distance_m - data.original_distance_m) /
        data.original_distance_m) * 100
    );

    const reportWindow = window.open("", "_blank");

    reportWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Urban Ripple Engine - Analysis Report</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 35px;
                    color: #1e293b;
                }

                h1 {
                    color: #0284c7;
                    text-align: center;
                }

                h2 {
                    margin-top: 30px;
                    border-bottom: 2px solid #0284c7;
                    padding-bottom: 8px;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }

                th, td {
                    border: 1px solid #cbd5e1;
                    padding: 14px;
                    text-align: left;
                }

                th {
                    background: #e0f2fe;
                }

                .summary {
                    background: #f1f5f9;
                    padding: 20px;
                    margin-top: 25px;
                    border-radius: 8px;
                }

                .footer {
                    margin-top: 50px;
                    text-align: center;
                    color: #64748b;
                }
            </style>
        </head>

        <body>

            <h1>Urban Ripple Engine</h1>

            <p style="text-align:center;">
                Intelligent Urban Road Impact & Route Analysis
            </p>

            <h2>Road Impact Analysis Report</h2>

            <p><b>Analysis Location:</b> Ujjain, Madhya Pradesh</p>

            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Result</th>
                </tr>

                <tr>
                    <td>Original Distance</td>
                    <td>${data.original_distance_m} m</td>
                </tr>

                <tr>
                    <td>Blocked Segments</td>
                    <td>${data.blocked_segments}</td>
                </tr>

                <tr>
                    <td>Alternate Distance</td>
                    <td>${data.alternate_distance_m} m</td>
                </tr>

                <tr>
                    <td>Extra Distance</td>
                    <td>${data.extra_distance_m} m</td>
                </tr>

                <tr>
                    <td>Route Impact</td>
                    <td>${impact.toFixed(2)}%</td>
                </tr>

                <tr>
                    <td>Impact Severity</td>
                    <td>${data.impact_severity}</td>
                </tr>
            </table>

            <div class="summary">
                <h3>Analysis Summary</h3>
                <h3>Smart Route Recommendation</h3>

<p>
    ${recommendation}
</p>
                Road closures have increased the original travel
                distance by ${impact.toFixed(2)}%.
                The alternate route distance is
                ${data.alternate_distance_m} meters.
            </div>

            <div class="footer">
                Generated by Urban Ripple Engine
            </div>

        </body>
        </html>
    `);

    reportWindow.document.close();

    reportWindow.onload = function() {
        reportWindow.print();
    };
}