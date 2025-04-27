document.getElementById('stockForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get references to form elements
    const submitBtn = document.querySelector('.submit-btn');

    // Update button text and disable it
    submitBtn.innerHTML = 'Generating...';
    submitBtn.disabled = true;

    try {
        // Collect user input
        const stockSymbol = document.getElementById('stockSymbol').value.toUpperCase();
        const numberOfShares = parseInt(document.getElementById('numberOfShares').value); // Updated field
        const predictionPeriod = document.getElementById('predictionPeriod').value;

        // Validate inputs
        if (!stockSymbol || isNaN(numberOfShares) || !predictionPeriod) {
            alert('Please fill out all fields correctly.');
            submitBtn.innerHTML = 'Generate Prediction';
            submitBtn.disabled = false;
            return;
        }

        // Send POST request to the backend
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                stock_symbol: stockSymbol,
                number_of_shares: numberOfShares, // Updated field
                prediction_period: predictionPeriod
            })
        });

        // Parse the response
        const result = await response.json();

        if (response.ok) {
            // Open a new tab/window with the prediction results
            const newTab = window.open('', '_blank');  // Opens a new tab

            // Write the prediction results to the new tab
            newTab.document.write(`
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Prediction Results - TimeForge</title>
                    <style>
                        * {
                            margin: 0;
                            padding: 0;
                            box-sizing: border-box;
                        }

                        :root {
                            --primary: #646cff;
                            --secondary: #535bf2;
                            --bg: #0a0a0a;
                            --text: #ffffff;
                        }

                        body {
                            font-family: 'Inter', sans-serif;
                            background: var(--bg);
                            color: var(--text);
                            overflow-x: hidden;
                            padding: 2rem;
                        }

                        .result-container {
                            max-width: 600px;
                            margin: 0 auto;
                            background: rgba(255, 255, 255, 0.05);
                            padding: 2rem;
                            border-radius: 16px;
                            backdrop-filter: blur(10px);
                            transition: all 0.3s ease;
                        }

                        .result-container h2 {
                            font-size: 2rem;
                            margin-bottom: 1rem;
                            color: var(--primary);
                        }

                        .result-container p {
                            opacity: 0.8;
                            line-height: 1.6;
                            margin-bottom: 1rem;
                        }

                        .result-container ul {
                            list-style-type: disc;
                            margin-left: 1.5rem;
                            opacity: 0.8;
                        }

                        .result-container ul li {
                            margin-bottom: 0.5rem;
                        }
                    </style>
                </head>
                <body>
                    <div class="result-container">
                        <h2>Prediction Results</h2>
                        <p><strong>Stock Symbol:</strong> ${result.stock_symbol}</p>
                        <p><strong>Currency:</strong> ${result.currency === 'INR' ? '₹ INR' : '$ USD'}</p>
                        <p><strong>Current Price:</strong> ${result.currency === 'INR' ? `₹${result.current_price.toFixed(2)}` : `$${result.current_price.toFixed(2)}`}</p>
                        <p><strong>Predicted Price:</strong> ${result.currency === 'INR' ? `₹${result.predicted_price.toFixed(2)}` : `$${result.predicted_price.toFixed(2)}`}</p>
                        <p><strong>Price Change:</strong> ${result.price_change_percentage}%</p>
                        <p><strong>Recommendation:</strong> ${result.recommendation}</p>
                        <p><strong>Number of Shares:</strong> ${result.number_of_shares}</p>
                        <p><strong>Total Cost:</strong> ${result.currency === 'INR' ? `₹${result.total_cost.toFixed(2)}` : `$${result.total_cost.toFixed(2)}`}</p>
                        <p><strong>Profit:</strong> ${result.currency === 'INR' ? `₹${result.profit.toFixed(2)}` : `$${result.profit.toFixed(2)}`}</p>
                        <p><strong>Final Value:</strong> ${result.currency === 'INR' ? `₹${result.final_value.toFixed(2)}` : `$${result.final_value.toFixed(2)}`}</p>
                        <h2>Pros and Cons of Purchasing the Stock</h2>
                        <p><strong>Pros:</strong></p>
                        <ul>
                            ${result.analysis.pros.map(pro => `<li>${pro}</li>`).join('')}
                        </ul>
                        <p><strong>Cons:</strong></p>
                        <ul>
                            ${result.analysis.cons.map(con => `<li>${con}</li>`).join('')}
                        </ul>
                    </div>
                </body>
                </html>
            `);

            // Close the writing stream for the new tab
            newTab.document.close();
        } else {
            alert(`Error: ${result.error}`);
        }
    } catch (error) {
        console.error('Error during prediction:', error);
        alert('An error occurred while generating the prediction.');
    } finally {
        // Re-enable the button
        submitBtn.innerHTML = 'Generate Prediction';
        submitBtn.disabled = false;
    }
});