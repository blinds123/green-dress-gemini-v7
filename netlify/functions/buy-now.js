exports.handler = async (event) => {
  const { amountUSD } = JSON.parse(event.body);
  const response = await fetch('https://simpleswap-automation-1.onrender.com/buy-now', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amountUSD })
  });
  const data = await response.json();
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  };
};
